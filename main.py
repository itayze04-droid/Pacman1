import arcade
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from game import PacmanGame
from Start import *

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    start_view = StartView()
    window.show_view(start_view)

    arcade.run()

if __name__ == "__main__":
    main()
