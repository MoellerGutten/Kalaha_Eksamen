import pygame as pg
import math

pg.init()

width = 1000
height = 700

pi = math.pi

res = [width, height]

white = (255, 255, 255)
screen_display = pg.display

surface = screen_display.set_mode(res)

ball = pg.image.load("Kalaha_Kugle.png")


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

window = True
while window:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            window = False

    surface.fill(white)
    generate(10)
    screen_display.update()

pg.quit()