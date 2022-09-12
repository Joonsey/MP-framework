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
        self.npcs = {}
        self._npcs = []

        pyglet.clock.schedule_interval(self.draw, 1/FPS)
        #pyglet.clock.schedule_interval(self.draw, 1/FPS)
        # if i at some point want to make a update function at a different frequency than fps

        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

    def draw(self, dt):
        self.clear()
        self.player.update(self.keyboard, dt)
        self.network.send(self.player.network_position())

        for npc in self.network.responses.keys():
            coords = self.network.responses[npc]
            if npc not in self.npcs:
                if npc == self.network.identifier:
                    pass
                else:
                    self.npcs[npc] = [coords, Player(player_img, coords[0], coords[1], batch = self.batch)]
            else:
                player = self.npcs[npc][1]
                player.x = coords[0]
                player.y = coords[1]
                player.update_pos()


        self.batch.draw()


if __name__ == "__main__":
    game = Game_client()
    pyglet.app.run()
