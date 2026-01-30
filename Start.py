import arcade
from game import PacmanGame
from constants import WINDOW_TITLE

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        # כותרת
        arcade.draw_text(
            "PACMAN",
            self.window.width // 2,
            self.window.height // 2 + 80,
            arcade.color.YELLOW,
            60,
            anchor_x="center",
            bold=True
        )

        # הוראות
        arcade.draw_text(
            "Press ENTER to start",
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC to exit",
            self.window.width // 2,
            self.window.height // 2 - 40,
            arcade.color.GRAY,
            16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = PacmanGame()
            game_view.setup()
            self.window.show_view(game_view)

        elif key == arcade.key.ESCAPE:
            arcade.exit()
