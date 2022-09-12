import os
import pyglet
from pyglet.image import load, ImageGrid
from pyglet.resource import animation, image
from pyglet.sprite import Sprite

pyglet.resource.path

asset_folder_name = 'assets'
assets_path = os.path.join(os.getcwd(), asset_folder_name)


GLOBAL_SERVER_IP = "84.212.20.23"
PACKET_SIZE = 10240

"""containing paths to all assets"""
ASSET_DICT = {
    'test_img': load(os.path.join(assets_path, 'test.png')),
    'test_img_spritesheet': pyglet.image.Animation.from_image_sequence(ImageGrid(load(os.path.join(assets_path, 'test_animation_sheet.png')), rows=1, columns=4), duration=0.2)
    #'test_anim': animation(os.path.join(assets_path, 'test.gif'))
}




