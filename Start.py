import arcade
from game import PacmanGame
from constants import *


class StartView(arcade.View):
    def __init__(self):
        super().__init__()

        self.title_text = arcade.Text(
            "PACMAN", 0, 0, arcade.color.YELLOW, 60, anchor_x="center", bold=True
        )
        self.button_label = arcade.Text(
            "START GAME", 0, 0, arcade.color.BLACK, 20, anchor_x="center", anchor_y="center"
        )
        self.button_w, self.button_h = 200, 60
        self.button_x = 0
        self.button_y = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()


        cx = self.window.width / 2
        cy = self.window.height / 2


        self.title_text.position = (cx, cy + 100)
        self.title_text.draw()


        self.button_x = cx - self.button_w / 2
        self.button_y = cy - self.button_h / 2


        arcade.draw_rect_filled(
            arcade.rect.XYWH(cx, cy, self.button_w, self.button_h),
            arcade.color.GREEN
        )


        self.button_label.position = (cx, cy)
        self.button_label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.button_x <= x <= self.button_x + self.button_w and
                self.button_y <= y <= self.button_y + self.button_h):

            game_view = PacmanGame()
            game_view.setup()
            self.window.show_view(game_view)