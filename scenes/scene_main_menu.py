import pygame as pg
import sys
import time
from game.menuObject import Button, TextBox, load_image, ImageFont, mutli_box

def run_scene(screen):
    running = True

    font_pixel = ImageFont("fonts\pixel_small", scale=3)

    scale_tb = 8/7
    font_dot_matrix = ImageFont("fonts\dot_matrix", scale=scale_tb)

    buttons_x = 300

    # instantiating buttons
    main_menu_objects:dict = {}
    TEXT_OFFSET_MENU_BUTTON = (18, 18)
    IMAGES_MENU_BUTTON =  [load_image("menu\\sepha_button\\red_sepha_button.png"), load_image("menu\\sepha_button\\yel_sepha_button.png"), None]
    IMAGES_MENU_TEXTBOX = [load_image("menu\\sepha_button\\red_sepha_button.png"), None, load_image("menu\\sepha_button\\yel_sepha_button.png")]

    main_menu_objects.update({"New Game" :  Button((buttons_x, 340), IMAGES_MENU_BUTTON,  6,
                                                    text="NEW GAME", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})
    main_menu_objects.update({"Load Game" : Button((buttons_x, 440), IMAGES_MENU_BUTTON,  6,
                                                    text="LOAD GAME", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})
    main_menu_objects.update({"Settings" :  Button((buttons_x, 540), IMAGES_MENU_BUTTON,  6,
                                                    text="SETTINGS", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})
    main_menu_objects.update({"Quit" :      Button((buttons_x, 640), IMAGES_MENU_BUTTON,  6,
                                                    text="QUIT", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})

    settings_1_objects:dict = {}
    settings_1_objects.update({"Back" :     Button((buttons_x, 640), IMAGES_MENU_BUTTON, 6,
                                                   text="BACK", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})

    new_game_1_objects:dict = {}
    new_game_1_objects.update({"Generate" : Button((buttons_x, 540), IMAGES_MENU_BUTTON, 6,
                                                   text="GENERATE", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})
    new_game_1_objects.update({"Back" :     Button((buttons_x, 640), IMAGES_MENU_BUTTON, 6,
                                                   text="BACK", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})
    
    tb = mutli_box("menu\\dot_matrix_textbox", (12,1))
    tb_images = [tb, None, None]
    new_game_1_objects.update({"Name TB" :  TextBox((buttons_x, 140), tb_images, scale_tb,
                                                    text="A B A B A B ", text_offset=(7*scale_tb, 7*scale_tb), font=font_dot_matrix)})

    load_game_1_objects:dict = {}
    load_game_1_objects.update({"Back" :    Button((buttons_x, 640), IMAGES_MENU_BUTTON, 6,
                                                    text="BACK", text_offset=TEXT_OFFSET_MENU_BUTTON, font=font_pixel)})

    title = load_image("menu/Title.png", scale = 4)

    # menu state
    menu_state = "main_menu"

    clock = pg.time.Clock()

    while running:
        dt = clock.tick(60)
        # print fps
        #print(1/(dt/1000))
        
        # draw background
        screen.fill((110, 130, 140))
        
        # main menu
        if menu_state == "main_menu":

            # draw title image
            screen.blit(title, (280, 100))

            # draw main menu buttons
            if main_menu_objects.get("New Game").draw(screen):
                menu_state = "new_game_1"
                ##time.sleep(0.1)
            if main_menu_objects.get("Load Game").draw(screen):
                menu_state = "load_game_1"
                ##time.sleep(0.1)
            if main_menu_objects.get("Settings").draw(screen):
                menu_state = "settings_1"
                ##time.sleep(0.1)
            if main_menu_objects.get("Quit").draw(screen):
                sys.exit()
        
        if menu_state == "settings_1":
            if settings_1_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                ##time.sleep(0.1)

        if menu_state == "new_game_1":
            new_game_1_objects.get("Name TB").draw (screen)

            if new_game_1_objects.get("Generate").draw(screen):
                return "generator"
            if new_game_1_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                ##time.sleep(0.1)

        if menu_state == "load_game_1":
            if load_game_1_objects.get("Back").draw(screen):
                menu_state = "main_menu"
                ##time.sleep(0.1)

        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

        pg.display.flip()