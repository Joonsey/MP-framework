import pyglet
from pyglet import image

import pickle
import dill

from network import Network_client
from classes import Player

WIDTH = 1080
HEIGHT = 720
FPS = 10

player_img = image.load('test.png')

class Game_client(pyglet.window.Window):
    def __init__(self) -> None:
        super(Game_client, self).__init__()

        self.set_size(WIDTH, HEIGHT)
        self.batch = pyglet.graphics.Batch()
        self.player = Player(player_img, 20, 30, self.batch)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        pyglet.clock.schedule_interval(self.draw, 1/FPS)


    def draw(self, dt):
        self.player.draw(self.keyboard, dt)


if __name__ == "__main__":
    game = Game_client()
    pyglet.app.run()
