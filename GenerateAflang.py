import pygame as pg
import random
import math
from PIL import Image


#OBSOLETE FILE, SE main.py !!!
#OBSOLETE FILE, SE main.py !!!
#OBSOLETE FILE, SE main.py !!!

pg.init()

width = 1000
height = 700

pi = math.pi

res = [width, height]

white = (255,255,255)
red = (180,50,50)
screen_display = pg.display

surface2 = screen_display.set_mode(res)
surface = screen_display.set_mode(res)


angle = random.random()*pi*2

ball = pg.image.load("images/Kalaha_Kugle.png")
ball_x = ball.get_size()[0]
ball_y = ball.get_size()[1]

pos_x = (width - ball_x) / 2
pos_y = (height - ball_y) / 2

def generate_ellipse(n):
    ellipse1 = pg.Rect(100,100,200,400)
    pg.draw.ellipse(surface, red, ellipse1, width=5)

    max_x = ellipse1.bottomright[0]-ellipse1.topleft[0]
    max_y = ellipse1.bottomright[1]-ellipse1.topleft[1]


    for i in range(n):
        ball_pos_x = random.randrange(max_x)
        ball_pos_y = random.randrange(max_y)
        surface2.blit(ball, (ball_pos_x, ball_pos_y))

    export()

def export():
    data = pg.image.save(surface2, "Balls.png")



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            window = False

        surface.fill(white)
        generate_ellipse(10)

        screen_display.update()


pg.quit()