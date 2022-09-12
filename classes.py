import pyglet
from pyglet.window import key

from network import Network_client

PLAYER_WIDTH=16
PLAYER_HEIGHT=16
SPEED = 10


class Player:
    def __init__(self, img, x, y, batch=None) -> None:
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(img, x, y, batch=batch)
        self.direction = 0
        self.new_direction = 0
        self.images = [img.get_transform(True), img]


    def update_pos(self):
        self.sprite.update(x=self.x, y=self.y)

    def update(self, keyboard, dt):
        self.input_handler(keyboard, dt)
        self.change_direction(self.new_direction)
        self.update_pos()
        
    def change_direction(self, direction):
        if direction != self.direction:
            self.direction = direction
            self.sprite.image = self.images[direction]


    def input_handler(self, keyboard, dt):
        if keyboard[key.D]:
            self.x += SPEED
            self.new_direction = 1
        elif keyboard[key.A]:
            self.x -= SPEED
            self.new_direction = 0
        if keyboard[key.W]:
            self.y += SPEED
        elif keyboard[key.S]:
            self.y -= SPEED

    def network_position(self):
        return [self.x, self.y]


    def change_color(self, color: tuple):
        self.sprite.color = color
        self.sprite._update_color()

