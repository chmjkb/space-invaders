class GameStats:
    """Monitoring stats in the game"""

    def __init__(self, ai_game):
        """Initializing the variables"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Initializing variables which could change during the game"""
        self.ships_left = self.settings.ship_limit

