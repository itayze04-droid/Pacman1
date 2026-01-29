import arcade
from constants import *
from characters import *

"""
מודול הלוגיקה הראשית של משחק הפקמן.

מכיל את המחלקה:
- PacmanGame: ניהול מצב המשחק, ציור, עדכון ותשובת מקלדת.
"""

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list = []
        self.coin_list = []
        self.ghost_list = []
        self.player_list = []
        self.apple_list = []
        self.object_list = None
        self.player = None
        self.game_over = False
        self.start_x = TILE_SIZE + 18
        self.start_y = TILE_SIZE + 18
        self.background_music=arcade.load_sound("Pac-Man intro music.mp3")

    def setup(self):
        map_width = len(LEVEL_MAP[0]) * TILE_SIZE
        map_height = len(LEVEL_MAP) * TILE_SIZE

        self.offset_x = (self.window.width - map_width) // 2
        self.offset_y = (self.window.height - map_height) // 2
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.game_over = False
        self.music_player = self.background_music.play(
            volume=0.4,
            loop=True
        )

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2 + self.offset_x
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2 + self.offset_y

                if cell == "#":
                    self.wall_list.append(Wall(x, y))
                elif cell == ".":
                    self.coin_list.append(Coin(x, y))
                elif cell == "P":
                    self.player = Player(x, y)
                    self.player_list.append(self.player)
                    self.start_x = x
                    self.start_y = y

                elif cell == "G":
                    self.ghost_list.append(Enemy(x, y))
                elif cell == "A":
                    self.apple_list.append(Apple(x, y))
        self.map_left = self.offset_x
        self.map_right = self.offset_x + MAP_WIDTH_PIXELS
        self.map_bottom = self.offset_y
        self.map_top = self.offset_y + MAP_HEIGHT_PIXELS

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        self.apple_list.draw()

        arcade.draw_text(f"Score: {self.player.score}", 10, self.window.height - 30, arcade.color.WHITE, 16)
        arcade.draw_text(f"Lives: {self.player.lives}", 10, self.window.height - 55, arcade.color.WHITE, 16)

        if self.game_over and len(self.coin_list) != 0:
            arcade.draw_text("GAME OVER", self.window.width / 2 - 145, self.window.height / 2, arcade.color.RED, 40)
        if len(self.coin_list) == 0:
            arcade.draw_text("YOU WON!", self.window.width / 2 - 145, self.window.height / 2, arcade.color.GREEN, 40)
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_x = 0
            self.player.change_y = 1
        elif key == arcade.key.S:
            self.player.change_x = 0
            self.player.change_y = -1
        elif key == arcade.key.A:
            self.player.change_x = -1
            self.player.change_y = 0
        elif key == arcade.key.D:
            self.player.change_x = 1
            self.player.change_y = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

    def on_update(self, delta_time):
        if self.game_over:
            return

        old_x = self.player.center_x
        old_y = self.player.center_y
        self.player.update()
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = old_x
            self.player.center_y = old_y

            if self.player.center_x < self.map_left:
                self.player.center_x = self.map_right
            elif self.player.center_x > self.map_right:
                self.player.center_x = self.map_left

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = old_x
            self.player.center_y = old_y

        for ghost in self.ghost_list:
            ghost_old_x = ghost.center_x
            ghost_old_y = ghost.center_y
            ghost.update(delta_time, self.player.power_mode)

            if ghost.center_x < self.map_left:
                ghost.center_x = self.map_right
            elif ghost.center_x > self.map_right:
                ghost.center_x = self.map_left

            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x = ghost_old_x
                ghost.center_y = ghost_old_y
                ghost.pick_new_direction()

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = old_x
            self.player.center_y = old_y

        hit_coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_coins:
            self.player.score += 1
            coin.remove_from_sprite_lists()

        hit_apples = arcade.check_for_collision_with_list(self.player, self.apple_list)
        for apple in hit_apples:
            apple.remove_from_sprite_lists()
            self.player.power_mode = True
            self.player.power_time = 5.0

        if self.player.power_mode:
            self.player.power_time -= delta_time
            if self.player.power_time <= 0:
                self.player.power_mode = False

                for ghost in self.ghost_list:
                    ghost_old_x = ghost.center_x
                    ghost_old_y = ghost.center_y

                    ghost.update(delta_time, self.player.power_mode)


                    if ghost.center_x < 0:
                        ghost.center_x = MAP_WIDTH_PIXELS
                    elif ghost.center_x > MAP_WIDTH_PIXELS:
                        ghost.center_x = 0


                    if arcade.check_for_collision_with_list(ghost, self.wall_list):
                        ghost.center_x = ghost_old_x
                        ghost.center_y = ghost_old_y
                        ghost.pick_new_direction()

        if arcade.check_for_collision_with_list(self.player, self.ghost_list):
            if self.player.power_mode:
                for ghost in self.ghost_list:
                    if arcade.check_for_collision(self.player, ghost):
                        ghost.center_x = self.start_x
                        ghost.center_y = self.start_y
                        self.player.score += 10
            else:
                self.player.lives -= 1
                self.player.center_x = self.start_x
                self.player.center_y = self.start_y
                self.player.change_x = 0
                self.player.change_y = 0
                if self.player.lives <= 0:
                    self.game_over = True
                    arcade.stop_sound(self.music_player)
