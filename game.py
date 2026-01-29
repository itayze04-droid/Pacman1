import arcade
import random
from constants import *
from characters import *


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()

        self.player = None
        self.game_over = False
        self.start_x = 0
        self.start_y = 0
        self.background_music = arcade.load_sound("man-theme-original (mp3cut.net).mp3")
        self.music_player = None
        self.coin_icon = arcade.load_texture("coin.png")
        self.game_over_sound=arcade.load_sound("Pac Man Death Sound FX.mp3")
        self.win_sound=arcade.load_sound("win_sound.mp3")
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            button_left = self.window.width / 2 - 100
            button_right = self.window.width / 2 + 100
            button_bottom = self.window.height / 2 - 65
            button_top = self.window.height / 2 - 15

            if button_left < x < button_right and button_bottom < y < button_top:
                self.setup()

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
        self.heart_list = arcade.SpriteList()

        self.game_over = False

        if self.background_music and not self.music_player:
            self.music_player = self.background_music.play(volume=0.4, loop=True)

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
        if self.player:
            for i in range(self.player.lives):
                heart = arcade.Sprite("pngegg.png", scale=0.08)
                heart.center_x = 50 + (i * 45)
                heart.center_y = self.window.height - 80
                self.heart_list.append(heart)

    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.apple_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        self.heart_list.draw()


        arcade.draw_texture_rect(
            texture=self.coin_icon,
            rect=arcade.rect.XYWH(30, self.window.height - 30, 25, 25)
        )


        arcade.draw_text(
            f"{self.player.score}",
            55,
            self.window.height - 42,
            arcade.color.WHITE,
            20,
            bold=True
        )


        arcade.draw_text(f"{self.player.score}", 55, self.window.height - 42, arcade.color.WHITE, 20, bold=True)
        if self.game_over:
            if len(self.coin_list) != 0:
                arcade.draw_text("GAME OVER", self.window.width / 2, self.window.height / 2+400,
                                 arcade.color.RED, 80, align="center", anchor_x="center")
            else:
                arcade.draw_text("YOU WON!", self.window.width / 2, self.window.height / 2+400,
                                 arcade.color.GREEN, 80, align="center", anchor_x="center")



    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.W:
            self.player.change_x, self.player.change_y = 0, 1
        elif key == arcade.key.S:
            self.player.change_x, self.player.change_y = 0, -1
        elif key == arcade.key.A:
            self.player.change_x, self.player.change_y = -1, 0
        elif key == arcade.key.D:
            self.player.change_x, self.player.change_y = 1, 0

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.S]:
            self.player.change_y = 0
        if key in [arcade.key.A, arcade.key.D]:
            self.player.change_x = 0

    def get_random_free_position(self):
        while True:
            row = random.randint(0, len(LEVEL_MAP) - 1)
            col = random.randint(0, len(LEVEL_MAP[0]) - 1)
            if LEVEL_MAP[row][col] != "#":
                x = col * TILE_SIZE + TILE_SIZE / 2 + self.offset_x
                y = (rows - row - 1) * TILE_SIZE + TILE_SIZE / 2 + self.offset_y
                return x, y


    def on_update(self, delta_time):
        if self.game_over:
            return

        old_x, old_y = self.player.center_x, self.player.center_y
        self.player.update()
        if self.player.center_x < self.map_left:
            self.player.center_x = self.map_right - TILE_SIZE

        elif self.player.center_x > self.map_right:
            self.player.center_x = self.map_left + TILE_SIZE
        self.player.center_x = max(self.map_left, min(self.player.center_x, self.map_right))
        self.player.center_y = max(self.map_bottom, min(self.player.center_y, self.map_top))
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x, self.player.center_y = old_x, old_y

        for ghost in self.ghost_list:
            g_old_x, g_old_y = ghost.center_x, ghost.center_y
            ghost.update(delta_time, self.player.power_mode)

            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x, ghost.center_y = g_old_x, g_old_y
                ghost.pick_new_direction()

            if ghost.center_x < self.offset_x:
                ghost.center_x = self.offset_x + MAP_WIDTH_PIXELS
            elif ghost.center_x > self.offset_x + MAP_WIDTH_PIXELS:
                ghost.center_x = self.offset_x

            if ghost.center_y < self.offset_y:
                ghost.center_y = self.offset_y + MAP_HEIGHT_PIXELS
            elif ghost.center_y > self.offset_y + MAP_HEIGHT_PIXELS:
                ghost.center_y = self.offset_y

        hit_coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_coins:
            self.player.score += 1
            coin.remove_from_sprite_lists()

        if len(self.coin_list) == 0:
            if not self.game_over:
                self.game_over = True
                if self.music_player:
                    arcade.stop_sound(self.music_player)
                arcade.play_sound(self.win_sound)

        hit_apples = arcade.check_for_collision_with_list(self.player, self.apple_list)
        for apple in hit_apples:
            apple.remove_from_sprite_lists()
            self.player.power_mode = True
            self.player.power_time = 5.0

        if self.player.power_mode:
            self.player.power_time -= delta_time
            if self.player.power_time <= 0:
                self.player.power_mode = False


        ghost_hit_list = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        if ghost_hit_list:
            if self.player.power_mode:
                for ghost in ghost_hit_list:
                    new_x, new_y = self.get_random_free_position()
                    ghost.center_x = new_x
                    ghost.center_y = new_y
                    self.player.score += 10
            else:
                self.player.lives -= 1
                if len(self.heart_list) > 0:
                    self.heart_list.pop()

                self.player.center_x, self.player.center_y = self.start_x, self.start_y
                self.player.change_x, self.player.change_y = 0, 0

                if self.player.lives <= 0:

                    arcade.stop_sound(self.music_player)
                    arcade.play_sound(self.game_over_sound)
                    self.game_over = True
