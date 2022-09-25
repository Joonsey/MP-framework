import os
import pyglet
from pyglet.image import load, ImageGrid
from pyglet.resource import animation, image
from pyglet.sprite import Sprite
from _thread import start_new_thread

TILE_SIZE = 32

asset_folder_name = 'assets'
assets_path = os.path.join(os.getcwd(), asset_folder_name)

def run_in_thread(func):
    def run(*k, **kw):
        start_new_thread(func, k)
    return run

def get_padding_for_map(map_seed, width, height):
    total_size_of_map_horizontal = len(map_seed[0])*TILE_SIZE
    total_size_of_map_vertical = len(map_seed)*TILE_SIZE
    left_padding = (width/2) - (total_size_of_map_horizontal/2)
    bottom_padding = (height/2) - (total_size_of_map_vertical/2)

    return left_padding, bottom_padding

def get_amount_of_cols(width):
    return width // TILE_SIZE

def get_amount_of_rows(height):
    return height // TILE_SIZE

def load_animation_from_sequential_file(img_dir, rows=1, cols=1, duration=0.2) -> pyglet.image.Animation:
    """
    loads an animation from a file containing sequences of images
    if rows and cols are not specified it will dynamically find the amount of columns
    """
    return pyglet.image.Animation.from_image_sequence(get_imagegrid_from_file(img_dir, rows, cols), duration=duration)

def load_animation_from_imagegrid(imagegrid: ImageGrid, duration=0.2) -> pyglet.image.Animation:
    """loads an animation from an ImageGrid object"""
    return pyglet.image.Animation.from_image_sequence(imagegrid, duration)

def get_imagegrid_from_file(img_dir, rows=1, cols=1) -> ImageGrid:
    """
    construct an image grid from a file
    if rows and cols are not specified it will dynamically find the amount of columns
    """
    img = load(os.path.join(assets_path, img_dir))
    if cols == 1 and rows == 1:
        return ImageGrid(img, rows=get_amount_of_rows(img.height), columns=get_amount_of_cols(img.width))
    else:
        return ImageGrid(img, rows=rows, columns=cols)

GLOBAL_SERVER_IP = "84.212.20.23"
PACKET_SIZE = 10240


rocks = get_imagegrid_from_file('rocks.png')
red_bush = get_imagegrid_from_file('red-bush.png')
green_bush = get_imagegrid_from_file('green-bush.png')

"""containing paths to all assets"""
ASSET_DICT = {
    'test_img': load(os.path.join(assets_path, 'test.png')),
    'test_img_spritesheet': load_animation_from_sequential_file('test_animation_sheet.png', cols=4),
    'tiles': {
        1: rocks[0],
        2: rocks[3],
        3: red_bush[2],
    },
    'map_seed':
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 2, 1, 2, 2, 0, 1, 1, 1],
        [0, 1, 1, 2, 1, 2, 2, 0, 1, 1, 1],
        [0, 3, 1, 2, 1, 1, 2, 0, 1, 3, 1],
        [0, 3, 3, 2, 1, 1, 1, 0, 3, 3, 1],
        [1, 1, 3, 1, 1, 1, 1, 3, 3, 1, 1]
    ]
}
