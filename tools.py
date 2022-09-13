import os
import pyglet
from pyglet.image import load, ImageGrid
from pyglet.resource import animation, image
from pyglet.sprite import Sprite
from _thread import start_new_thread

pyglet.resource.path

asset_folder_name = 'assets'
assets_path = os.path.join(os.getcwd(), asset_folder_name)

def run_in_thread(func):
    def run(*k, **kw):
        start_new_thread(func, k)
    return run

def load_animation_from_sequntial_file(img_dir, rows=1, cols=1, duration=0.2):
    return pyglet.image.Animation.from_image_sequence(ImageGrid(load(os.path.join(assets_path, img_dir)), rows=rows, columns=cols), duration=duration)
GLOBAL_SERVER_IP = "84.212.20.23"
PACKET_SIZE = 10240

"""containing paths to all assets"""
ASSET_DICT = {
    'test_img': load(os.path.join(assets_path, 'test.png')),
    'test_img_spritesheet': load_animation_from_sequntial_file('test_animation_sheet.png', cols=4),
    #'test_anim': animation(os.path.join(assets_path, 'test.gif'))
}




