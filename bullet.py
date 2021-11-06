import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class designed to manage bullets"""

    def __init__(self, game):
        """Creating an object of a bullet"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Creating a rectangle at (0, 0) and then changing its position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        # Position of the bullet is defined in a float variable
        self.y = float(self.rect.y)

    def update(self):
        """Handling the movement of the bullet"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Displaying the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
    