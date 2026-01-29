import arcade
from game import PacmanGame



class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        # הגדרת כפתור ה-PLAY במרכז המסך
        self.play_btn = {"x": 300, "y": 250, "w": 200, "h": 60}

    def on_show_view(self):
        # צבע רקע למסך הפתיחה
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        # כותרת המשחק
        arcade.draw_text("PACMAN", self.window.width / 2, 400,
                         arcade.color.YELLOW, 60, anchor_x="center")

        # ציור כפתור ה-PLAY (מלבן ירוק)
        arcade.draw_lrbt_rectangle_filled(self.play_btn["x"],
                                          self.play_btn["x"] + self.play_btn["w"],
                                          self.play_btn["y"],
                                          self.play_btn["y"] + self.play_btn["h"],
                                          arcade.color.GREEN)

        # טקסט על הכפתור
        arcade.draw_text("PLAY",
                         self.play_btn["x"] + self.play_btn["w"] / 2,
                         self.play_btn["y"] + self.play_btn["h"] / 2,
                         arcade.color.BLACK, 25, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # בדיקה אם הלחיצה הייתה בתוך אזור הכפתור
        if (self.play_btn["x"] <= x <= self.play_btn["x"] + self.play_btn["w"] and
                self.play_btn["y"] <= y <= self.play_btn["y"] + self.play_btn["h"]):
            # מעבר למשחק עצמו
            game_view = PacmanGame()
            game_view.setup()
            self.window.show_view(game_view)


# --- הרצת האפליקציה ---
if __name__ == "__main__":
    window = arcade.Window(800, 600, "Pacman Game")
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()