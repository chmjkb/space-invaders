import pygame

import os

from settings import Settings


class Ship:
    """Class designed to manage the ship"""

    def __init__(self, ai_game):
        """Initializing the space ship and its default location"""

        self.screen = ai_game.screen
        self.settings = Settings()
        self.screen_rect = ai_game.screen.get_rect()

        # Loading the spaceship image and getting its rect
        self.image = pygame.image.load(os.path.join('images', 'ship.png'))
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect()

        # Every new spaceship will be displayed on the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Storing the placement of ship to the float variable
        self.x = float(self.rect.x)

        # Variables showing if the ship is moving towards the right side
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Moving the ship"""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Updating rect placemen t based on self.x value
        self.rect.x = self.x

    def blitme(self):
        """Displaying the spaceship in the right place"""

        self.screen.blit(self.image, self.rect)
