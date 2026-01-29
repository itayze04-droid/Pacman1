import arcade
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from game import PacmanGame

"""
נקודת הכניסה למשחק פקמן.

אחראית על:
- יצירת חלון Arcade
- יצירת אובייקט PacmanGame
- אתחול המשחק
- הרצת לולאת המשחק
"""

def main():
    """פונקציית main שמריצה את המשחק."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True)
    view = PacmanGame()
    view.setup()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
