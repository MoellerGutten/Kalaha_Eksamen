import math

import pygame as pg
from buttonclass import Button, backButton, imgButton
from pygame import mixer
import random


pg.init()
mixer.init()

width = 1000
height = 1000

gamewidth = 520
gameheight = 600

pi = math.pi

res = [width, height]

white = (255, 255, 255)
light_grey = (197, 197, 197)
grey = (100, 100, 100)
black = (0, 0, 0)

offset = 100

screen_display = pg.display

window_icon = pg.image.load("images/window_icon.png")

pg.display.set_caption("Kalaha")
pg.display.set_icon(window_icon)

surface = screen_display.set_mode(res)

ball = pg.image.load("images/Kalaha_Kugle.png")

gamestate = "start_menu"


img_button = imgButton("images/Kalaha_cut.png", 0, 440)


button_start = Button(light_grey, 300,  75, 0, "Start Game")
back_button = backButton(light_grey, 50, 50, 200, 50, 0, "Back")
button_leaderboard = Button(light_grey, 300, 75, 1, "Leaderboard")
button_quit = Button(light_grey, 300, 75, 2, "Quit")


def sound():
    print('hello')
    sounds = ['sound/sound1.mp3','sound/sound2.mp3','sound/sound3.mp3']
    i = random.randint(0,2)
    mixer.music.load(sounds[i])
    mixer.music.set_volume(0.5)
    mixer.music.play()




def generate(n):
    ball_x = ball.get_size()[0]
    ball_y = ball.get_size()[1]

    pos_x = (res[0] - ball_x) / 2
    pos_y = (res[1] - ball_y) / 2

    if n > 1:
        points1 = []
        points2 = []

        for i in range(n):
            if n < 6:
                angle = i * (2 * pi / (n - 1))
                x = math.cos(angle) * ball_x + pos_x
                y = math.sin(angle) * ball_x + pos_y
                points1.append((x, y))
                surface.blit(ball, points1[i])
                if i == 5:
                    break
            else:
                angle = i * (2 * pi / (6 - 1))
                x = math.cos(angle) * ball_x + pos_x
                y = math.sin(angle) * ball_x + pos_y
                points1.append((x, y))
                surface.blit(ball, points1[i])
        if n > 6:
            for i in range(n):
                angle = i * (2 * pi / (n - 6))
                x = math.cos(angle) * ball_x * 2 + pos_x
                y = math.sin(angle) * ball_x * 2 + pos_y
                points2.append((x, y))
                surface.blit(ball, points2[i])

    surface.blit(ball, (pos_x, pos_y))


def draw_game():
    surface.fill(white)

    global gamestate

    img_button.draw()

    color = (255, 0, 0)

    for i in range(8):
        pg.draw.rect(surface, color,
                     pg.Rect((gamewidth / 2) + i / 7 * gamewidth-26, height - (height - gameheight / 2), 40, 120))

    for i in range(8):
        pg.draw.rect(surface, color,
                     pg.Rect((gamewidth / 2) + i / 7 * gamewidth-26, height - (height - gameheight / 2)+400, 40, 120))

    if img_button.isOver():
        if event.type == pg.MOUSEBUTTONUP:
            img_button.move_button()

    back_button.draw(surface, 5, outline=black)

    screen_display.update()


def draw_leaderboard():
    surface.fill(white)

    global gamestate

    font = pg.font.SysFont('arial', 40)
    title = font.render('Leaderboard', True, black)
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2 - offset))

    back_button.draw(surface, 5, outline=black)

    pg.display.update()


def draw_start_screen():
    surface.fill(white)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render('Kalaha', True, black)
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2 - offset))

    button_start.draw(surface, 5, outline=black)

    button_leaderboard.draw(surface, 5, outline=black)

    button_quit.draw(surface, 5, outline=black)

    pg.display.update()


clock = pg.time.Clock()


window = True
while window:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            window = False

        if button_start.isOver():
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "game"

        if back_button.isOver():
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "start_menu"

        if button_leaderboard.isOver():
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "leaderboard"

        if button_quit.isOver():
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "quit"


    if gamestate == "start_menu":
        draw_start_screen()

    if gamestate == "game":
        draw_game()

    if gamestate == "leaderboard":
        draw_leaderboard()

    if gamestate == "quit":
        window = False

clock.tick(120)

pg.quit()
