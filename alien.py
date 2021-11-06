import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class displaying a single alien"""

    def __init__(self, ai_game):
        """Initializing the alien"""

        super().__init__()
        self.screen = ai_game.screen

        # Loading the alien image
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        # Setting the alien location close to the left top corner of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Storing the x value as a float
        self.x = float(self.rect.x)
