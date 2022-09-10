import pyglet

class Game_client():
    def __init__(self) -> None:
        self.screen_width = 1080
        self.screen_height = 720
        self.window = pyglet.window.Window()


    def run(self) -> None:
        pyglet.app.run()


if __name__ == "__main__":
    game = Game_client()
    game.run()
