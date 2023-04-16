import pygame as pg
import sys
from game.rails.splines import Spline as Spline, SplineNode
from CONSTANTS import WHITE
from game.menuObject import ImageFont, load_image, Button
import numpy as np

def run_scene(screen):
    running = True
    game_paused = False

    action = "none"
    things = {}

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
                if action == "spline_first_point":
                    print("Created first spline point")
                    things.update({"point": pg.mouse.get_pos()})
                    action = "spline_second_point"
                    hover_spline = Spline(node_1=SplineNode(pg.mouse.get_pos()), node_2=SplineNode(pg.mouse.get_pos()))

                elif action == "spline_second_point":
                    print("Created spline")
                    point_temp = pg.mouse.get_pos()

                    hover_spline.node_1.position = np.array(point_temp)

                    if "direction" in things.keys():
                        splines.append(Spline(node_1=SplineNode(things.get("point")), node_2=SplineNode(point_temp), d1=things.get("direction")))
                    else:
                        splines.append(Spline(node_1=SplineNode(things.get("point")), node_2=SplineNode(point_temp)))

                    splines[-1].recalculate()
                    if pg.key.get_mods() & pg.KMOD_SHIFT:
                        action = "spline_second_point"
                        things.update({"point": point_temp})
                        d2 = -splines[-1].get_d2()
                        things.update({"direction": d2})
                    else:
                        action = "none"
                        if "direction" in things.keys():
                            things.pop("direction")
                        things.pop("point")

        if action == "spline_second_point":
            if "direction" in things.keys(): hover_spline.set_d1(things.get("direction"))
            hover_spline.node_2.position = np.array(pg.mouse.get_pos())
            hover_spline.mode = 2
            hover_spline.recalculate()
            hover_spline.draw(screen)

        for spline in splines:
            spline.draw(screen)
        
        if menu_objects.get("Make Spline").draw(screen):
            action = "spline_first_point"
            print("Started creating spline")

        #print("FPS:" + str(1000/dt))
        pg.display.flip()

    return