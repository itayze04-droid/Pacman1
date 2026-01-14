import arcade
from constants import LEVEL_MAP
from constants import TILE_SIZE
from constants import rows
from characters import Wall, Coin, Player, Enemy
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
        arcade.clear()

        arcade.draw_text(f"Score: {self.player.score}",10,self.window.height - 30,arcade.color.WHITE,16)
        arcade.draw_text(f"Lives: {self.player.lives}",10,self.window.height - 55,arcade.color.WHITE,16)
        if self.game_over:
            arcade.draw_text("GAME OVER",self.window.width / 2,self.window.height / 2,arcade.color.RED,40,)