class Settings:
    """Class designed to keep the settings of a game"""

    def __init__(self):
        """Initializing variables"""

        # Screen settings
        self.screen_width = 900
        self.screen_height = 500

        # Background color (olive ish)
        self.bg_color = (75, 108, 0)
        # Ship moving speed
        self.ship_speed = 1.5

        # Bullet-related settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (244, 108, 0)  # Orange
        self.bullets_allowed = 3  # This allows the player to shoot only 3 bullets at a time

        # Alien related settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 stands for right, -1 stands for left
