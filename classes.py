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
    def update(self):
        self.sprite.update(x=self.x, y=self.y)

    def draw(self, keyboard, dt):
        self.input_handler(keyboard, dt)
        self.update()
        self.sprite.draw()

    def input_handler(self, keyboard, dt):
        if keyboard[key.D]:
            self.x += SPEED
        elif keyboard[key.A]:
            self.x -= SPEED
        if keyboard[key.W]:
            self.y += SPEED
        elif keyboard[key.S]:
            self.y -= SPEED

    def network_position(self):
        return "%d, %d" % (self.x, self.y)
