import pygame as pg
import os
import CONSTANTS

# abstract MenuObject
class MenuObject():
    def __init__(self, x, y, image) -> None:
        pass

    def draw(self, screen) -> bool:
        return False

# abstract Clickable
class Clickable(MenuObject):
    def __init__(self, x, y, image, scale = 1, image_hover = None, image_click = None) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

        if image_hover is None:
            self.image_hover = self.image
        else:
            self.image_hover = pg.transform.scale(image_hover, (int(width * scale), int(height * scale)))

        if image_click is None:
            self.image_click = self.image
        else:
            self.image_click = pg.transform.scale(image_click, (int(width * scale), int(height * scale)))

# Button class
class Button(Clickable):
    def __init__(self, x, y, image, scale, image_hover = None, image_click = None) -> None:
        super().__init__(x, y, image, scale, image_hover=image_hover, image_click=image_click)

    def draw(self, surface) -> bool:
        action = False
        hover = False

        # get mouse position
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            hover = True
            if not self.clicked and pg.mouse.get_pressed()[0]:
                self.clicked = True
                action = True
            
        if self.clicked and not pg.mouse.get_pressed()[0]:
            self.clicked = False

        if self.clicked:
            surface.blit(self.image_click, (self.rect.x, self.rect.y))
        elif hover:
            surface.blit(self.image_hover, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

# TextBox class
class TextBox(Clickable):
    def __init__(self, x, y, image, scale, image_hover = None, image_click = None):
        super().__init__(x, y, image, scale, image_hover=image_hover, image_click=image_click)

    def draw(self, surface):
        action = False
        hover = False

        # get mouse position
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            hover = True
            if not self.clicked and pg.mouse.get_pressed()[0]:
                self.clicked = True
                action = True
            
        if self.clicked and pg.mouse.get_pressed()[0] and not hover:
            self.clicked = False

        if self.clicked:
            surface.blit(self.image_click, (self.rect.x, self.rect.y))
        elif hover:
            surface.blit(self.image_hover, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action



# draw text
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#load image function
def load_image(name, colorkey=None, scale=1) -> pg.image:
    fullname = os.path.join(CONSTANTS.data_dir, name)
    image = pg.image.load(fullname)

    size = (image.get_size())
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    #image = image.convert()
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image
