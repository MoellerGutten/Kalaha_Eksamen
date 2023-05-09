import pygame as pg
pg.init()

width = 1000
height = 1000

res = [width, height]

white = (255, 255, 255)
light_grey = (197, 197, 197)
grey = (100, 100, 100)
black = (0, 0, 0)

offset = 100

screen_display = pg.display

surface = screen_display.set_mode(res)


# Template from S0
class Button:
    def __init__(self, color, x, y, button_width, button_height, buttongamestate, text=''):
        self.color = color
        self.button_width = button_width
        self.button_height = button_height
        self.buttongamestate = buttongamestate
        self.text = text
        self.x = x
        self.y = y

    def draw(self, surface, border_width, outline):
        # Call this method to draw the button on the screen
        if outline and border_width:
            # Parameters in order of appearance: (pygame display, outline colour, x position, y position, button width, button height, border curvature)
            pg.draw.rect(surface, outline, (self.x - border_width, self.y - border_width, self.button_width + (border_width*2), self.button_height + (border_width*2)), 0)

        # Same as above
        pg.draw.rect(surface, self.color, (self.x, self.y, self.button_width, self.button_height), 0)

        if self.text != '':
            font = pg.font.SysFont('arial', 40)
            text = font.render(self.text, True, black)
            # Parameters in order of appearance: (text, x, y)
            surface.blit(text, (self.x + (self.button_width / 2 - text.get_width() / 2), self.y + (self.button_height / 2 - text.get_height() / 2)))

    def draw_text(self, text):
        if text != '':
            font = pg.font.SysFont('arial', 80)
            font2 = pg.font.SysFont('arial', 90)
            toWrite1 = font.render(text, True, white)
            toWrite2 = font2.set_bold(True)
            toWrite2 = font2.render(text, True, black)
            # Parameters in order of appearance: (text, x, y), where the x and y is centered
            surface.blit(toWrite2, (self.x + (self.button_width / 2 - toWrite2.get_width() / 2), self.y + (self.button_height / 2 - toWrite2.get_height() / 2)))
            surface.blit(toWrite1, (self.x + (self.button_width / 2 - toWrite1.get_width() / 2), self.y + (self.button_height / 2 - toWrite1.get_height() / 2)))

    def isOver(self, gamestate):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pg.mouse.get_pos()
        self.color = light_grey
        if self.x < pos[0] < self.x + self.button_width:
            if self.y < pos[1] < self.y + self.button_height:
                if gamestate == self.buttongamestate:
                    self.color = grey
                    return True
        return False

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y