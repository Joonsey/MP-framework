import pyglet
from pyglet import image
import sys
from sys import argv

from network import Network_client
from classes import SPEED, Player, Physics_object
from tools import ASSET_DICT, PACKET_SIZE

AMOUNT_OF_BYTES_IN_PACKET = 6 #THIS WILL EXPAND AS PACKET SIZE INCREASES
# SEE NETWORK ln 10:18 -> FOR REFERENCE!
WIDTH = 1080
HEIGHT = 720
FPS  = 120
TPS  = 20
FONT_SIZE = 36
NOT_PLAYER_COLOR = (10,223,15)
IP = "52.143.187.171"
PORT = 5555

player_img = ASSET_DICT['test_img']
#player_img = ASSET_DICT['test_anim']
player_img = ASSET_DICT['test_img_spritesheet']

class Game_client(pyglet.window.Window):
    def __init__(self, network: Network_client) -> None:
        super(Game_client, self).__init__()

        self.network = network
        self.set_size(WIDTH, HEIGHT)
        self.player_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.player = Player(player_img, 20, 30, self.player_batch)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        self.npcs = {}
        self.tick = 0
        self.fps = 0

        #TEST
        #TODO remove when testing is redundant
        self.player.objects_to_collide_with.append(Physics_object(30,30,30,30))

        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

        pyglet.clock.schedule_interval(self.update, 1/TPS)
        pyglet.clock.schedule_interval(self.draw, 1/FPS)

        self.fps_counter_label = pyglet.text.Label(
            int(self.fps).__str__(),
            font_name="new times roman",
            font_size=FONT_SIZE,
            x = 0,
            y = self.height-FONT_SIZE,
            batch=self.ui_batch
        )

        self.debug_label = pyglet.text.Label(
            "debug",
            font_name="new times roman",
            font_size=FONT_SIZE,
            x = self.width - 100,
            y = self.height-FONT_SIZE,
            batch=self.ui_batch
        )

    def get_players(self):
        npcs = self.network.responses
        for i in range(0, len(npcs), AMOUNT_OF_BYTES_IN_PACKET):
            id = npcs[i]
            x_coord = npcs[i+1]
            y_coord = npcs[i+2]
            color = npcs[i+3:i+6]

            # supported data structure for color
            #color = b'\xff\x00\x00'
            #color = [0,0,255]

            if id.to_bytes(1, 'little') == self.network.identifier:
                pass
            elif id not in self.npcs.keys():
                self.npcs[id] = Player(player_img, x_coord * SPEED, y_coord * SPEED, batch = self.player_batch)
            else:
                player   = self.npcs[id]
                player.x = x_coord * SPEED
                player.y = y_coord * SPEED
                player.update_pos()
                player.set_color_from_bytes(color)

    def update(self, dt):
        self.tick = pyglet.clock.tick()
        self.fps = pyglet.clock.get_fps()
        self.fps_counter_label.text = int(self.fps).__str__()
        self.fps_counter_label.y = self.height - FONT_SIZE
        self.debug_label.y = self.height - FONT_SIZE
        self.debug_label.x = self.width - self.debug_label.content_width
        self.debug_label.text = str(self.player.is_coliding) + " " + str(self.player.x) + ", " +  str(self.player.y)
        self.player.update(self.keyboard, dt)

        data = (
        self.network.identifier
        + int(self.player.x / SPEED).to_bytes(1,'little')
        + int(self.player.y / SPEED).to_bytes(1, 'little')
        + self.player.get_color_in_bytes()
        )
        #print(len(data)) #TODO KEEP THIS
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
    game = Game_client(Network_client(IP, PORT))
    pyglet.app.run()
