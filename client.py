import pyglet
from pyglet import image

from network import Network_client
from classes import Player
from tools import ASSET_DICT

WIDTH = 1080
HEIGHT = 720
FPS = 60
NOT_PLAYER_COLOR = (10,223,15)

player_img = ASSET_DICT['test_img']

class Game_client(pyglet.window.Window):
    def __init__(self) -> None:
        super(Game_client, self).__init__()

        self.network = Network_client()
        self.set_size(WIDTH, HEIGHT)
        self.player_batch = pyglet.graphics.Batch()
        self.player = Player(player_img, 20, 30, self.player_batch)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        self.npcs = {}

        pyglet.clock.schedule_interval(self.update, 1/FPS)
        pyglet.clock.schedule_interval(self.draw, 1/FPS)

        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

    def update(self, dt):
        self.player.update(self.keyboard, dt)

        data = {
            'location': self.player.network_position(),
            'color': NOT_PLAYER_COLOR
        }
        self.network.send(data)


        for npc in self.network.responses.keys():
            coords = self.network.responses[npc]['location']
            color = self.network.responses[npc]['color']
            if npc not in self.npcs:
                if npc == self.network.identifier:
                    pass
                else:
                    self.npcs[npc] = [coords, Player(player_img, coords[0], coords[1], batch = self.player_batch)]
            else:
                player   = self.npcs[npc][1]
                player.x = coords[0]
                player.y = coords[1]
                player.change_color(color)
                player.update_pos()

    def draw(self, dt):
        self.clear()
        self.player_batch.draw()


if __name__ == "__main__":
    game = Game_client()
    pyglet.app.run()
