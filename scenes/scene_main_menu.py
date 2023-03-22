import pygame as pg
import sys
import time
from draw_lib import Button, TextBox, load_image, ImageFont

def run_scene(screen):
    running = True

    font_pixel = ImageFont("fonts\pixel_small", scale=3)
    font_dot_matrix = ImageFont("fonts\dot_matrix", scale=1)

    buttons_x = 300

    # instantiating buttons
    main_menu_objects:dict = {}
    main_menu_objects.update({"New Game" :  Button(buttons_x, 340, load_image("menu\\red_sepha_button.png"),  6, image_hover=load_image("menu\\yel_sepha_button.png")
                                                   , text="NEW GAME", text_x=18, text_y=18, font=font_pixel)})
    main_menu_objects.update({"Load Game" : Button(buttons_x, 440, load_image("menu\\red_sepha_button.png"),  6, image_hover=load_image("menu\\yel_sepha_button.png")
                                                   , text="LOAD GAME", text_x=18, text_y=18, font=font_pixel)})
    main_menu_objects.update({"Settings" :  Button(buttons_x, 540, load_image("menu\\red_sepha_button.png"),  6, image_hover=load_image("menu\\yel_sepha_button.png")
                                                   , text="SETTINGS", text_x=18, text_y=18, font=font_pixel)})
    main_menu_objects.update({"Quit" :      Button(buttons_x, 640, load_image("menu\\red_sepha_button.png"),  6, image_hover=load_image("menu\\yel_sepha_button.png")
                                                   , text="QUIT", text_x=18, text_y=18, font=font_pixel)})

    settings_1_objects:dict = {}
    settings_1_objects.update({"Back" :     Button(buttons_x, 640, load_image("menu/back_red.png"),      6, image_hover=load_image("menu/back_yel.png"))})

    new_game_1_objects:dict = {}
    new_game_1_objects.update({"Generate" : Button(buttons_x, 540, load_image("menu/generate_red.png"),  6, image_hover=load_image("menu/generate_yel.png"))})
    new_game_1_objects.update({"Back" :     Button(buttons_x, 640, load_image("menu/back_red.png"),      6, image_hover=load_image("menu/back_yel.png"))})
    new_game_1_objects.update({"Name TB" :  TextBox(buttons_x, 140, load_image("menu/name_tb.png"),      6)})

    load_game_1_objects:dict = {}
    load_game_1_objects.update({"Back" :    Button(buttons_x, 640, load_image("menu/back_red.png"),      6, image_hover=load_image("menu/back_yel.png"))})



    title = load_image("menu/Title.png", scale = 4)

    # menu state
    menu_state = "main_menu"

    while running:
        # draw background
        screen.fill((110, 130, 140))
        
        # main menu
        if menu_state == "main_menu":

            # draw title image
            screen.blit(title, (280, 100))

            # draw main menu buttons
            if main_menu_objects.get("New Game").draw(screen):
                menu_state = "new_game_1"
                time.sleep(0.1)
            if main_menu_objects.get("Load Game").draw(screen):
                menu_state = "load_game_1"
                time.sleep(0.1)
            if main_menu_objects.get("Settings").draw(screen):
                menu_state = "settings_1"
                time.sleep(0.1)
            if main_menu_objects.get("Quit").draw(screen):
                sys.exit()
        
        if menu_state == "settings_1":
            if settings_1_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                time.sleep(0.1)

        if menu_state == "new_game_1":
            new_game_1_objects.get("Name TB").draw (screen)

            if new_game_1_objects.get("Generate").draw(screen):
                pass
            if new_game_1_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                time.sleep(0.1)

        if menu_state == "load_game_1":
            if load_game_1_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                time.sleep(0.1)

        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("REE")
        
        pg.display.flip()