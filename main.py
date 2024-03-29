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

# For placing different objects and to reduce code
def center_width(obj_width):
    return WIDTH / 2 - obj_width / 2


def center_height(obj_height):
    return HEIGHT / 2 - obj_height / 2


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

# Fits the board to the screen
gameboard_img = pg.image.load("images/Kalaha_cut.png")
gameboard_img = pg.transform.scale(gameboard_img, (1420, 353))

# Standard size for all buttons
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 75

# Initializes all button objects
button_start = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 425, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Start Game")
button_leaderboard = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 500, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Leaderboard")
button_quit = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 575, BUTTON_WIDTH, BUTTON_HEIGHT, "start_menu", "Quit")
button_choice_player = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 275, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Mod spiller")
button_choice_bot = Button(LIGHT_GREY, center_width(BUTTON_WIDTH), 350, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Mod bot")
back_button = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "game", "Tilbage")
back_button_leaderboard = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "leaderboard", "Tilbage")
back_button_choice = Button(LIGHT_GREY, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "choice", "Tilbage")

# Initializes the invisible buttons on the game board in a list
boardbutton_list = []
for i in range(6):
    boardbutton_list.append(Button(LIGHT_GREY, 204 + i * 105, 320, 65, 65, "game", ""))
for i in range(6):
    boardbutton_list.append(Button(LIGHT_GREY, 204 + i * 105, 420, 65, 65, "game", ""))

# Initializes seperately due to different dimensions
Scoreleftbutton = Button(LIGHT_GREY, 90, 320, 90, 170, "game", "")
Scorerightbutton = Button(LIGHT_GREY, 820, 320, 90, 170, "game", "")

# Generates random points for the left and right scores
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
    # Gets size of ball img
    ball_x = ball.get_size()[0]
    ball_y = ball.get_size()[1]

    # Gets middle of button and ball
    pos_x = (button_x + ball_x)
    pos_y = (button_y + ball_y)

    # if it only needs to generate a single ball, it generates in the middle of button
    if n == 1:
        surface.blit(ball, (pos_x, pos_y))

    if n > 1:
        points1 = []
        points2 = []
        for i in range(n):
            # The first 6 balls are in an inner circle
            if n < 6:
                # Splits the angle evenly among the circle
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
        # Generates the rest of the balls in an outer circle
        if n > 6:
            for i in range(n):
                angle = i * (2 * PI / (n - 6)) - random.randrange(1, 2)
                x = math.cos(angle) * ball_x * 1.5 + pos_x
                y = math.sin(angle) * ball_x * 1.5 + pos_y
                points2.append((x, y))
                surface.blit(ball, points2[i])
        surface.blit(ball, (pos_x, pos_y))

# Generates the balls generated above in the left score
def generate_score_left(n):
    for i in range(n):
        surface.blit(ball, ellipse1_points[i])

# Generates the balls generated above in the right score
def generate_score_right(n):
    for i in range(n):
        surface.blit(ball, ellipse2_points[i])

# Draws screen with buttons to choose opponent
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

# Main game screen
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

# Draws leaderboard with data from database
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

    head1 = font.render(f'Resultat', True, BLACK)
    head2 = font.render(f'Stilling', True, BLACK)
    head4 = font.render(f'Dato', True, BLACK)
    surface.blit(head1, [WIDTH / 6, (700 / 4) + 5])
    surface.blit(head2, [WIDTH / 6 + column_space, (700 / 4) + 5])
    surface.blit(head4, [WIDTH / 6 + 2 * column_space, (700 / 4) + 5])



    cur.execute('SELECT * FROM leaderbord')
    rows = cur.fetchall()
    for row in rows:
        column1 = font.render('{:>5}'.format(str(row[2])), True, BLACK)
        column2 = font.render('{:30}'.format(str(row[1])), True, BLACK)
        column3 = font.render('{:60}'.format(row[3]), True, BLACK)
        surface.blit(column1, [WIDTH / 6, (700 / 4) + i + 5])
        surface.blit(column2, [WIDTH / 6 + column_space, (700 / 4) + i + 5])
        surface.blit(column3, [WIDTH / 6 + 2*column_space, (700 / 4) + i + 5])

        i += 40
    con.close()

    pg.display.update()

# The start screen where you can navigate to either game or leaderboard
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

# Temp victory screen that dissapears automatically
def draw_victory_screen(who_won, stilling1, stilling2):
    surface.fill(WHITE)

    global gamestate

    font = pg.font.SysFont('arial', 80)
    title = font.render(who_won, True, BLACK)
    surface.blit(title, (center_width(title.get_width()), center_height(title.get_height()) - OFFSET))

    # appends score from previous game
    update_database(stilling1, stilling2, who_won)

    pg.display.update()


def update_board(engine):
    # Draws all the balls on the board
    for i in range(12):
        if i <= 5:
            generate(engine.board[i], boardbutton_list[i].get_x_pos(), boardbutton_list[i].get_y_pos())
        elif i >= 6:
            generate(engine.board[18 - i], boardbutton_list[i].get_x_pos(), boardbutton_list[i].get_y_pos())
    # Draws balls in goals
    generate_score_left(engine.board[13])
    generate_score_right(engine.board[6])

    # Draws the score text
    for i in range(12):
        if i <= 5:
            boardbutton_list[i].draw_text(str(engine.board[i]))
        elif i >= 6:
            boardbutton_list[i].draw_text(str(engine.board[18 - i]))

    # Draws score on goals
    Scoreleftbutton.draw_text(str(engine.board[13]))
    Scorerightbutton.draw_text(str(engine.board[6]))


# updates the board arcording to the new move made so it is slow indead of instend
def update_move(oldboard, newboard, engine):
    # dict that contains the corresponding value, becuase the way the board is set up arcording to the board list
    correct_button_list = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0, 13: 0, 12: 7, 11: 8, 10: 9, 9: 10, 8: 11, 7: 12}
    update_list = []
    updated_board = []
    starting_point = None
    y = 0
    i = 0
    # for loop that makes a new board that has the location of the updated values
    for element in oldboard:
        new_value = newboard[y] - element
        updated_board.append(new_value)
        y += 1
    # for loop that appends the updated_board values if the location has been changed
    for element in updated_board:
        if element > 0:
            update_list.append(i)
        # checks if it was the starting point of the move
        elif element < 0:
            update_list.append(i)
            starting_point = i
        i += 1
    # sets starting_points variable to the index of where it is in update_list
    starting_point = update_list.index(starting_point)
    z = starting_point
    # for loop that loops through update_list and slowly adds the new number to the buttons values
    for __ in range(len(update_list)):
        # x variable that contains which button that needs to be updated
        x = f"boardbutton_list[{correct_button_list[update_list[z]] - 1}]"
        # num variable that contains what value in the game board it need to get
        num = update_list[z]
        # if statement that checks if it is one of the goals, because it has a different variable name then just adding 1 number to it
        if num == 6:
            Scorerightbutton.draw_text(str(engine.board[6]))
        elif num == 13:
            Scoreleftbutton.draw_text(str(engine.board[13]))
        else:
            # eval(x) turns the str value into a variable number, so the correct button gets updated
            eval(x).draw_text(str(engine.board[num]))
        # updates the GUI
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
        # Sequence detects button clicks (Has to be in while loop to prevent lag)
        # Changes gametate according to button
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
        # Detects clicks on game button and moves accordingly
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
    # Makes a move one at a time, instead of all at once
    if gamestate == "game":
        if gameBoard != game_engine.board:
            update_move(gameBoard, game_engine.board, game_engine)
            gameBoard = []
            for element in game_engine.board:
                gameBoard.append(element)
            update_board(game_engine)

    if gamestate == "game":
        draw_game(game_engine, isplayer1, bot_move)
    # Detects win and changes to victory screen
    if game_engine.check_win()[0]:
        gamestate = "victory"
    # Restarts after 4 secs and goes to main menu
    if gamestate == "victory":
        draw_victory_screen(game_engine.check_win()[1],game_engine.board[6], game_engine.board[13])
        time.sleep(4)
        gamestate = "start_menu"
    # Resets game and draws screen
    if gamestate == "start_menu":
        game_engine.board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        isplayer1 = True
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
