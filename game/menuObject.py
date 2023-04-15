import pygame as pg
import os
from CONSTANTS import BLACK, DATA_DIR

# abstract MenuObject
class MenuObject():
    def __init__(self, x, y, image) -> None:
        pass

    def draw(self, screen) -> bool:
        return False

# abstract Clickable
class Clickable(MenuObject):
    def __init__(self, position, images, scale=1, 
                 text="", font=None, text_color=BLACK, text_offset = (0, 0)) -> None:
        # image vars
        width = images[0].get_width()
        height = images[0].get_height()
        self.image = pg.transform.scale(images[0], (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        # text vars
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_x = text_offset[0] + position[0]
        self.text_y = text_offset[1] + position[1]

        # internal state vars
        self.clicked = False

        # setting hover image
        if images[1] is None:
            self.image_hover = self.image
        else:
            self.image_hover = pg.transform.scale(images[1], (int(width * scale), int(height * scale)))

        # setting click image
        if images[2] is None:
            self.image_click = self.image
        else:
            self.image_click = pg.transform.scale(images[2], (int(width * scale), int(height * scale)))

# Button class
class Button(Clickable):
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
            if not self.font is None: draw_text(surface, self.text, self.font, self.text_x, self.text_y, text_col=self.text_color)
        elif hover:
            surface.blit(self.image_hover, (self.rect.x, self.rect.y))
            if not self.font is None: draw_text(surface, self.text, self.font, self.text_x, self.text_y, text_col=self.text_color)
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
            if not self.font is None: draw_text(surface, self.text, self.font, self.text_x, self.text_y, text_col=self.text_color)
        
        return action

# TextBox class
class TextBox(Clickable):
    def __init__(self, position, images, scale=1, 
                 text="", font=None, text_color=BLACK, text_offset = (0, 0)) -> None:
        super().__init__(position, images, scale, text=text, font=font, text_color=text_color, text_offset=text_offset)
        self.written_text = ""

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

        if self.clicked:
            if pg.mouse.get_pressed()[0] and not hover:
                self.clicked = False

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key== pg.K_BACKSPACE:
                        self.written_text = self.written_text[:-1]
                    elif event.key == pg.K_RETURN:
                        self.clicked = False
                    else:
                        self.written_text += event.unicode.upper()
                pg.event.post(event)
        

        if self.clicked:
            surface.blit(self.image_click, (self.rect.x, self.rect.y))
            if not self.font is None: draw_text(surface, self.written_text, self.font, self.text_x, self.text_y, text_col=self.text_color)
        elif hover:
            surface.blit(self.image_hover, (self.rect.x, self.rect.y))
            if not self.font is None: draw_text(surface, self.written_text, self.font, self.text_x, self.text_y, text_col=self.text_color)
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
            if not self.font is None: draw_text(surface, self.written_text, self.font, self.text_x, self.text_y, text_col=self.text_color)
        
        return action

# draw text
def draw_text(screen, text, font, x, y, text_col=(0,0,0)):
    img = font.render(text)
    screen.blit(img, (x, y))

#load image function
def load_image(name, colorkey=None, scale=1) -> pg.surface.Surface:
    fullname = os.path.join(DATA_DIR, name)
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

# creates multisegment box
def mutli_box(box_dir_name, size:tuple) -> pg.surface.Surface:
    box_dir_path = os.path.join(DATA_DIR, box_dir_name)

    segment_names = ["single", "start", "middle", "end", "top_left", "top_mid", "top_right", "mid_right", "bot_right", "bot_mid", "bot_left", "mid_left", "mid_mid"]

    segments = {}
    for segment_name in segment_names:
        segments.update({segment_name:load_image(os.path.join(box_dir_path, segment_name + ".png"))})

    # single panel
    if size[0] == 1:
        return segments.get("single")
    
    # horizontal panel
    if size[1] == 1:
        start_extra = segments.get("start").get_size()[0] - segments.get("middle").get_size()[0]
        end_extra   = segments.get("end").get_size()[0]   - segments.get("middle").get_size()[0]
        
        textbox_image = pg.surface.Surface(((segments.get("middle").get_size()[0] * size[0]) + start_extra + end_extra, segments.get("single").get_size()[0]), pg.SRCALPHA).convert_alpha()
        pos_x = 0
        for x in range(size[0]):
            if x == 0:
                name_type = "start"
            elif x == size[0]-1:
                name_type = "end"
            else:
                name_type = "middle"
            
            segment = segments.get(name_type)
            textbox_image.blit(segment, (pos_x, 0))
            pos_x += segment.get_size()[0]

        return textbox_image

class ImageFont():
    def __init__(self, font_dir_name, scale=1):
        self.scale = scale
        self.characters = {}
        self.char_len = {}
        font_dir_path = os.path.join(DATA_DIR, font_dir_name)
        for filename in os.listdir(font_dir_path):
            character_name = filename.removesuffix(".png")

            if character_name == "period":       character_name = "."
            elif character_name == "comma":      character_name = ","
            elif character_name == "word_space": character_name = " "

            filepath = os.path.join(font_dir_path, filename)
            char_image = load_image(filepath, scale=self.scale)
            self.characters.update({character_name: char_image})
            self.char_len.update({character_name: char_image.get_size()[0]})
    
    def render(self, text:str) -> pg.surface.Surface:
        # turn text string into list of characters
        text = [*text]
        # define the space between characters character early because it will be used a lot
        char_space = self.characters.get("char_space")
        # some important position tracking variables
        pos_x = 0
        text_len = 0

        # loop over characters and figure out how big the surface to blit to will have to be
        # this needs to happen because each character isnt the same length
        for character in text:
            if not character in self.char_len.keys(): text_len += list(self.char_len.values())[0]
            else: text_len += self.char_len.get(character)
            text_len += self.char_len.get("char_space")

        # define text_image which will be returned
        base_size = list(self.characters.values())[0].get_size()
        text_image = pg.surface.Surface((text_len*self.scale, base_size[1]*self.scale), pg.SRCALPHA).convert_alpha()

        for character in text:
            # check if character actually exists, if not, return first in self.characters
            if not character in self.characters.keys(): char_image = list(self.characters.values())[0]
            else: char_image = self.characters.get(character)
            
            # blit character and character space to text_image
            text_image.blit(char_image, (pos_x, 0))
            text_image.blit(char_space, (pos_x + char_image.get_size()[0], 0) )

            # update position to draw next character
            pos_x += char_image.get_size()[0] + self.char_len.get("char_space")
        
        # return text_image generated
        return text_image

class Container():
    def __init__():
        pass