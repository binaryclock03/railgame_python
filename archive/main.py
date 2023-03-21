import os
import sys
import time
import pygame as pg
import terrain
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
    for i in range((map._size_chunks[1] * map._size_chunks[0])):
        map.generate_chunk(i, resolution = 4, insert_to_map=True)

        if i % (map._size_chunks[0]*20) == (map._size_chunks[0]*20)-1:
            pass
            map.convert_heightmap_to_mapimage()
    map.convert_heightmap_to_mapimage()
        

map = terrain.Terrain()
map.set_world_size((100,100))

pg.init()

size = width, height = 800,800

screen = pg.display.set_mode(size)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                map._reset_world_map_heightmap()
                map.set_seed(-1)
                task = threading.Thread(target=generate_map)
                task.start()
            
            if event.key == pg.K_F2:
                map.set_sealevel(map._sealevel + 0.025)

            if event.key == pg.K_F3:
                map.set_sealevel(map._sealevel - 0.025)

            if event.key == pg.K_F4:
                map.convert_heightmap_to_countourmap_image()

    map.draw_worldmap(screen, 0, 0)
    pg.display.flip()