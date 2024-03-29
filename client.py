from pyglet import image
from sys import argv

import random
import threading
import pyglet
import sys

from pyglet.window import FPSDisplay
import server

from network import Network_client, Packet
from classes import CONST_MOVEMENT_SPEED, SPEED, Moving_particle, Player, Physics_object, Level, Tile, Particle, Light_particle
from tools import ASSET_DICT, PACKET_SIZE, get_padding_for_map, TILE_SIZE, BYTEORDER

LEVEL_WIDTH = 32
LEVEL_HEIGHT = 32

AMOUNT_OF_BYTES_IN_PACKET = 9 #THIS WILL EXPAND AS PACKET SIZE INCREASES
# SEE NETWORK ln 10:18 -> FOR REFERENCE!
WIDTH = 1080
HEIGHT = 720
FPS = 120
TPS = 60
FONT_SIZE = 36
NOT_PLAYER_COLOR = (10,223,15)
IP = "52.143.187.171"
PORT = 5555

player_img = ASSET_DICT['test_img']
#player_img = ASSET_DICT['test_anim']
player_img = ASSET_DICT['test_img_spritesheet']

class Game_client(pyglet.window.Window):
    def __init__(self, network: Network_client, vsync=True) -> None:
        super(Game_client, self).__init__()

        self.set_vsync(vsync)
        self.network = network
        self.set_size(WIDTH, HEIGHT)
        self.player_batch = pyglet.graphics.Batch()
        self.level_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.particle_batch = pyglet.graphics.Batch()
        self.player = Player(player_img, 20, 30, self.player_batch)
        self.level = Level(LEVEL_WIDTH, LEVEL_HEIGHT)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        self.npcs = {}
        self.particles = []
        self.fps = 0
        self.player.objects_to_collide_with = self.level.collision_tiles
        self.fps_display_label = FPSDisplay(window=self)

        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

        self.debug_label = pyglet.text.Label(
            "debug",
            font_name="new times roman",
            font_size=FONT_SIZE,
            x = self.width - 100,
            y = self.height-FONT_SIZE,
            batch=self.ui_batch
        )

        self.map_seed = ASSET_DICT['map_seed']

        self.level.draw_level(self.map_seed, batch=self.level_batch)
        left_padding, bottom_padding = get_padding_for_map(self.map_seed, self.width, self.height)
        self.level.update_level_pos_with_respect_to_padding(left_padding, bottom_padding)

        pyglet.clock.schedule_interval(self.update, 1/TPS)
        pyglet.clock.schedule_interval(self.draw, 1/FPS)

    def get_players(self):
        npcs = self.network.responses
        for i in range(0, len(npcs), AMOUNT_OF_BYTES_IN_PACKET):
            packet = Packet(
                npcs[i],
                int.from_bytes(npcs[i+1:i+3], BYTEORDER),
                int.from_bytes(npcs[i+3:i+5], BYTEORDER),
                npcs[i+5:i+8],
                npcs[i+8])
            id = packet.id

            if id.to_bytes(1, BYTEORDER) == self.network.identifier:
                pass
            elif id not in self.npcs.keys():
                self.npcs[id] = Player(player_img, packet.x * CONST_MOVEMENT_SPEED, packet.x * CONST_MOVEMENT_SPEED, batch = self.player_batch)
            else:
                player   = self.npcs[id]
                player.x = packet.x
                player.y = packet.y
                player.set_color_from_bytes(packet.color)
                player.change_direction(packet.direction)
                player.update_pos()
                if player.physics_obj not in self.player.other_players: self.player.other_players.append(player.physics_obj)

    def update(self, dt):
        self.fps = pyglet.clock.get_fps()
        self.debug_label.y = self.height - FONT_SIZE
        self.debug_label.x = self.width - self.debug_label.content_width
        self.debug_label.text = str(self.player.is_coliding) + " " + str(int(self.player.x)) + ", " +  str(int(self.player.y))
        self.player.update(self.keyboard, dt)

        data = (
            self.network.identifier
            + int(self.player.x).to_bytes(2,BYTEORDER)
            + int(self.player.y).to_bytes(2, BYTEORDER)
            + self.player.get_color_in_bytes()
            + self.player.direction.to_bytes(1, BYTEORDER)
        )
        #print(len(data)) #TODO KEEP THIS
        self.network.send(data)
        self.get_players()

        self.spawn_random_default_particle()
        self.handle_client_inputs(self.keyboard)

    def handle_client_inputs(self, keyboard):
        # TODO
        # MAJOR FUCKING ISSUE WITH THESE

        if keyboard[pyglet.window.key.Q]:
            sys.exit(0)

        # FULLSCREEN
        if keyboard[pyglet.window.key.F11] and not self.fullscreen:
            self.set_fullscreen(True)

        elif keyboard[pyglet.window.key.F12] and self.fullscreen:
            self.set_fullscreen(False)

        if keyboard[pyglet.window.key.F]:
            left_padding, bottom_padding = get_padding_for_map(self.map_seed, self.width, self.height)
            self.level.update_level_pos_with_respect_to_padding(left_padding, bottom_padding)



    def spawn_random_default_particle(self):
        """
        primairly for test purposes

        spawns default particle and random location on screen
        """
        if random.randint(0,100) < 30:
            randx = random.randint(0,self.width)
            randy = random.randint(0,self.height)
            self.particles.append(Light_particle(randx, randy,-5, 10, batch=self.particle_batch))

        for particle in self.particles:
            new_xpos = particle.xpos + random.randint(particle.velocity,0)
            new_ypos = particle.ypos + random.randint(particle.velocity,0)
            particle.update_pos(new_xpos, new_ypos)
            particle.lifespan -= .1
            if particle.lifespan <= 0:
                self.particles.pop(self.particles.index(particle))
                del particle


    def draw(self, dt):
        """being called by the pyglet.clock"""
        self.clear()
        self.level_batch.draw()
        self.player_batch.draw()
        self.particle_batch.draw()
        self.ui_batch.draw()
        self.fps_display_label.draw()

    def on_resize(self, width, height):
        left_padding, bottom_padding = get_padding_for_map(self.map_seed, width, height)
        self.level.update_level_pos_with_respect_to_padding(left_padding, bottom_padding)
        return super().on_resize(width, height)



if __name__ == "__main__":
    args = len(argv) > 1
    vsync = False
    if args:
        if '-l' in argv:
            IP = "localhost"
        if '-h' in argv:
            client_server = server.Network_server(IP, PORT)
            threading.Thread(target=client_server.run, daemon=True).start()
            print(f"hosting server at {IP} and port: {PORT}")
        if '-vsync' in argv:
            vsync = True

    print(f"looking for server at {IP} ...")
    game = Game_client(Network_client(IP, PORT), vsync=vsync)
    pyglet.app.run()
