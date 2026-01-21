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
        self.list_wall = []
        self.list_coin = []
        self.list_ghost = []
        self.list_player = []
        self.object_list = None
        self.player = None
        self.game_over = False
        self.start_x =TILE_SIZE+18
        self.start_y = TILE_SIZE+18

    def setup(self):
        self.list_wall = arcade.SpriteList()
        self.list_coin = arcade.SpriteList()
        self.list_ghost = arcade.SpriteList()
        self.list_player = arcade.SpriteList()
        self.game_over = False

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (rows - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if cell == "#":
                    self.list_wall.append(Wall(x, y))

                elif cell == ".":
                    self.list_coin.append(Coin(x, y))

                elif cell == "P":
                    self.player = Player(x, y)
                    self.list_player.append(self.player)

                elif cell == "G":
                    self.list_ghost.append(Enemy(x, y))

    def on_draw(self):
        self.clear()
        self.list_wall.draw()
        self.list_coin.draw()
        self.list_ghost.draw()
        self.list_player.draw()
        arcade.draw_text(f"Score: {self.player.score}",10,self.window.height - 30,arcade.color.WHITE,16)
        arcade.draw_text(f"Lives: {self.player.lives}",10,self.window.height - 55,arcade.color.WHITE,16)
        if self.game_over:
            arcade.draw_text("GAME OVER",self.window.width /2-150,self.window.height / 2,arcade.color.RED,40,)
        if len(self.list_coin) == 0:
            arcade.draw_text("YOU WON!", self.window.width / 2 - 150, self.window.height / 2, arcade.color.GREEN, 40, )

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


    def on_key_release(self,key, modifiers):
        if key==arcade.key.W or key ==arcade.key.S:
            self.player.change_y=0
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x=0


    def on_update(self, delta_time):
        if self.game_over:
            return
        old_x = self.player.center_x
        old_y = self.player.center_y

        self.player.update()
        if arcade.check_for_collision_with_list(self.player, self.list_wall):
            self.player.center_x = old_x
            self.player.center_y = old_y

        hit_coins = arcade.check_for_collision_with_list(self.player, self.list_coin)
        for coin in hit_coins:
            self.player.score += 1
            coin.remove_from_sprite_lists()

        for ghost in self.list_ghost:
            ghost_old_x = ghost.center_x
            ghost_old_y = ghost.center_y
            ghost.update(delta_time)

            if arcade.check_for_collision_with_list(ghost, self.list_wall):
                ghost.center_x = ghost_old_x
                ghost.center_y = ghost_old_y
                ghost.pick_new_direction()

        if arcade.check_for_collision_with_list(self.player, self.list_ghost):
            self.player.lives -= 1
            self.player.center_x = self.start_x
            self.player.center_y = self.start_y
            self.player.change_x = 0
            self.player.change_y = 0

            if self.player.lives <= 0:
                self.game_over = True
