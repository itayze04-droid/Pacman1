import arcade
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