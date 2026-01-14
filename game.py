import arcade
from constants import LEVEL_MAP
from constants import TILE_SIZE
from constants import rows

"""
מודול הלוגיקה הראשית של משחק הפקמן.

מכיל את המחלקה:
- PacmanGame: ניהול מצב המשחק, ציור, עדכון ותשובת מקלדת.
"""
class PacmanGame(arcade.View):
    def __init__(self, object_list=None, player=None, game_over=False):
        super().__init__()
        self.list_wall = []
        self.list_coin = []
        self.list_ghost = []
        self.list_player = []
        self.object_list = object_list
        self.player = player
        self.game_over = game_over

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
                    self.list_wall.append((x, y))
                elif cell == ".":
                    self.list_coin.append((x, y))
                elif cell == "P":
                    self.list_player = (x, y)
                elif cell == "G":
                    self.list_ghost.append((x, y))

    def on_draw(self):
        self.clear()
        self.list_wall.draw()
        self.list_coin.draw()
        self.list_ghost.draw()
        self.list_player.draw()
        self.game_over.draw()
