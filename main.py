import pygame as pg
import scenes.scene_main_menu as scene_main_menu
import scenes.scene_generator as scene_generator
import scenes.scene_spline_testing as scene_spline_testing

# pygame stuff
pg.init()
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200,800
screen = pg.display.set_mode(SCREEN_SIZE)

# game variables
scene = "main_menu"

while True:
    if scene == "main_menu":
        scene = scene_main_menu.run_scene(screen)
    elif scene == "generator":
        scene = scene_generator.run_scene(screen)
    elif scene == "spline_testing":
        scene = scene_spline_testing.run_scene(screen)