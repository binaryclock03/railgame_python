import pygame as pg
import sys
from draw_lib import Button, load_image

def run_scene(screen):
    running = True

    # instantiating buttons
    buttons:dict = {}
    buttons_x = 300
    buttons.update({"New Game" :  Button(buttons_x, 340, load_image("menu/new_game_red.png"),  6, image_hover=load_image("menu/new_game_yel.png"))})
    buttons.update({"Load Game" : Button(buttons_x, 440, load_image("menu/load_game_red.png"), 6, image_hover=load_image("menu/load_game_yel.png"))})
    buttons.update({"Settings" :  Button(buttons_x, 540, load_image("menu/settings_red.png"),  6, image_hover=load_image("menu/settings_yel.png"))})
    buttons.update({"Quit" :      Button(buttons_x, 640, load_image("menu/quit_red.png"),      6, image_hover=load_image("menu/quit_yel.png"))})

    title = load_image("menu/Title.png", scale = 4)

    while running:
        # draw background
        screen.fill((110, 130, 140))

        # draw images
        screen.blit(title, (280, 100))

        # drawing buttons
        if buttons.get("New Game").draw(screen):
            print("New Game")
        if buttons.get("Load Game").draw(screen):
            print("Load")
        if buttons.get("Settings").draw(screen):
            print("Settings")
        if buttons.get("Quit").draw(screen):
            sys.exit()

        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("REE")
        
        pg.display.flip()