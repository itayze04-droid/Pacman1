import random
import arcade
from constants import TILE_SIZE

class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(TILE_SIZE//2 - 6, arcade.color.GOLD)
        self.center_x = x
        self.center_y = y

class Wall(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BLUE, 255)
        self.center_x = x
        self.center_y = y

class Apple(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(TILE_SIZE//2 - 4, arcade.color.RED)
        self.center_x = x
        self.center_y = y

class Character(arcade.Sprite):
    def __init__(self, x, y, texture):
        super().__init__()
        self.texture = texture
        self.center_x = x
        self.center_y = y
        self.speed = 2
        self.change_x = 0
        self.change_y = 0

player_texture = arcade.make_circle_texture(TILE_SIZE-6, arcade.color.PURPLE)
class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, player_texture)
        self.score = 0
        self.lives = 3
        self.power_mode = False
        self.power_time = 0.0

    def update(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

enemy_texture = arcade.make_soft_square_texture(TILE_SIZE-6, arcade.color.RED, 255)
ghost_power_texture = arcade.make_soft_square_texture(TILE_SIZE-6, arcade.color.LIGHT_BLUE, 255)
class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_texture)
        self.direction_change_time = 0

    def pick_new_direction(self):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        self.change_x, self.change_y = random.choice(directions)
        self.direction_change_time = random.uniform(0.3, 1.0)

    def update(self, delta_time=1/60, power_mode=False):
        self.direction_change_time -= delta_time
        if self.direction_change_time <= 0:
            self.pick_new_direction()

        if power_mode:
            self.texture = ghost_power_texture
            speed_multiplier = 0.5
        else:
            self.texture = enemy_texture
            speed_multiplier = 1.0

        self.center_x += self.change_x * self.speed * speed_multiplier
        self.center_y += self.change_y * self.speed * speed_multiplier
