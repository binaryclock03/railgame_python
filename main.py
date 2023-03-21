import os
import sys
import pygame as pg
from pygame import transform
import terrain2
import threading

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = (image.get_size())
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def generate_map():
    map.generate_world_map()

def draw_worldmap(image, screen, x, y, scale = 1):
    surf = pg.surfarray.make_surface(image)
    surf = pg.transform.scale(surf, (800,800))
    screen.blit(surf, (x, y))      

#START
map = terrain2.Terrain((100,100), 4, sea_level=0.45)

pg.init()

size = width, height = 1200,800
screen = pg.display.set_mode(size)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                task = threading.Thread(target=generate_map)
                task.start()

    draw_worldmap(map.get_world_map_image(), screen, 400, 0)
    pg.display.flip()