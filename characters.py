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
    def __init__(self, x_center, y_center, value=10):
        super().__init__("assets/coin.png", scale=0.5)
        self.center_x = x_center
        self.center_y = y_center
        self.value = value

class Wall(arcade.Sprite):
    def __init__(self, x_center, y_center):
        super().__init__("assets/wall.png", scale=0.5)
        self.center_x = x_center
        self.center_y = y_center


class Character(arcade.Sprite):
    def __init__(self, image_path, x_center, y_center, speed=1):
        super().__init__(image_path, scale=0.5)
        self.center_x = x_center
        self.center_y = y_center
        self.speed = speed
        self.change_x = 0
        self.change_y = 0

class Player(Character):
    def __init__(self, x_center, y_center, speed=2):
        super().__init__("assets/pacman.png", x_center, y_center, speed)
        self.score = 0
        self.lives = 3

    def update(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, x_center, y_center, speed=1):
        super().__init__("assets/ghost.png", x_center, y_center, speed)
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
