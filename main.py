import pygame as pg
import math
from buttonclass import *

pg.init()

width = 1000
height = 1000

pi = math.pi

res = [width, height]

white = (255, 255, 255)
light_grey = (197, 197, 197)
grey = (100, 100, 100)
black = (0, 0, 0)

offset = 100

screen_display = pg.display

window_icon = pg.image.load("window_icon.png")

pg.display.set_caption("Kalaha",)
pg.display.set_icon(window_icon)

surface = screen_display.set_mode(res)

ball = pg.image.load("Kalaha_Kugle.png")

gamestate = "start_menu"


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

    generate(7)

    back_button = backButton(light_grey, 50, 50, 200, 50, 0, "Back")
    back_button.draw(surface, 5, outline=black)
    back_button.isOver()
    if back_button.isClicked():
        gamestate = "start_menu"

    screen_display.update()


def draw_leaderboard():
    surface.fill(white)

    global gamestate

    font = pg.font.SysFont('arial', 40)
    title = font.render('Leaderboard', True, black)
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2 - offset))

    back_button = backButton(light_grey,50,50, 200,  50, 0, "Back")
    back_button.draw(surface,5,outline=black)
    back_button.isOver()
    if back_button.isClicked():
        gamestate = "start_menu"

    pg.display.update()


def draw_start_screen():
    surface.fill(white)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render('Kalaha', True, black)
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2 - offset))

    button_start = Button(light_grey, 300,  75, 0, "Start Game")
    button_start.draw(surface, 5, outline=black)
    button_start.isOver()
    if button_start.isClicked():
        gamestate = "game"

    button_leaderboard = Button(light_grey, 300, 75, 1, "Leaderboard")
    button_leaderboard.draw(surface, 5, outline=black)
    button_leaderboard.isOver()
    if button_leaderboard.isClicked():
        gamestate = "leaderboard"

    button_quit = Button(light_grey, 300, 75, 2, "Quit")
    button_quit.draw(surface, 5, outline=black)
    button_quit.isOver()
    if button_quit.isClicked():
        gamestate = "quit"

    pg.display.update()


window = True
while window:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            window = False
    if gamestate == "start_menu":
        draw_start_screen()
    if gamestate == "game":
        draw_game()
    if gamestate == "leaderboard":
        draw_leaderboard()
    if gamestate == "quit":
        window = False


pg.quit()
