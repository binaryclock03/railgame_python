import pygame as pg
import sys
import threading
import draw_lib as dl
import terrain2
from draw_lib import ImageFont

def run_scene(screen):
    running = True
    game_paused = False

    font_pixel = ImageFont("fonts\pixel_small", scale=3)

    #START
    map = terrain2.Terrain((100,100), 4, sea_level=0.5)

    while running == True:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    if not 'task' in locals():
                        task = threading.Thread(target=generate_map, args=[map])
                        task.start()
                
                elif event.key == pg.K_SPACE:
                    game_paused = True

        screen.fill((60, 70, 80))

        draw_worldmap(map.get_world_map_image(), screen, 400, 0)

        # check if game is paused
        if game_paused == True:
            pass
        else:
            dl.draw_text(screen, "Press SPACE to pause", font_pixel, 40, 160)

        pg.display.flip()

    return


def generate_map(map):
    map.generate_world_map()

def draw_worldmap(image, screen, x, y, scale = 1):
    surf = pg.surfarray.make_surface(image)
    surf = pg.transform.scale(surf, (800,800))
    screen.blit(surf, (x, y))      
