import pygame as pg
import math

pg.init()

width = 1000
height = 1000

pi = math.pi

res = [width, height]

white = (255, 255, 255)
screen_display = pg.display

window_icon = pg.image.load( "window_icon.png")

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
    generate(10)
    screen_display.update()


def draw_start_screen():
    surface.fill(white)
    font = pg.font.SysFont('arial', 40)
    title = font.render('Kalaha', True, (0,0,0))
    start_button = font.render('Start', True, (0,0,0))
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2))
    surface.blit(start_button, (width / 2 - start_button.get_width() / 2, height/ 2 + start_button.get_height() / 2))
    pg.display.update()


window = True
while window:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            window = False
    if gamestate == "start_menu":
        draw_start_screen()
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            gamestate = "game"
    if gamestate == "game":
        draw_game()


pg.quit()