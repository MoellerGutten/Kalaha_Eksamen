import math
import time

import kalaha

import pygame as pg
from buttonclass import Button, imgButton
from pygame import mixer
import random

pg.init()
mixer.init()

WIDTH = 1000
HEIGHT = 800

PI = math.pi

RES = [WIDTH, HEIGHT]

WHITE = (255, 255, 255)
LIGHT_GREY = (197, 197, 197)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

OFFSET = 80

screen_display = pg.display

window_icon = pg.image.load("images/window_icon.png")

pg.display.set_caption("Kalaha")
pg.display.set_icon(window_icon)

surface = screen_display.set_mode(RES)

ball = pg.image.load("images/Kalaha_Kugle.png")
ball = pg.transform.scale(ball, (25, 25))

gamestate = "start_menu"

gameboard_img = pg.image.load("images/Kalaha_cut.png")
gameboard_img = pg.transform.scale(gameboard_img, (1420, 353))

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 75

BUTTON_MIDDLE_X = WIDTH / 2 - BUTTON_WIDTH / 2


button_start = Button(LIGHT_GREY, BUTTON_MIDDLE_X, 425, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Start Game")
button_leaderboard = Button(LIGHT_GREY, BUTTON_MIDDLE_X, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Leaderboard")
button_quit = Button(LIGHT_GREY, BUTTON_MIDDLE_X, 575, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Quit")
button_choice_player = Button(LIGHT_GREY, BUTTON_MIDDLE_X, 275, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Mod spiller")
button_choice_bot = Button(LIGHT_GREY, BUTTON_MIDDLE_X, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Mod bot")
back_button = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "game", "Tilbage")
back_button_leaderboard = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "leaderboard", "Tilbage")
back_button_choice = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Tilbage")

boardbutton1 = Button(LIGHT_GREY, 204, 320, 65, 65, "game", "")
boardbutton2 = Button(LIGHT_GREY, 309, 320, 65, 65, "game", "")
boardbutton3 = Button(LIGHT_GREY, 414, 320, 65, 65, "game", "")
boardbutton4 = Button(LIGHT_GREY, 519, 320, 65, 65, "game", "")
boardbutton5 = Button(LIGHT_GREY, 624, 320, 65, 65, "game", "")
boardbutton6 = Button(LIGHT_GREY, 729, 320, 65, 65, "game", "")
boardbutton7 = Button(LIGHT_GREY, 204, 420, 65, 65, "game", "")
boardbutton8 = Button(LIGHT_GREY, 309, 420, 65, 65, "game", "")
boardbutton9 = Button(LIGHT_GREY, 414, 420, 65, 65, "game", "")
boardbutton10 = Button(LIGHT_GREY, 519, 420, 65, 65, "game", "")
boardbutton11 = Button(LIGHT_GREY, 624, 420, 65, 65, "game", "")
boardbutton12 = Button(LIGHT_GREY, 729, 420, 65, 65, "game", "")
Scoreleftbutton = Button(LIGHT_GREY, 90, 320, 90, 170, "game", "")
Scorerightbutton = Button(LIGHT_GREY, 820, 320, 90, 170, "game", "")

ellipse1_points = []
ellipse1 = pg.Rect(90,320,90,170)
ellipse2_points = []
ellipse2 = pg.Rect(820,320,90,170)

ellipse_x1 = [int(ellipse1.centerx-(ellipse1.width/2)), int(ellipse1.centerx)]
ellipse_x2 = [int(ellipse2.centerx-(ellipse2.width/2)), int(ellipse2.centerx)]


for i in range(72):
    ball_pos_x1 = random.randrange(ellipse_x1[0], ellipse_x1[1])
    ball_pos_y1 = random.randrange(ellipse1.y, ellipse1.y + ellipse1.height)
    ball_pos_x2 = random.randrange(ellipse_x2[0], ellipse_x2[1])
    ball_pos_y2 = random.randrange(ellipse2.y, ellipse2.y + ellipse2.height)
    ellipse1_points.append((ball_pos_x1, ball_pos_y1))
    ellipse2_points.append((ball_pos_x2, ball_pos_y2))


def sound():
    sounds = ['sound/sound1.mp3', 'sound/sound2.mp3', 'sound/sound3.mp3']
    randomvalue = random.randint(0, 2)
    mixer.music.load(sounds[randomvalue])
    mixer.music.set_volume(0.5)
    mixer.music.play()


def generate(n, button_x, button_y):
    ball_x = ball.get_size()[0]
    ball_y = ball.get_size()[1]

    pos_x = (button_x + ball_x)
    pos_y = (button_y + ball_y)
    if n == 1:
        surface.blit(ball, (pos_x, pos_y))
    if n > 1:
        points1 = []
        points2 = []

        for i in range(n):
            if n < 6:
                angle = i * (2 * PI / (n - 1)) - random.randrange(1, 2)
                x = math.cos(angle) * ball_x + pos_x
                y = math.sin(angle) * ball_x + pos_y
                points1.append((x, y))
                surface.blit(ball, points1[i])
                if i == 5:
                    break
            else:
                angle = i * (2 * PI / (6 - 1)) - random.randrange(1, 2)
                x = math.cos(angle) * ball_x + pos_x
                y = math.sin(angle) * ball_x + pos_y
                points1.append((x, y))
                surface.blit(ball, points1[i])
        if n > 6:
            for i in range(n):
                angle = i * (2 * PI / (n - 6)) - random.randrange(1, 2)
                x = math.cos(angle) * ball_x * 1.5 + pos_x
                y = math.sin(angle) * ball_x * 1.5 + pos_y
                points2.append((x, y))
                surface.blit(ball, points2[i])
        surface.blit(ball, (pos_x, pos_y))


def generate_score_left(n):
    for i in range(n):
        surface.blit(ball, ellipse1_points[i])


def generate_score_right(n):
    for i in range(n):
        surface.blit(ball, ellipse2_points[i])


def draw_game_choice():
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 40)
    title = font.render('Vælg i mellem:', True, BLACK)
    surface.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2 + OFFSET * -3))

    back_button_choice.draw(surface, 5, outline=BLACK)

    button_choice_player.draw(surface, 5, outline=BLACK)
    button_choice_bot.draw(surface, 5, outline=BLACK)

    pg.display.update()


def draw_game(engine, player_status):
    surface.fill(WHITE)

    global gamestate

    surface.blit(gameboard_img, (WIDTH / 2 - gameboard_img.get_width() / 2, HEIGHT / 2 - gameboard_img.get_height() / 2))

    back_button.draw(surface, 5, outline=BLACK)

    font = pg.font.SysFont('arial', 40)
    if player_status:
        title = font.render('Player 1', True, BLACK)
    else:
        title = font.render('Player 2', True, BLACK)
    surface.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 3 - title.get_height() / 2 - OFFSET))

    update_board(engine)

    screen_display.update()


def draw_leaderboard():
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 40)
    title = font.render('Leaderboard', True, BLACK)
    surface.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2 - OFFSET))

    back_button_leaderboard.draw(surface, 5, outline=BLACK)

    pg.display.update()


def draw_start_screen():
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render('Kalaha', True, BLACK)
    surface.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 3 - title.get_height() / 2 - OFFSET))

    button_start.draw(surface, 5, outline=BLACK)

    button_leaderboard.draw(surface, 5, outline=BLACK)

    button_quit.draw(surface, 5, outline=BLACK)

    pg.display.update()


def draw_victory_screen(who_won):
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render(who_won, True, BLACK)
    surface.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2 - OFFSET))

    back_button.draw(surface, 5, outline=BLACK)

    pg.display.update()


def update_board(engine):
    generate(engine.board[0], boardbutton1.get_x_pos(), boardbutton1.get_y_pos())
    generate(engine.board[1], boardbutton2.get_x_pos(), boardbutton2.get_y_pos())
    generate(engine.board[2], boardbutton3.get_x_pos(), boardbutton3.get_y_pos())
    generate(engine.board[3], boardbutton4.get_x_pos(), boardbutton4.get_y_pos())
    generate(engine.board[4], boardbutton5.get_x_pos(), boardbutton5.get_y_pos())
    generate(engine.board[5], boardbutton6.get_x_pos(), boardbutton6.get_y_pos())
    generate(engine.board[12], boardbutton7.get_x_pos(), boardbutton7.get_y_pos())
    generate(engine.board[11], boardbutton8.get_x_pos(), boardbutton8.get_y_pos())
    generate(engine.board[10], boardbutton9.get_x_pos(), boardbutton9.get_y_pos())
    generate(engine.board[9], boardbutton10.get_x_pos(), boardbutton10.get_y_pos())
    generate(engine.board[8], boardbutton11.get_x_pos(), boardbutton11.get_y_pos())
    generate(engine.board[7], boardbutton12.get_x_pos(), boardbutton12.get_y_pos())

    generate_score_left(engine.board[13])
    generate_score_right(engine.board[6])

    boardbutton1.draw_text(str(engine.board[0]))
    boardbutton2.draw_text(str(engine.board[1]))
    boardbutton3.draw_text(str(engine.board[2]))
    boardbutton4.draw_text(str(engine.board[3]))
    boardbutton5.draw_text(str(engine.board[4]))
    boardbutton6.draw_text(str(engine.board[5]))
    boardbutton7.draw_text(str(engine.board[12]))
    boardbutton8.draw_text(str(engine.board[11]))
    boardbutton9.draw_text(str(engine.board[10]))
    boardbutton10.draw_text(str(engine.board[9]))
    boardbutton11.draw_text(str(engine.board[8]))
    boardbutton12.draw_text(str(engine.board[7]))

    Scoreleftbutton.draw_text(str(engine.board[13]))
    Scorerightbutton.draw_text(str(engine.board[6]))


clock = pg.time.Clock()


window = True
game_board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
game_engine = kalaha.kalaha(game_board)
isplayer1 = True
isbot = False
while window:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            window = False
        if button_start.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "choice"
        if back_button.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "start_menu"
        if back_button_leaderboard.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "start_menu"
        if button_leaderboard.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "leaderboard"
        if back_button_choice.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "start_menu"
        if button_choice_player.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "game"
        if button_choice_bot.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "game"
                isbot = True
        if button_quit.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                gamestate = "quit"
        if boardbutton1.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(0, False)
        if boardbutton2.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(1, False)
        if boardbutton3.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(2, False)
        if boardbutton4.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(3, False)
        if boardbutton5.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(4, False)
        if boardbutton6.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(5, False)
        if boardbutton7.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    empty, isplayer1 = game_engine.move(12, True)
        if boardbutton8.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    empty, isplayer1 = game_engine.move(11, True)
        if boardbutton9.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    empty, isplayer1 = game_engine.move(10, True)
        if boardbutton10.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    empty, isplayer1 = game_engine.move(9, True)
        if boardbutton11.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    empty, isplayer1 = game_engine.move(8, True)
        if boardbutton12.isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                sound()
                if isplayer1:
                    empty, isplayer1 = game_engine.move(7, True)
    if isbot and not isplayer1:
        empty, isplayer1 = game_engine.bot_move()

    if game_engine.check_win()[0]:
        gamestate = "victory"

    if gamestate == "victory":
        draw_victory_screen(game_engine.check_win()[1])
        time.sleep(5)
        gamestate = "start_menu"
        game_engine.board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        isplayer1 = True

    if gamestate == "start_menu":
        draw_start_screen()

    if gamestate == "game":
        draw_game(game_engine, isplayer1)

    if gamestate == "leaderboard":
        draw_leaderboard()

    if gamestate == "choice":
        draw_game_choice()

    if gamestate == "quit":
        window = False

pg.quit()
