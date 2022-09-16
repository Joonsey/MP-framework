import pyglet
from pyglet import image
import sys
from sys import argv

from network import Network_client
from classes import SPEED, Player
from tools import ASSET_DICT, PACKET_SIZE

AMOUNT_OF_BYTES_IN_PACKE = 3 #THIS WILL EXPAND AS PACKET SIZE INCREASES
# SEE NETWORK ln 10:18 -> FOR REFERENCE!
WIDTH = 1080
HEIGHT = 720
FPS  = 120
TPS  = 20
FONT_SIZE = 36
NOT_PLAYER_COLOR = (10,223,15)
IP   = "localhost"
IP = "52.143.187.171"
PORT = 5555

player_img = ASSET_DICT['test_img']
#player_img = ASSET_DICT['test_anim']
player_img = ASSET_DICT['test_img_spritesheet']

class Game_client(pyglet.window.Window):
    def __init__(self) -> None:
        super(Game_client, self).__init__()

        self.network = Network_client(IP, PORT)
        self.set_size(WIDTH, HEIGHT)
        self.player_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.player = Player(player_img, 20, 30, self.player_batch)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        self.npcs = {}
        self.tick = 0
        self.fps = 0



        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

        pyglet.clock.schedule_interval(self.update, 1/TPS)
        pyglet.clock.schedule_interval(self.draw, 1/FPS)

        self.fps_counter_label = pyglet.text.Label(
            self.fps.__str__(),
            font_name="new times roman",
            font_size=FONT_SIZE,
            x = 0,
            y = self.height-FONT_SIZE,
            batch=self.ui_batch
        )

    def get_players(self):
        npcs = self.network.responses
        for i in range(0, len(npcs), AMOUNT_OF_BYTES_IN_PACKET):
            id = npcs[i]
            coords = npcs[i+1:i+3]
            if id.to_bytes(1, 'little') != self.network.identifier and id not in self.npcs.keys():
                self.npcs[id] = Player(player_img, coords[0] * SPEED, coords[1] * SPEED, batch = self.player_batch)
            else:
                try:
                    player   = self.npcs[id]
                    player.x = coords[0] * SPEED
                    player.y = coords[1] * SPEED
                    player.update_pos()
                except: pass

    def update(self, dt):
        self.tick = pyglet.clock.tick()
        self.fps = pyglet.clock.get_fps()
        self.fps_counter_label.text = self.fps.__str__()
        self.fps_counter_label.y = self.height - FONT_SIZE
        self.player.update(self.keyboard, dt)

        data = self.network.identifier + int(self.player.x / SPEED).to_bytes(1,'little') + int(self.player.y / SPEED).to_bytes(1, 'little')
        self.network.send(data)
        self.get_players()

        self.handle_client_inputs(self.keyboard)

    def handle_client_inputs(self, keyboard):
        # TODO
        # MAJOR FUCKING ISSUE WITH THESE

        if keyboard[pyglet.window.key.Q]:
            sys.exit(0)

        if keyboard[pyglet.window.key.F11]:
            self.set_fullscreen(True if not self.fullscreen else False)

        elif keyboard[pyglet.window.key.F12]:
            self.set_fullscreen(False if self.fullscreen else True)


    def draw(self, dt):
        self.clear()
        self.player_batch.draw()
        self.ui_batch.draw()


if __name__ == "__main__":
    args = len(argv) > 1
    if args:
        if argv[1] == '-l':
            IP = "localhost"
    game = Game_client()
    pyglet.app.run()
