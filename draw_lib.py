import pygame as pg
import os
import CONSTANTS

# button class
class Button():
    def __init__(self, x, y, image, scale, image_hover = None, image_click = None) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image_click = image_click
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

        if action:
            surface.blit(self.image_click, (self.rect.x, self.rect.y))
        elif hover:
            surface.blit(self.image_hover, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

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
