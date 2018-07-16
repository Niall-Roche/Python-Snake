import pygame
import random
import sqlite3

from InputBox import InputBox
from Block import Block
from Button import Button

pygame.init()
snake_icon = pygame.image.load("assets/images/snake_icon.png")
pygame.display.set_icon(snake_icon);

conn = sqlite3.connect("DB/gameDB.db")
conn.row_factory = sqlite3.Row

display_width = 800
display_height = 600
top_section_height = display_height/10
game_title = "NO STEP ON SNEK"

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption(game_title)

gameExit = False
gameOver = False
paused = False
startMenu = True
scoreMenu = False

white = (255,255,255)
black = (64, 70, 79)
green = (0,155,0)
game_colour = (214, 44, 44)
game_colour_light = (234, 96, 96)
game_green = (51, 206, 4)
game_green_light = (131, 242, 118)
game_blue = (27, 106, 232)
game_blue_light = (96, 181, 242)

defaultFont = pygame.font.SysFont(None, 25)
yahooFont = pygame.font.Font("assets/fonts/Yahoo.ttf", 25)
exedore = pygame.font.Font("assets/fonts/exedore.ttf", 25)
exedorel = pygame.font.Font("assets/fonts/exedorel.ttf", 45)

snakeHeadImg = pygame.image.load("assets/images/snake_head.png")
appleImg = pygame.image.load("assets/images/apple_1.gif")
AudioNoImg = pygame.image.load("assets/images/audio-no.png")
AudioYesImg = pygame.image.load("assets/images/audio-yes.png")

audio_active = True

clock = pygame.time.Clock()

def createBlock(xPos, yPos, colour, size, img=None):
    block = Block(xPos, yPos, colour, size, img)
    return block

def drawList(items):
    for item in items:
        if item.img != None:
            gameDisplay.blit(item.img, [item.xPos, item.yPos])
        else:
            gameDisplay.fill(item.colour, rect=[item.xPos,item.yPos,item.size,item.size])

def message_text(msg, colour, font):
    text = font.render(msg, True, colour)
    return text, text.get_rect()

def message_to_screen(msg,colour,font=defaultFont, x_offset=0, y_offset=0):
    screen_text, text_rect = message_text(msg, colour, font)
    text_rect.center = (display_width/2) + x_offset, (display_width/2) + y_offset
    gameDisplay.blit(screen_text, text_rect)

def rotateHead(img, direction):
    return {
        'right': pygame.transform.rotate(img, 270),
        'left': pygame.transform.rotate(img, 90),
        'up': pygame.transform.rotate(img, 0),
        'down': pygame.transform.rotate(img, 180)
    }[direction]

def snake(snakeList, maxLength, direction):
    if len(snakeList) > maxLength:
        del snakeList[0]

    gameDisplay.blit(rotateHead(snakeHeadImg, direction), [snakeList[-1].xPos, snakeList[-1].yPos])

    for snk in snakeList[:-1]:
        gameDisplay.fill(snk.colour, rect=[snk.xPos,snk.yPos,snk.size,snk.size])

def topSection():
    score = 'S C O R E : '
    gameDisplay.fill(game_colour, rect=[0,0,display_width,top_section_height])
    message_to_screen(score, white, exedore, y_offset=-370)

def updateScore(currentScore):
    if int(currentScore) > 9 and int(currentScore) < 100:
        scoreOffset = 120
    elif int(currentScore) > 99 and int(currentScore) < 1000:
        scoreOffset = 140
    else:
        scoreOffset = 110
    message_to_screen(currentScore, white, exedore, scoreOffset, y_offset=-370)

def save_player(name, score):
    c = conn.cursor()
    c.execute('select MAX(id) as max_id from players')
    nextId = c.fetchone()["max_id"] + 1
    if c.execute('select "Y" from players where upper(name) = ?', (name.upper(),)).fetchone() == None:
        c.execute('insert into players(id, name, score) values(?,?,?)', (nextId, name, score))
    else:
        c.execute("""update players
                     set score = ?
                     where upper(name) = ?""", (score, name.upper()))
    conn.commit()

def drawBtns(btns):
    for btn in btns:
        btn.draw(gameDisplay)

def handleBtnEvents(btns, event):
    for btn in btns:
        btn.handle_event(event)

def handleGameOptions(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        toggle_audio()

def handleAudio():
    if pygame.mixer.music.get_busy() and not audio_active:
        pygame.mixer.music.stop()
    elif not pygame.mixer.music.get_busy() and audio_active:
        pygame.mixer.music.play(-1)

    if audio_active:
        audioBtn.update_img(AudioYesImg)
    else:
        audioBtn.update_img(AudioNoImg)

def toggle_audio():
    global audio_active
    audio_active = not audio_active

audioBtn = Button(display_width-50,
                  top_section_height-50,
                  30,
                  30,
                  colour=black,
                  img=AudioYesImg,
                  active_event=toggle_audio)

def gameLoop():
    global startMenu
    global gameExit
    global gameOver
    global paused
    blockSize = 20
    lead_x = display_width/2
    movement = 20
    # blockSize = movement
    lead_x_change = movement
    lead_y = display_height/2
    lead_y_change = 0
    fps = 15
    apples = []
    maxApples = 3
    snakeList = []
    maxLength = 5
    score = 0
    direction = "right"

    gameExit = False
    gameOver = False
    paused = False

    pygame.mixer.music.load("assets/sound/Androids.wav")
    while not gameExit:

        if startMenu:
            startLoop()

        if scoreMenu:
            scoreBoardLoop()

        if paused:
            pauseLoop()

        box = InputBox(display_width/2 -20, display_height/2 + 30, 140, 32)

        if gameOver:
            gameOverLoop(box, score)

        for event in pygame.event.get():
            handleGameOptions(event)
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if lead_y_change != movement:
                    lead_y_change = -movement
                    lead_x_change = 0
                    direction = 'up'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if lead_y_change != -movement:
                    lead_y_change = movement
                    lead_x_change = 0
                    direction = 'down'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if lead_x_change != -movement:
                    lead_x_change = movement
                    lead_y_change = 0
                    direction = 'right'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if lead_x_change != movement:
                    lead_x_change = -movement
                    lead_y_change = 0
                    direction = 'left'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = True
            # elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN):
            #     lead_x_change = 0
            #     lead_y_change = 0

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x < 0 or (lead_x + (blockSize-movement)) >= display_width or lead_y < top_section_height or (lead_y + (blockSize-movement)) >= display_height:
            gameOver = True

        # randAppleX = round(random.randrange(1, display_width-blockSize)/blockSize)*blockSize
        # randAppleY = round(random.randrange(top_section_height, display_height-blockSize)/blockSize)*blockSize
        randAppleX = random.randrange(1, display_width-blockSize)
        randAppleY = random.randrange(top_section_height, display_height-blockSize)
        randApple = random.randrange(1, 1000)
        if len(apples) < maxApples and randApple % 17 == 0:
            apples.append(createBlock(randAppleX, randAppleY, game_colour, blockSize, appleImg))

        snakeHead = createBlock(lead_x,lead_y,green,blockSize)
        snakeList.append(snakeHead)

        gameDisplay.fill(white)
        topSection()
        audioBtn.draw(gameDisplay)
        updateScore(str(score))
        drawList(apples)
        snake(snakeList, maxLength, direction)

        if not startMenu and not scoreMenu and not gameOver:
            pygame.display.update()

        for apple in apples:
            if (lead_x >= apple.xPos and lead_x <= apple.xPos + apple.size) or (lead_x + blockSize >= apple.xPos and lead_x + blockSize <= apple.xPos + apple.size):
                if (lead_y >= apple.yPos and lead_y <= apple.yPos + apple.size) or (lead_y + blockSize >= apple.yPos and lead_y + blockSize <= apple.yPos + apple.size):
                    maxLength+=1
                    score+=1
                    apples.remove(apple)
                    drawList(apples)

        for snk in snakeList[:-1]:
            if (lead_y_change != 0 or lead_x_change != 0) and lead_x == snk.xPos and lead_y == snk.yPos:
                gameOver = True

        if gameOver:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/sound/80s-bass-line-loop-86-bpm.wav")

        clock.tick(fps)

    quit_event()

def pauseLoop():

    def continue_game():
        global paused
        paused = False

    def main_menu():
        global paused
        global startMenu
        paused = False
        startMenu = True
        gameLoop()

    continueBtn = Button(125,
                          display_height -50,
                          text="CONTINUE",
                          colour=game_colour,
                          active_colour=game_colour_light,
                          font=exedore,
                          active_event=continue_game)

    mainMenuBtn = Button(continueBtn.get_width() + continueBtn.get_xPos() + 50,
                         display_height -50,
                         text="MAIN MENU",
                         colour=game_green,
                         active_colour=game_green_light,
                         font=exedore,
                         active_event=main_menu)

    quitBtn = Button(mainMenuBtn.get_width() + mainMenuBtn.get_xPos() + 50,
                     display_height -50,
                     text="QUIT",
                     colour=game_blue,
                     active_colour=game_blue_light,
                     font=exedore,
                     active_event=quit_event)

    btns = ((audioBtn, continueBtn, mainMenuBtn, quitBtn))

    while paused:
        gameDisplay.fill(white)
        message_to_screen("PAUSED", game_colour, exedorel, y_offset=-150)
        message_to_screen("Press P to continue", game_colour, y_offset=-100)
        drawBtns(btns)
        handleAudio()
        pygame.display.update()

        for event in pygame.event.get():
            handleGameOptions(event)
            handleBtnEvents(btns, event)

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                quit_event()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                continue_game()


def gameOverLoop(box, score):

    def play_again():
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sound/Androids.wav")
        gameLoop()

    def main_menu():
        global startMenu
        startMenu = True
        gameLoop()

    playAgainBtn = Button(100,
                          display_height -50,
                          text="PLAY AGAIN",
                          colour=game_colour,
                          active_colour=game_colour_light,
                          font=exedore,
                          active_event=play_again)

    mainMenuBtn = Button(playAgainBtn.get_width() + playAgainBtn.get_xPos() + 50,
                         display_height -50,
                         text="MAIN MENU",
                         colour=game_green,
                         active_colour=game_green_light,
                         font=exedore,
                         active_event=main_menu)

    quitBtn = Button(mainMenuBtn.get_width() + mainMenuBtn.get_xPos() + 50,
                     display_height -50,
                     text="QUIT",
                     colour=game_blue,
                     active_colour=game_blue_light,
                     font=exedore,
                     active_event=quit_event)

    btns = ((audioBtn, playAgainBtn, mainMenuBtn, quitBtn))

    while gameOver:
        gameDisplay.fill(black)
        message_to_screen("GAME OVER", game_colour, exedorel, y_offset=-150)
        message_to_screen(f"Your score was: {score}", game_colour, y_offset=-100)
        message_to_screen("Enter your name", game_colour, x_offset=-95, y_offset=-50)
        drawBtns(btns)
        box.update()
        box.draw(gameDisplay)
        handleAudio()
        pygame.display.update()

        for event in pygame.event.get():
            box.handle_event(event)
            if not box.get_active():
                handleGameOptions(event)
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    quit_event()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    play_again()
            else:
                if event.type == pygame.QUIT:
                    quit_event()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    save_player(box.get_text().strip(), str(score))
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/sound/Androids.wav")
                    main_menu()
            handleBtnEvents(btns, event)


def startLoop():

    def play_from_start():
        global startMenu
        startMenu = False

    def score_from_start():
        global startMenu
        global scoreMenu
        startMenu = False
        scoreMenu = True

    playBtn = Button(display_width/2, display_height/2, text="PLAY", colour=game_colour, active_colour=game_colour_light, center_to_self=True, font=exedore, active_event=play_from_start)
    scoreBtn = Button(display_width/2, display_height/2 + 75, text="SCORE BOARD", colour=game_colour, active_colour=game_colour_light, center_to_self=True, font=exedore, active_event=score_from_start)
    quitBtn = Button(display_width/2, display_height/2 + 150, text="QUIT", colour=game_colour, active_colour=game_colour_light, center_to_self=True, font=exedore, active_event=quit_event)

    btns = ((audioBtn, playBtn, scoreBtn, quitBtn))

    while startMenu:
        gameDisplay.fill(black)
        message_to_screen(game_title, game_colour, exedorel, y_offset=-200)
        drawBtns(btns)
        for event in pygame.event.get():
            handleBtnEvents(btns, event)
            handleGameOptions(event)
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                quit_event()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                play_from_start()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                score_from_start()
        handleAudio()
        pygame.display.update()

def scoreBoardLoop():

    def back_to_start():
        global scoreMenu
        global startMenu
        startMenu = True
        scoreMenu = False

    c = conn.cursor()

    goBackBtn = Button(display_width/2,
                       display_height - 50,
                       text="GO BACK",
                       colour=game_colour,
                       active_colour=game_colour_light,
                       center_to_self=True,
                       font=exedore,
                       active_event=back_to_start)

    while scoreMenu:
        offsetY = -280
        gameDisplay.fill(black)
        message_to_screen('PLAYER', green, y_offset=-300, x_offset=-50)
        message_to_screen('SCORE', green, y_offset=-300, x_offset=50)
        drawBtns((audioBtn, goBackBtn))
        handleAudio()
        for player in c.execute('select upper(name) name, score from players order by score desc'):
            message_to_screen(str(player["name"]), game_colour, y_offset=offsetY, x_offset=-50)
            message_to_screen(str(player["score"]), game_colour, y_offset=offsetY, x_offset=50)
            offsetY+=20
        pygame.display.update()

        for event in pygame.event.get():
            handleGameOptions(event)
            handleBtnEvents((goBackBtn,), event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                back_to_start()
            elif event.type == pygame.QUIT:
                quit_event()

def quit_event():
    conn.close()
    pygame.quit()
    quit()

gameLoop()
