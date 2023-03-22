import pygame as pg
import terrain2
import scenes.scene_main_menu as scene_main_menu
import scenes.scene_generator as scene_generator

#START
map = terrain2.Terrain((100,100), 4, sea_level=0.5)

pg.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200,800
screen = pg.display.set_mode(SCREEN_SIZE)

# game variables
game_paused = False

# define fonts
font = pg.font.SysFont("arialblack", 40)

# define colors
TEXT_COL = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

scene = "main_menu"
while True:
    if scene == "main_menu":
        scene_main_menu.run_scene(screen)
    elif scene == "generator":
        scene_generator.run_scene(screen)