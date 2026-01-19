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
        self.start_x = 0
        self.start_y = 0

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
            arcade.draw_text("GAME OVER",self.window.width / 2,self.window.height / 2,arcade.color.RED,40,)

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
        if key==arcade.key.DOWN or key ==arcade.key.UP:
            self.player.change_y=0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x=0
