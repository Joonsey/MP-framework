import pyglet
from pyglet import image

from network import Network_client
from classes import Player

WIDTH = 1080
HEIGHT = 720
FPS = 60

player_img = image.load('test.png')

class Game_client(pyglet.window.Window):
    def __init__(self) -> None:
        super(Game_client, self).__init__()

        self.network = Network_client()
        self.set_size(WIDTH, HEIGHT)
        self.batch = pyglet.graphics.Batch()
        self.player = Player(player_img, 20, 30, self.batch)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        pyglet.clock.schedule_interval(self.draw, 1/FPS)
        #pyglet.clock.schedule_interval(self.draw, 1/FPS)
        # if i at some point want to make a update function at a differen frequency than fps

        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

    def draw(self, dt):
        self.clear()
        self.player.draw(self.keyboard, dt)
        self.network.send(self.player.network_position())
        print(self.network.responses)


if __name__ == "__main__":
    game = Game_client()
    pyglet.app.run()
