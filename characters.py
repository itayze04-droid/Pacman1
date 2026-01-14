"""
מודול הדמויות (Sprites) במשחק פקמן.

מכיל את המחלקות:
- Character: מחלקת בסיס לדמויות (שיתוף שדה speed וכו')
- Pacman: השחקן הראשי
- Ghost: רוחות שנעות בצורה רנדומלית
- Coin: מטבעות לאיסוף
- Wall: קירות שחוסמים תנועה
"""
import random
import arcade

class Coin(arcade.Sprite):
    def __init__(self, x_center, y_center):
        super().__init__()
        self.center_x = x_center
        self.center_y = y_center
        self.size = 20
        self.color = arcade.color.GOLD
        self.value = 10

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.size / 2, self.color)

class Wall(arcade.Sprite):
    def __init__(self, x_center, y_center):
        super().__init__()
        self.center_x = x_center
        self.center_y = y_center
        self.width = 32
        self.height = 32
        self.color = arcade.color.BLUE

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

class Character(arcade.Sprite):
    def __init__(self, x_center, y_center):
        super().__init__()
        self.center_x = x_center
        self.center_y = y_center
        self.speed = 1
        self.change_x = 0
        self.change_y = 0
        self.size = 28
        self.color = arcade.color.YELLOW

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.size / 2, self.color)

class Player(Character):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center)
        self.score = 0
        self.lives = 3
        self.color = arcade.color.YELLOW  # צבע "קבוע" של השחקן

    def update(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center)
        self.color = arcade.color.RED
        self.direction_change_time = 0

    def pick_new_direction(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.change_x, self.change_y = random.choice(directions)
        self.direction_change_time = random.uniform(0.3, 1.0)

    def update(self, time_delta=1/60):
        self.direction_change_time -= time_delta
        if self.direction_change_time <= 0:
            self.pick_new_direction()
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
