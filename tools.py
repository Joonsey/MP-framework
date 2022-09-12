import os
import pyglet
from pyglet.image import load

asset_folder_name = 'assets'
assets_path = os.path.join(os.getcwd(), asset_folder_name)
"""containing paths to all assets"""
ASSET_DICT = {
    'test_img': load(os.path.join(assets_path, 'test.png'))
}


