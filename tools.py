import os
import pyglet
from pyglet.image import load

asset_folder_name = 'assets'
assets_path = os.path.join(os.getcwd(), asset_folder_name)


GLOBAL_SERVER_IP = "84.212.20.23"
PACKET_SIZE = 10240

"""containing paths to all assets"""
ASSET_DICT = {
    'test_img': load(os.path.join(assets_path, 'test.png'))
}




