import pygame as pg
import sys
from draw_lib import Button, load_image

def run_scene(screen):
    running = True

    # instantiating buttons
    buttons:dict = {}
    buttons_x = 300
    buttons.update({"New Game" : Button(buttons_x, 340, load_image("new_game_red.png"), 6)})
    buttons.update({"Load Game" : Button(buttons_x, 440, load_image("load_game_red.png"), 6, image_hover=load_image("load_game_yel.png"))})
    buttons.update({"Settings" : Button(buttons_x, 540, load_image("settings_red.png"), 6)})
    #buttons.update({"Quit Game" : Button(buttons_x, 160, load_image("Quit_Game.png"), 8)})

    title = load_image("Title.png", scale = 4)

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


        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("REE")
        
        pg.display.flip()