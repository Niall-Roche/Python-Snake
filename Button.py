import pygame
pygame.init()

class Button:

    blue_green = ((0,255,170))

    defaultFont = pygame.font.Font("assets/fonts/GeosansLight.ttf", 20)

    def __init__(self,
                 x,
                 y,
                 w=None,
                 h=None,
                 text='',
                 img=None,
                 colour=blue_green,
                 active_colour=None,
                 center_to_self=False,
                 font=defaultFont,
                 active_event=None):
        self.colour = colour
        self.active_colour = active_colour if active_colour is not None else colour
        self.text = text
        self.font = font
        self.img=img
        self.active_event = active_event
        self.__current_colour = self.colour
        self.__txt_surface = font.render(text, True, self.__current_colour)
        self.__active = False
        self.__focus = False

        if w is None and h is None:
            w = self.__txt_surface.get_width() + 10
            h = self.__txt_surface.get_height() + 10

        if center_to_self:
            x = x - w/2

        self.rect = pygame.Rect(x, y, w, h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.__current_colour = self.active_colour
                self.__focus = True
            else:
                self.__current_colour = self.colour
                self.focus = False
            self.__txt_surface = self.font.render(self.text, True, self.__current_colour)

        if self.__focus and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.active_event:
            self.active_event()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.__active = True
                if self.active_event:
                    self.active_event()
        else:
            self.__active = False

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.rect.x, self.rect.y))
        else:
            # Blit the text.
            screen.blit(self.__txt_surface, (self.rect.x + 5, self.rect.y + 5))
            # Blit the rect.
            pygame.draw.rect(screen, self.__current_colour, self.rect, 2)

    def update_img(self, img):
        self.img = img

    def get_text(self):
        return self.text

    def get_width(self):
        return self.rect.w

    def get_height(self):
        return self.rect.h

    def get_xPos(self):
        return self.rect.x

    def get_yPos(self):
        return self.rect.y

    def get_focus(self):
        return self.__focus

    def set_focus(self, tgl):
        self.__focus = tgl
