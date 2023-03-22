import pygame as pg
import sys
import threading
import draw_lib as dl

def run_scene(screen):
    running = True

    while running == True:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    if not 'task' in locals():
                        task = threading.Thread(target=generate_map)
                        task.start()
                
                elif event.key == pg.K_SPACE:
                    game_paused = True

        screen.fill((60, 70, 80))

        draw_worldmap(map.get_world_map_image(), screen, 400, 0)

        # check if game is paused
        if game_paused == True:
            pass
        else:
            dl.draw_text("Press SPACE to pause", font, TEXT_COL, 40, 160)

    return


def generate_map():
    map.generate_world_map()

def draw_worldmap(image, screen, x, y, scale = 1):
    surf = pg.surfarray.make_surface(image)
    surf = pg.transform.scale(surf, (800,800))
    screen.blit(surf, (x, y))      
