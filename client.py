import pyglet
from network import Network_client

class Game_client():
    def __init__(self) -> None:
        self.screen_width = 1080
        self.screen_height = 720
        self.window = pyglet.window.Window()
        self.network = Network_client()


    def run(self) -> None:
        pyglet.app.run()
        response = self.network.connect() # connecting to server
        assert response, """
        Response was invalid.
        error connecting to the server. Make sure the server is running
        """

if __name__ == "__main__":
    game = Game_client()
    game.run()
