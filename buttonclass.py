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
    def __init__(self, color, button_width, button_height, index, text=''):
        self.color = color
        self.button_width = button_width
        self.button_height = button_height
        self.text = text
        self.index = index
        self.x = width / 2 - self.button_width / 2
        self.y = height / 2 - self.button_height / 2 + offset * self.index

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

    def isOver(self):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pg.mouse.get_pos()
        if self.x < pos[0] < self.x + self.button_width:
            if self.y < pos[1] < self.y + self.button_height:
                self.color = grey
                self.draw(surface, 5, outline=black)
                return True
        return False

    def isClicked(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and self.isOver():
                return True
            return False