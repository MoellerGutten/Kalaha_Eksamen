import math

import pygame as pg
from buttonclass import Button, imgButton
from pygame import mixer
import random


pg.init()
mixer.init()

width = 1000
height = 1000

gamewidth = 840
gameheight = 210

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

gameboard_img = pg.image.load("images/Kalaha_cut.png")
gameboard_img = pg.transform.scale(gameboard_img, (1420,353))

button_start = Button(light_grey, width / 2 - 300 / 2, height / 2 - 75 / 2 + offset * 1,300,  75,"start_menu" ,"Start Game")
button_leaderboard = Button(light_grey, width / 2 - 300 / 2, height / 2 - 75 / 2 + offset * 2,300,  75,"start_menu", "Leaderboard")
button_quit = Button(light_grey, width / 2 - 300 / 2, height / 2 - 75 / 2 + offset * 3,300,  75, "start_menu","Quit")
back_button = Button(light_grey, 50,50,200, 50, "game", "Back")
back_button_leaderboard = Button(light_grey, 50, 50, 200, 50, "leaderboard", "Back")

boardbutton1 = Button(light_grey,204, 420, 65,65,"game")
boardbutton2 = Button(light_grey,309, 420, 65,65,"game")
boardbutton3 = Button(light_grey,414, 420, 65,65,"game")
boardbutton4 = Button(light_grey,519, 420, 65,65,"game")
boardbutton5 = Button(light_grey,624, 420, 65,65,"game")
boardbutton6 = Button(light_grey,729, 420, 65,65,"game")
boardbutton7 = Button(light_grey,204, 520, 65,65,"game")
boardbutton8 = Button(light_grey,309, 520, 65,65,"game")
boardbutton9 = Button(light_grey,414, 520, 65,65,"game")
boardbutton10 = Button(light_grey,519, 520, 65,65,"game")
boardbutton11 = Button(light_grey,624, 520, 65,65,"game")
boardbutton12 = Button(light_grey,729, 520, 65,65,"game")

ellipse1_points = []
ellipse1 = pg.Rect(100, 100, 200, 400)
ellipse2_points = []
ellipse2 = pg.Rect(500,100,200,400)


#max_x1 = ellipse1.bottomright[0]- ellipse1.topleft[0] + ellipse1.x
#max_y1 = ellipse1.bottomright[1] - ellipse1.topleft[1]+ ellipse1.y
ellipse_x1 = [int(ellipse1.centerx-(ellipse1.width/2)), int(ellipse1.centerx)]
ellipse_x2 = [int(ellipse2.centerx-(ellipse2.width/2)), int(ellipse2.centerx)]


for i in range(72):
    ball_pos_x1 = random.randrange(ellipse_x1[0], ellipse_x1[1])
    ball_pos_y1 = random.randrange(ellipse1.height)
    ball_pos_x2 = random.randrange(ellipse_x2[0],ellipse_x2[1])
    ball_pos_y2 = random.randrange(ellipse2.height)
    ellipse1_points.append((ball_pos_x1, ball_pos_y1))
    ellipse2_points.append((ball_pos_x2, ball_pos_y2))



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


def generate_ellipse(n):
    pg.draw.ellipse(surface, grey, ellipse1, width=5)
    pg.draw.ellipse(surface, grey, ellipse2, width=5)

    for i in range(n):
        surface.blit(ball, ellipse1_points[i])
        surface.blit(ball, ellipse2_points[i])


def draw_game():
    surface.fill(white)

    global gamestate

    color = (255, 0, 0)

    surface.blit(gameboard_img, (width / 2 - gameboard_img.get_width() / 2, height / 2 - gameboard_img.get_height() / 2))

    debug_rect = pg.Rect(80, 395, 840, 210)
    pg.draw.rect(surface, black, debug_rect, 3)

    for i in range(6):
        button_rect = pg.Rect((gamewidth / 4.1) + i / 8 * gamewidth, height/2 - gameheight / 2+25, 65, 65)
        button = pg.draw.rect(surface, color, button_rect)

    for i in range(6):
        button_rect = pg.Rect((gamewidth / 4.1) + i / 8 * gamewidth, height / 2 - gameheight / 2 + 125, 65, 65)
        button = pg.draw.rect(surface, color, button_rect)

    back_button.draw(surface, 5, outline=black)

    boardbutton1.draw_text("1")

    screen_display.update()


def draw_leaderboard():
    surface.fill(white)

    global gamestate

    font = pg.font.SysFont('arial', 40)
    title = font.render('Leaderboard', True, black)
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2 - offset))

    back_button_leaderboard.draw(surface, 5, outline=black)

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

        if button_start.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "game"

        if back_button.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "start_menu"

        if back_button_leaderboard.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "start_menu"

        if button_leaderboard.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "leaderboard"

        if button_quit.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "quit"

        if boardbutton1.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton2.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton3.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton4.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton5.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton6.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton7.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton8.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton9.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton10.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton11.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")
        if boardbutton12.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                print("test")

    if gamestate == "start_menu":
        draw_start_screen()

    if gamestate == "game":
        draw_game()

    if gamestate == "leaderboard":
        draw_leaderboard()

    if gamestate == "quit":
        window = False

pg.quit()
