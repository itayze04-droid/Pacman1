"""
מודול קבועים עבור משחק פקמן.

מכיל:
- הגדרות חלון (רוחב, גובה, כותרת)
- גודל אריח בודד במפה
- מפה לוגית (LEVEL_MAP) שמגדירה קירות, מטבעות, פקמן ורוחות.
"""
import arcade
# הגדרות חלון
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pacman Arcade Example"
SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

# גודל אריח במפה (בפיקסלים)
TILE_SIZE = 32

# מפה:
# # - קיר
# . - מטבע
# P - פקמן (נקודת התחלה לשחקן)
# G - רוח
with open("LEVEL_MAP.txt", "r") as file:
    lines = file.read().splitlines()

LEVEL_MAP = lines
# נחשב את רוחב המפה בפיקסלים לשימוש בלוגיקה
MAP_WIDTH_PIXELS = len(LEVEL_MAP[0]) * TILE_SIZE



rows = len(LEVEL_MAP)