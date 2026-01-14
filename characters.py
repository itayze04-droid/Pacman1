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
from pygame.examples.multiplayer_joystick import player

from constants import TILE_SIZE


class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(TILE_SIZE//10, arcade.color.GOLD)
        self.center_x = x
        self.center_y = y
        self.width=TILE_SIZE//5
        self.height=TILE_SIZE//5




class Wall(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_rectangle_texture(TILE_SIZE, TILE_SIZE,arcade.color.BLUE)
        self.center_x = x
        self.center_y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE



class Character(arcade.Sprite):
    def __init__(self, x, y, texture):
        super().__init__()
        self.texture = texture
        self.center_x = x
        self.center_y = y
        self.speed = 2
        self.change_x = 0
        self.change_y = 0
        self.width = TILE_SIZE // 7
        self.height = TILE_SIZE // 7


player_texture=arcade.make_circle_texture(TILE_SIZE//7,arcade.color.PURPLE)
class Player(Character):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center,player_texture)
        self.score = 0
        self.lives = 3


    def update(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
enemy_texture=arcade.make_circle_texture(TILE_SIZE//7,arcade.color.RED)
class Enemy(Character):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center,enemy_texture)
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
