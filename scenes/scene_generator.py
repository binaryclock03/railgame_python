import pygame as pg
import sys
import threading
import terrain2
from game.menuObject import ImageFont, draw_text, load_image

def run_scene(screen):
    running = True
    game_paused = False

    # define fonts
    font_pixel = ImageFont("fonts\pixel_small", scale=3)

    #main_menu_objects:dict = {}
    TEXT_OFFSET_MENU_BUTTON = (18, 18)
    IMAGES_MENU_BUTTON =  [load_image("menu\\sepha_button\\red_sepha_button.png"), load_image("menu\\sepha_button\\yel_sepha_button.png"), None]
    IMAGES_MENU_TEXTBOX = [load_image("menu\\sepha_button\\red_sepha_button.png"), None, load_image("menu\\sepha_button\\yel_sepha_button.png")]

    #START
    map = terrain2.Terrain((100,100), 4, sea_level=0.5)
    generator_task = threading.Thread(target=generate_map, args=[map])
    generator_task.start()

    while running == True:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    if not generator_task.is_alive():
                        generator_task.join()
                        generator_task = threading.Thread(target=generate_map, args=[map])
                        generator_task.start()

        screen.fill((60, 70, 80))

        draw_worldmap(map.get_world_map_image(), screen, 400, 0)

        draw_text(screen, "F ONE TO REGEN", font_pixel, 20, 100)

        pg.display.flip()

    return


def generate_map(map:terrain2.Terrain):
    import random as rand
    map.set_seed(rand.randint(0, 99999))
    map.generate_world_map()

def draw_worldmap(image, screen, x, y, scale = 1):
    surf = pg.surfarray.make_surface(image)
    surf = pg.transform.scale(surf, (800,800))
    screen.blit(surf, (x, y))      
