import math
import sqlite3 as lite
import pygame as pg
import pygame_menu as pgm
from buttonclass import Button, backButton, imgButton
from pygame import mixer
import random
from datetime import date


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


button_start = Button(light_grey, 300,  75, 0, "start_menu", "Start Game")
back_button = backButton(light_grey, 50, 50, 200, 50, 0, "game", "Back")
back_button_leaderboard = backButton(light_grey, 50, 50, 200, 50, 0, "leaderboard", "Back")
button_leaderboard = Button(light_grey, 300, 75, 1,"start_menu", "Leaderboard")
button_quit = Button(light_grey, 300, 75, 2, "start_menu", "Quit")

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

def update_database(stilling, resultat):
    tidspunkt = date.today()
    con = None
    con = lite.connect("leaderboard.db")
    cur = con.cursor()
    cur.execute("INSERT INTO leaderbord(stilling, resultat, tidspunkt) VALUES('" + str(stilling) + "','" + str(resultat) + "', '" + str(tidspunkt) + "')")
    con.commit()
    con.close()

def update_leaderboard():
    print("hello")


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
    end_time = 0
    surface.fill(white)

    global gamestate

    img_button.draw()

    color = (255, 0, 0)

    generate_ellipse(10)

    for i in range(8):
        pg.draw.rect(surface, color,
                     pg.Rect((gamewidth / 2) + i / 7 * gamewidth-26, height - (height - gameheight / 2), 40, 120))

    for i in range(8):
        pg.draw.rect(surface, color,
                     pg.Rect((gamewidth / 2) + i / 7 * gamewidth-26, height - (height - gameheight / 2)+400, 40, 120))

    pressed = pg.key.get_pressed()
    k = 50
    if img_button.isOver():
        #if event.type == pg.MOUSEBUTTONDOWN:
        if pressed[pg.K_RIGHT]:
            for k in range(50):
                img_button.move_button()



    back_button.draw(surface, 5, outline=black)

    screen_display.update()


def draw_leaderboard():
    surface.fill(white)

    global gamestate

    font = pg.font.SysFont('arial', 40)
    title = font.render('Leaderboard', True, black)

    back_button_leaderboard.draw(surface, 5, outline=black)

    con = None
    con = lite.connect("leaderboard.db")
    cur = con.cursor()

    i = 35
    column_space = 200

    head1 = font.render(f'Spiller', True, black)
    head2 = font.render(f'Stilling', True, black)
    head3 = font.render(f'Resultat', True, black)
    head4 = font.render(f'Dato', True, black)
    surface.blit(head1, [gamewidth / 5, (700 / 4) + 5])
    surface.blit(head2, [gamewidth / 5 + column_space, (700 / 4) + 5])
    surface.blit(head3, [gamewidth / 5 + 2 * column_space, (700 / 4) + 5])
    surface.blit(head4, [gamewidth / 5 + 3 * column_space, (700 / 4) + 5])



    cur.execute('SELECT * FROM leaderbord')
    rows = cur.fetchall()
    for row in rows:
        column1 = font.render('{:>5}'.format(str(row[1])), True, black)
        column2 = font.render('{:30}'.format(str(row[2])), True, black)
        column3 = font.render('{:60}'.format(row[3]), True, black)
        column4 = font.render('{:90}'.format(row[4]), True, black)
        surface.blit(column1, [gamewidth / 5, (700 / 4) + i + 5])
        surface.blit(column2, [gamewidth / 5 + column_space, (700 / 4) + i + 5])
        surface.blit(column3, [gamewidth / 5 + 2*column_space, (700 / 4) + i + 5])
        surface.blit(column4, [gamewidth / 5 + 3*column_space, (700 / 4) + i + 5])

        i += 39
    con.close()

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
                update_leaderboard()

        if button_quit.isOver(gamestate):
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
