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
                 reference=None,
                 text=None,
                 img=None,
                 symbol=None,
                 colour=blue_green,
                 active_colour=None,
                 center_to_self=False,
                 font=defaultFont,
                 onClick=None,
                 onClickParams=None):
        self.reference = reference
        self.colour = colour
        self.active_colour = active_colour if active_colour is not None else colour
        self.text = text
        self.font = font
        self.img=img
        self.__onClick = onClick
        self.__onClickParams = onClickParams
        self.__current_colour = self.colour
        self.__active = False
        self.__focus = False
        self.symbol = symbol
        self.__txt_surface = font.render(text, True, self.__current_colour) if text is not None else None

        if w is None and h is None and self.symbol is None:
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
            if self.__txt_surface:
                self.__txt_surface = self.font.render(self.text, True, self.__current_colour)

        # if self.__focus and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.onClick:
        #     self.onClick( args )

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.__active = True
                if self.__onClick:
                    if self.__onClickParams:
                        self.__onClick(self.__onClickParams)
                    else:
                        self.__onClick()
        else:
            self.__active = False

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.rect.x, self.rect.y))
        elif self.symbol == "TRIANGLE_UP":
            triangle_points = ((self.rect.x + self.rect.w/2, self.rect.y + 5),
                               (self.rect.x + 5, self.rect.y + self.rect.h - 5),
                               (self.rect.x + self.rect.w - 5, self.rect.y + self.rect.h - 5))
            pygame.draw.polygon(screen, self.__current_colour, triangle_points)
            pygame.draw.rect(screen, self.__current_colour, self.rect, 2)
        elif self.symbol == "TRIANGLE_DOWN":
            triangle_points = ((self.rect.x + self.rect.w/2, self.rect.y + self.rect.h - 5),
                               (self.rect.x + 5, self.rect.y + 5),
                               (self.rect.x + self.rect.w - 5, self.rect.y + 5))
            pygame.draw.polygon(screen, self.__current_colour, triangle_points)
            pygame.draw.rect(screen, self.__current_colour, self.rect, 2)
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
