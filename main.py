import math

import sqlite3 as lite

import time

import kalaha

import pygame as pg
from buttonclass import Button
from pygame import mixer
import random
from datetime import date

pg.init()
mixer.init()

WIDTH = 1000
HEIGHT = 800

PI = math.pi

RES = [WIDTH, HEIGHT]


def center_width(obj_width):
    return WIDTH / 2 - obj_width / 2


def center_height(obj_height):
    return HEIGHT / 2 - obj_height / 2


WHITE = (255, 255, 255)
black = (0,0,0)
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

window = True
game_board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
game_engine = kalaha.kalaha(game_board)
isplayer1 = True
isbot = False

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 75


button_start = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 425, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Start Game")
button_leaderboard = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 500, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Leaderboard")
button_quit = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 575, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Quit")
button_choice_player = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 275, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Mod spiller")
button_choice_bot = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 350, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Mod bot")
back_button = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "game", "Tilbage")
back_button_leaderboard = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "leaderboard", "Tilbage")
back_button_choice = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Tilbage")

boardbutton_list = []

for i in range(6):
    #(globals()['boardbutton%s' % (i+1)] =  Button(LIGHT_GREY, 204 + i * 105, 320, 65, 65, "game", ""))
    boardbutton_list.append(Button(LIGHT_GREY, 204 + i * 105, 320, 65, 65, "game", ""))
for i in range(6):
    #globals()['boardbutton%s' % (i+7)] =  Button(LIGHT_GREY, 204 + i * 105, 420, 65, 65, "game", "")
    boardbutton_list.append(Button(LIGHT_GREY, 204 + i * 105, 420, 65, 65, "game", ""))



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

def update_database(stilling1, stilling2, resultat):
    tidspunkt = date.today()
    stilling = str(stilling1) + " - " + str(stilling2)
    con = None
    con = lite.connect("leaderboard.db")
    cur = con.cursor()
    cur.execute("INSERT INTO leaderbord(stilling, resultat, tidspunkt) VALUES('" + str(stilling) + "','" + str(resultat) + "', '" + str(tidspunkt) + "')")
    con.commit()
    con.close()


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
    surface.blit(title, (center_width(title.get_width()), center_height(title.get_height()) + OFFSET * -3))

    back_button_choice.draw(surface, 5, outline=BLACK)

    button_choice_player.draw(surface, 5, outline=BLACK)
    button_choice_bot.draw(surface, 5, outline=BLACK)

    pg.display.update()


def draw_game(engine, player_status, bot_move):
    surface.fill(WHITE)

    global gamestate

    surface.blit(gameboard_img, (center_width(gameboard_img.get_width()), center_height(gameboard_img.get_height())))

    back_button.draw(surface, 5, outline=BLACK)

    font = pg.font.SysFont('arial', 40)
    if player_status:
        title = font.render('Player 1', True, BLACK)
    else:
        title = font.render('Player 2', True, BLACK)
    surface.blit(title, (center_width(title.get_width()), center_height(title.get_height()) - 2 * OFFSET))


    font = pg.font.SysFont('arial', 40)
    title = font.render(f'Bot moved: {bot_move}', True, BLACK)
    surface.blit(title, (center_width(title.get_width()), center_height(title.get_height()) - 3 * OFFSET))

    update_board(engine)

    screen_display.update()


def draw_leaderboard():
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 40)

    title = font.render('Leaderboard', True, BLACK)


    back_button_leaderboard.draw(surface, 5, outline=BLACK)

    con = None
    con = lite.connect("leaderboard.db")
    cur = con.cursor()

    i = 35
    column_space = 250

    head1 = font.render(f'Resultat', True, black)
    head2 = font.render(f'Stilling', True, black)
    head4 = font.render(f'Dato', True, black)
    surface.blit(head1, [WIDTH / 6, (700 / 4) + 5])
    surface.blit(head2, [WIDTH / 6 + column_space, (700 / 4) + 5])
    surface.blit(head4, [WIDTH / 6 + 2 * column_space, (700 / 4) + 5])



    cur.execute('SELECT * FROM leaderbord')
    rows = cur.fetchall()
    for row in rows:
        column1 = font.render('{:>5}'.format(str(row[2])), True, black)
        column2 = font.render('{:30}'.format(str(row[1])), True, black)
        column3 = font.render('{:60}'.format(row[3]), True, black)
        surface.blit(column1, [WIDTH / 6, (700 / 4) + i + 5])
        surface.blit(column2, [WIDTH / 6 + column_space, (700 / 4) + i + 5])
        surface.blit(column3, [WIDTH / 6 + 2*column_space, (700 / 4) + i + 5])

        i += 40
    con.close()

    pg.display.update()


def draw_start_screen():
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render('Kalaha', True, BLACK)
    surface.blit(title, (center_width(title.get_width()), center_height(title.get_height()) - OFFSET))

    button_start.draw(surface, 5, outline=BLACK)

    button_leaderboard.draw(surface, 5, outline=BLACK)

    button_quit.draw(surface, 5, outline=BLACK)

    pg.display.update()


def draw_victory_screen(who_won, stilling1, stilling2):
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render(who_won, True, BLACK)
    surface.blit(title, (center_width(title.get_width()), center_height(title.get_height()) - OFFSET))

    update_database(stilling1, stilling2, who_won)

    back_button.draw(surface, 5, outline=BLACK)

    pg.display.update()
"""
def gameclick(i):

    global isplayer1
    global isbot

    if i <= 5:
        if boardbutton_list[i].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(i, False)
    if i >= 6:
        if boardbutton_list[i].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    empty, isplayer1 = game_engine.move(18-i, False)
"""
def update_board(engine):
    for i in range(12):
        if i <= 5:
            generate(engine.board[i], boardbutton_list[i].get_x_pos(), boardbutton_list[i].get_y_pos())
        elif i >= 6:
            generate(engine.board[18 - i], boardbutton_list[i].get_x_pos(), boardbutton_list[i].get_y_pos())

    generate_score_left(engine.board[13])
    generate_score_right(engine.board[6])


    for i in range(12):
        if i <= 5:
            boardbutton_list[i].draw_text(str(engine.board[i]))
        elif i >= 6:
            boardbutton_list[i].draw_text(str(engine.board[18 - i]))


    Scoreleftbutton.draw_text(str(engine.board[13]))
    Scorerightbutton.draw_text(str(engine.board[6]))


def update_move(oldboard, newboard, engine):
    correct_button_list = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0, 13: 0, 12: 7, 11: 8, 10: 9, 9: 10, 8: 11, 7: 12}
    update_list = []
    updated_board = []
    starting_point = None
    y = 0
    i = 0
    for element in oldboard:
        new_value =  newboard[y] - element
        updated_board.append(new_value)
        y += 1
    for element in updated_board:
        if element > 0:
            update_list.append(i)
        elif element < 0:
            update_list.append(i)
            starting_point = i
        i += 1
    starting_point = update_list.index(starting_point)
    z = starting_point
    for __ in range(len(update_list)):
        x = f"boardbutton_list[{correct_button_list[update_list[z]]-1}]"
        num = update_list[z]
        if num == 6:
            Scorerightbutton.draw_text(str(engine.board[6]))
        elif num == 13:
            Scoreleftbutton.draw_text(str(engine.board[13]))
        else:
            eval(x).draw_text(str(engine.board[num]))
        pg.display.update()
        sound()
        pg.time.delay(250)
        z -= 1


clock = pg.time.Clock()


window = True
game_board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
gameBoard = []
for element in game_board:
    gameBoard.append(element)

game_engine = kalaha.kalaha(game_board)
isplayer1 = True
isbot = False
bot_move = None

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
        
        if boardbutton_list[0].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    __, isplayer1 = game_engine.move(0, False)
        if boardbutton_list[1].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    __, isplayer1 = game_engine.move(1, False)
        if boardbutton_list[2].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    __, isplayer1 = game_engine.move(2, False)
        if boardbutton_list[3].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    __, isplayer1 = game_engine.move(3, False)
        if boardbutton_list[4].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    __, isplayer1 = game_engine.move(4, False)
        if boardbutton_list[5].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if not isplayer1 and not isbot:
                    __, isplayer1 = game_engine.move(5, False)
        if boardbutton_list[6].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    __, isplayer1 = game_engine.move(12, True)
        if boardbutton_list[7].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    __, isplayer1 = game_engine.move(11, True)
        if boardbutton_list[8].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    __, isplayer1 = game_engine.move(10, True)
        if boardbutton_list[9].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    __, isplayer1 = game_engine.move(9, True)
        if boardbutton_list[10].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                if isplayer1:
                    __, isplayer1 = game_engine.move(8, True)
        if boardbutton_list[11].isOver(gamestate):
            if event.type == pg.MOUSEBUTTONUP:
                sound()
                if isplayer1:
                    __, isplayer1 = game_engine.move(7, True)

    if gameBoard != game_engine.board:
        update_move(gameBoard, game_engine.board, game_engine)
        gameBoard = []
        for element in game_engine.board:
            gameBoard.append(element)
        update_board(game_engine)

    if gamestate == "game":
        draw_game(game_engine, isplayer1, bot_move)


    if game_engine.check_win()[0]:
        gamestate = "victory"

    if gamestate == "victory":
        draw_victory_screen(game_engine.check_win()[1],game_engine.board[6], game_engine.board[13])
        time.sleep(5)
        gamestate = "start_menu"
        game_engine.board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        isplayer1 = True

    if gamestate == "start_menu":
        draw_start_screen()

    if gamestate == "leaderboard":
        draw_leaderboard()

    if gamestate == "choice":
        draw_game_choice()

    if gamestate == "quit":
        window = False

    if isbot and not isplayer1:
        bot_move, isplayer1 = game_engine.bot_move()

pg.quit()
