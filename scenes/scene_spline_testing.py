import pygame as pg
import sys
from game.rails.splines import Spline as Spline, SplineNode
from CONSTANTS import WHITE
from game.menuObject import ImageFont, load_image, Button
import numpy as np
from game.rails.action import Action

def run_scene(screen):
    running = True
    game_paused = False

    action = Action()
    import game.rails.rail_placer
    rail_placer = game.rails.rail_placer.RailPlacer(action)

    global splines 
    splines = []

    font_pixel = ImageFont("fonts\pixel_small", scale=3)

    scale_tb = 8/7
    font_dot_matrix = ImageFont("fonts\dot_matrix", scale=scale_tb)

    buttons_x = 300

    # instantiating buttons
    TEXT_OFFSET_MENU_BUTTON = (18, 18)
    IMAGES_MENU_BUTTON =  [load_image("menu\\sepha_button\\red_sepha_button.png"), load_image("menu\\sepha_button\\yel_sepha_button.png"), None]
    IMAGES_MENU_TEXTBOX = [load_image("menu\\sepha_button\\red_sepha_button.png"), None, load_image("menu\\sepha_button\\yel_sepha_button.png")]

    menu_objects:dict = {}
    menu_objects.update({"Make Spline" :  Button((buttons_x, 700), IMAGES_MENU_BUTTON,  6,
                                                    text="MAKE SPLINE", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})

    clock = pg.time.Clock()
    t = 0

    while running == True:
        dt = clock.tick(60)
        t += dt

        screen.fill(WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                rail_placer.mouse_button_down_eventhandler(splines)

        rail_placer.draw_hoverspline(screen)

        for spline in splines:
            spline.draw(screen)
        
        if menu_objects.get("Make Spline").draw(screen):
            action.update_action("spline_first_point")
            print("Started creating spline")

        #print("FPS:" + str(1000/dt))
        pg.display.flip()

    return