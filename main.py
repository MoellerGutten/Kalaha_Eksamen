import pygame as pg
import math

pg.init()

width = 1000
height = 1000

pi = math.pi

res = [width, height]

white = (255, 255, 255)
grey = (105,105,105)
black = (0,0,0)
screen_display = pg.display

window_icon = pg.image.load( "window_icon.png")

pg.display.set_caption("Kalaha",)
pg.display.set_icon(window_icon)

surface = screen_display.set_mode(res)

ball = pg.image.load("Kalaha_Kugle.png")

gamestate = "start_menu"


class button():
    def __init__(self, color, x, y, button_width, button_height,  text=''):
        self.color = color
        self.x = x
        self.y = y
        self.button_width = button_width
        self.button_height = button_height
        self.text = text


    def draw(self, surface, border_width, outline):
        # Call this method to draw the button on the screen
        if outline and border_width:
            pg.draw.rect(surface, outline, (self.x - border_width, self.y - border_width, self.button_width + (border_width*2), self.button_height + (border_width*2)), 0)

        pg.draw.rect(surface, self.color, (self.x, self.y, self.button_width, self.button_height), 0)

        if self.text != '':
            font = pg.font.SysFont('comicsans', 40)
            text = font.render(self.text, True, (white))
            surface.blit(text, (self.x + (self.button_width / 2 - text.get_width() / 2), self.y + (self.button_height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.button_width:
            if pos[1] > self.y and pos[1] < self.y + self.button_height:
                return True

        return False


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
    generate(7)
    screen_display.update()


def draw_start_screen():
    surface.fill(white)
    font = pg.font.SysFont('arial', 40)
    title = font.render('Kalaha', True, black)
    start_button = font.render('Start', True, black)
    surface.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 2))
    surface.blit(start_button, (width / 2 - start_button.get_width() / 2, height/ 2 + start_button.get_height() / 2))
    button1 = button(black, 100,100,100,50,"hej")
    button1.draw(surface, 5, outline=grey)
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