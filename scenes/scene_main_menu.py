import pygame as pg
import sys
import time
from draw_lib import Button, TextBox, load_image

def run_scene(screen):
    running = True

    buttons_x = 300

    # instantiating buttons
    main_menu_buttons:dict = {}
    main_menu_buttons.update({"New Game" :  Button(buttons_x, 340, load_image("menu/new_game_red.png"),  6, image_hover=load_image("menu/new_game_yel.png"))})
    main_menu_buttons.update({"Load Game" : Button(buttons_x, 440, load_image("menu/load_game_red.png"), 6, image_hover=load_image("menu/load_game_yel.png"))})
    main_menu_buttons.update({"Settings" :  Button(buttons_x, 540, load_image("menu/settings_red.png"),  6, image_hover=load_image("menu/settings_yel.png"))})
    main_menu_buttons.update({"Quit" :      Button(buttons_x, 640, load_image("menu/quit_red.png"),      6, image_hover=load_image("menu/quit_yel.png"))})

    settings_1_buttons:dict = {}
    settings_1_buttons.update({"Back" :     Button(buttons_x, 640, load_image("menu/back_red.png"),      6, image_hover=load_image("menu/back_yel.png"))})

    new_game_1_menu_objects:dict = {}
    new_game_1_menu_objects.update({"Generate" : Button(buttons_x, 540, load_image("menu/generate_red.png"),  6, image_hover=load_image("menu/generate_yel.png"))})
    new_game_1_menu_objects.update({"Back" :     Button(buttons_x, 640, load_image("menu/back_red.png"),      6, image_hover=load_image("menu/back_yel.png"))})
    new_game_1_menu_objects.update({"Name TB" :  TextBox(buttons_x, 140, load_image("menu/name_tb.png"),      6)})

    load_game_1_buttons:dict = {}
    load_game_1_buttons.update({"Back" :    Button(buttons_x, 640, load_image("menu/back_red.png"),      6, image_hover=load_image("menu/back_yel.png"))})



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
            if main_menu_buttons.get("New Game").draw(screen):
                menu_state = "new_game_1"
                time.sleep(0.1)
            if main_menu_buttons.get("Load Game").draw(screen):
                menu_state = "load_game_1"
                time.sleep(0.1)
            if main_menu_buttons.get("Settings").draw(screen):
                menu_state = "settings_1"
                time.sleep(0.1)
            if main_menu_buttons.get("Quit").draw(screen):
                sys.exit()
        
        if menu_state == "settings_1":
            if settings_1_buttons.get("Back").draw(screen):
                menu_state = "main_menu"
                time.sleep(0.1)

        if menu_state == "new_game_1":
            new_game_1_menu_objects.get("Name TB").draw (screen)

            if new_game_1_menu_objects.get("Generate").draw(screen):
                pass
            if new_game_1_menu_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                time.sleep(0.1)

        if menu_state == "load_game_1":
            if load_game_1_buttons.get("Back").draw(screen):
                menu_state = "main_menu"
                time.sleep(0.1)

        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("REE")
        
        pg.display.flip()