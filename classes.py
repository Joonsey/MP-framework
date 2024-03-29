import pyglet
from pyglet.window import key
from pyglet import shapes

from network import Network_client
from tools import ASSET_DICT, TILE_SIZE

PLAYER_WIDTH=16
PLAYER_HEIGHT=16
CONST_MOVEMENT_SPEED = 5
SPEED = [0,0]

class Player:
    def __init__(self, img, x, y, batch=None) -> None:
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(img, x, y, batch=batch)
        self.direction = 0
        self.new_direction = 0
        self.images = [img.get_transform(True), img]
        self.is_coliding = False
        self.physics_obj = Physics_object(x, y, self.sprite.width, self.sprite.height)
        self.objects_to_collide_with = []
        self.other_players = []


    def update_pos(self):
        self.sprite.update(x=self.x, y=self.y)
        self.physics_obj.xpos = self.x
        self.physics_obj.ypos = self.y

    def update(self, keyboard, dt):
        if self.physics_obj.is_coliding_with_list_of_objs(self.objects_to_collide_with):
            self.is_coliding = True
            self.change_color((255,0,0))
        elif self.physics_obj.is_coliding_with_list_of_objs(self.other_players):
            self.is_coliding = True
            self.change_color((0,0,255))
        else:
            self.is_coliding = False
            self.change_color((255,255,255))
        self.input_handler(keyboard, dt)
        self.change_direction(self.new_direction)
        self.update_pos()

    def change_direction(self, direction):
        if direction != self.direction:
            self.direction = direction
            self.sprite.image = self.images[direction]

    def input_handler(self, keyboard, dt):
        if keyboard[key.D]:
            SPEED[0] = 1
            self.new_direction = 1
        elif keyboard[key.A]:
            SPEED[0] = -1
            self.new_direction = 0
        else:
            SPEED[0] = 0

        if keyboard[key.W]:
            SPEED[1] = 1
        elif keyboard[key.S]:
            SPEED[1] = -1
        else:
            SPEED[1] = 0

        if keyboard[key.E]:
            #play_sound(max_mekker)
            pass
        if keyboard[key.F]:
            self.change_color((255,0,255))

        # update_pos is being used to synchronize the new calculated position to then check for colision
        self.x += SPEED[0] * 5
        self.update_pos()
        if self.physics_obj.is_coliding_with_list_of_objs(self.objects_to_collide_with):
            # horizontal colision detected
            self.x -= SPEED[0] * 5

        self.y += SPEED[1] * 5
        self.update_pos()
        if self.physics_obj.is_coliding_with_list_of_objs(self.objects_to_collide_with):
            # vertical colision detected
            self.y -= SPEED[1] * 5

    def get_color_in_bytes(self) -> bytes:
        colors = self.sprite.color
        color_in_bytes = b""
        for color in colors:
            color_in_bytes += color.to_bytes(1, 'little')
        return color_in_bytes

    def set_color_from_bytes(self, color: bytes | list[int]):
        new_color = color
        if type(color) == bytes:
            r = color[0]
            g = color[1]
            b = color[2]
            new_color = [r,g,b]
        self.change_color(tuple(new_color))

    def change_color(self, color: tuple):
        self.sprite.color = color
        self.sprite._update_color()

class Physics_object:
    #TODO DEBUG AND TEST THIS ENTIRE THING PLX THANKS 🧓🧓
    def __init__(self, xpos: int, ypos: int, width: int, height: int) -> None:
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

    def is_coliding_with_list_of_objs(self, colliders: list) -> list:
        object_collided_with = []
        for obj in colliders:
            if obj.is_colliding_with_obj(self):
                object_collided_with.append(obj)
        return object_collided_with

    def is_colliding_with_obj(self, obj) -> bool:
        colided = False
        if (obj.xpos <= self.xpos + self.width and
                obj.xpos >= self.xpos and
                obj.ypos <= self.ypos + self.height and
                obj.ypos >= self.ypos):
            colided = True

        return colided

class Level:
    """isometric lvl?"""
    def __init__(self, amount_of_x_tiles: int, amount_of_y_tiles: int, left_padding:int | float = 0, bottom_padding:int | float = 0) -> None:
        self.x_amount = amount_of_x_tiles
        self.y_amount = amount_of_y_tiles
        self.tiles = []
        self.left_padding = left_padding
        self.bottom_padding = bottom_padding
        self.collision_tiles = []


    def draw_level(self, seed: list[list[int]] | None = None, batch=None):
        if not seed:
            pass
        else:
            for y in range(0, len(seed)):
                for x in range(0, len(seed[y])):
                    current_val = seed[len(seed) - (y+1)][x]
                    xpos = TILE_SIZE * x
                    ypos = TILE_SIZE * y
                    tile = Tile(xpos,ypos, current_val, batch=batch)
                    self.tiles.append(tile)
                    if not current_val: self.collision_tiles.append(tile.physics_obj)

    def update_level_pos_with_respect_to_padding(self, left_padding, bottom_padding):
        for tile in self.tiles:
            tile.update_pos_with_respect_to_padding(left_padding, bottom_padding)

class Tile:
    """tile"""
    def __init__(self, xpos, ypos, kind, batch=None, **kwargs) -> None:
        if not kind:
            self.sprite = None
        else:
            img = ASSET_DICT['tiles'][kind]
            self.sprite = pyglet.sprite.Sprite(img, xpos, ypos, batch=batch)
        self.xpos = xpos
        self.ypos = ypos
        self.kind = kind
        self.physics_obj = Physics_object(xpos, ypos, TILE_SIZE, TILE_SIZE)
        self.left_padding = 0
        self.bottom_padding = 0

    def update_pos_with_respect_to_padding(self, left_padding, bottom_padding):
        self.update_pos(self.xpos - self.left_padding + left_padding,
                        self.ypos - self.bottom_padding + bottom_padding)
        self.left_padding = left_padding
        self.bottom_padding = bottom_padding

    def update_pos(self, x, y):
        self.xpos = x
        self.ypos = y
        self.physics_obj.xpos = x
        self.physics_obj.ypos = y
        if self.sprite:
            self.sprite.x = x
            self.sprite.y = y

class Particle:
    def __init__(self, xpos, ypos, velocity, lifespan,radius=3, color=(124,222,85), batch=None) -> None:
        self.xpos = xpos
        self.ypos = ypos
        self.velocity = velocity
        self.lifespan = lifespan
        self.texture = shapes.Circle(xpos, ypos, radius=radius, color=color, batch=batch)

    def update_pos(self, x, y):
        self.xpos = x
        self.ypos = y
        self.texture.x = x
        self.texture.y = y

class Light_particle(Particle):
    def __init__(self, xpos, ypos, velocity, lifespan, radius=3, color=(124, 222, 85), batch=None) -> None:
        super().__init__(xpos, ypos, velocity, lifespan, radius, color, batch)
        self.outer_texture = shapes.Circle(xpos, ypos, radius*4.5, batch=batch)
        self.outer_texture.opacity = 25

    def update_pos(self, x, y):
        self.outer_texture.x = x
        self.outer_texture.y = y
        return super().update_pos(x, y)

class Moving_particle(Particle):
    def __init__(self, xpos, ypos, width, height, velocity, lifespan, color=(124, 222, 85), batch=None) -> None:
        self.xpos = xpos
        self.ypos = ypos
        self.velocity = velocity
        self.lifespan = lifespan
        self.texture = shapes.Rectangle(xpos, ypos, width, height, color, batch=batch)


