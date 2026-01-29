import arcade
import random
from constants import *
from characters import *


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        # אתחול רשימות הספריטים
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()  # רשימת הלבבות לתצוגה

        self.player = None
        self.game_over = False
        self.start_x = 0
        self.start_y = 0

        # טעינת מוזיקת רקע
        try:
            self.background_music = arcade.load_sound("Pac-Man intro music.mp3")
        except:
            self.background_music = None
            print("Warning: Music file not found.")

        self.music_player = None

    def setup(self):
        map_width = len(LEVEL_MAP[0]) * TILE_SIZE
        map_height = len(LEVEL_MAP) * TILE_SIZE

        # חישוב המרחק כדי למרכז את המפה במסך
        self.offset_x = (self.window.width - map_width) // 2
        self.offset_y = (self.window.height - map_height) // 2

        # איפוס רשימות
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()

        self.game_over = False

        # ניהול מוזיקה
        if self.background_music and not self.music_player:
            self.music_player = self.background_music.play(volume=0.4, loop=True)

        # יצירת המבוך לפי המפה ב-constants.py
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

        # יצירת הלבבות (חיים) - מוגדלים
        if self.player:
            for i in range(self.player.lives):
                # scale=0.15 הופך אותם לגדולים וברורים
                heart = arcade.Sprite("pngegg.png", scale=0.08)
                # רווח של 60 פיקסלים בין לב ללב
                heart.center_x = 50 + (i * 45)
                # מיקום מתחת לטקסט הניקוד
                heart.center_y = self.window.height - 80
                self.heart_list.append(heart)

    def on_draw(self):
        self.clear()

        # ציור כל האלמנטים
        self.wall_list.draw()
        self.coin_list.draw()
        self.apple_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        self.heart_list.draw()  # ציור הלבבות שנותרו

        # כתיבת הניקוד
        arcade.draw_text(f"Score: {self.player.score}", 10, self.window.height - 30,
                         arcade.color.WHITE, 16, bold=True)

        # הודעות סיום משחק
        if self.game_over:
            if len(self.coin_list) != 0:
                arcade.draw_text("GAME OVER", self.window.width / 2, self.window.height / 2,
                                 arcade.color.RED, 40, align="center", anchor_x="center")
            else:
                arcade.draw_text("YOU WON!", self.window.width / 2, self.window.height / 2,
                                 arcade.color.GREEN, 40, align="center", anchor_x="center")

    def on_key_press(self, key, modifiers):
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

    def on_update(self, delta_time):
        if self.game_over:
            return

        # עדכון שחקן ומניעת מעבר דרך קירות
        old_x, old_y = self.player.center_x, self.player.center_y
        self.player.update()
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x, self.player.center_y = old_x, old_y

        # עדכון רוחות
        for ghost in self.ghost_list:
            g_old_x, g_old_y = ghost.center_x, ghost.center_y
            ghost.update(delta_time, self.player.power_mode)
            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x, ghost.center_y = g_old_x, g_old_y
                ghost.pick_new_direction()

        # איסוף מטבעות
        hit_coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_coins:
            self.player.score += 1
            coin.remove_from_sprite_lists()

        if len(self.coin_list) == 0:
            self.game_over = True

        # איסוף תפוח (Power Mode)
        hit_apples = arcade.check_for_collision_with_list(self.player, self.apple_list)
        for apple in hit_apples:
            apple.remove_from_sprite_lists()
            self.player.power_mode = True
            self.player.power_time = 5.0

        if self.player.power_mode:
            self.player.power_time -= delta_time
            if self.player.power_time <= 0:
                self.player.power_mode = False

        # בדיקת התנגשות עם רוחות
        ghost_hit_list = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        if ghost_hit_list:
            if self.player.power_mode:
                # פקמן חזק - הרוחות חוזרות להתחלה
                for ghost in ghost_hit_list:
                    ghost.center_x, ghost.center_y = self.start_x, self.start_y
                    self.player.score += 10
            else:
                # פקמן חלש - איבוד חיים ולב מהתצוגה
                self.player.lives -= 1
                if len(self.heart_list) > 0:
                    self.heart_list.pop()  # מסיר את הלב האחרון מהמסך

                # החזרת שחקן להתחלה
                self.player.center_x, self.player.center_y = self.start_x, self.start_y
                self.player.change_x, self.player.change_y = 0, 0

                if self.player.lives <= 0:
                    self.game_over = True