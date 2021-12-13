import sys
from time import sleep

import pygame
from pygame import mouse

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien



class AlienInvasion:
    """Main class created to manage the game"""

    def __init__(self):
        """Initializing main variables and the game itself"""

        pygame.init()
        pygame.display.set_caption("Space Invaders")

        # Screen size
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Creating an instance of Settings class
        self.settings = Settings()

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Creating an instance of GameStats class
        self.stats = GameStats(self)

        # Creating an instance of Ship class
        self.ship = Ship(self)

        # Background color (navy blue)
        self.bg_color = self.settings.bg_color

        # Creating sprite groups
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Creating Play button
        self.play_button = Button(self, self.screen, "Play")

    def run_game(self):
        """Starting the mainloop"""

        while True:
            # Waiting for events
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self.update_screen()

    def _check_events(self):
        """Reacting to events generated by keyboard and a mouse"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Beginning a new game if the player pressed on the button"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Reaction to key being pressed"""

        if event.key == pygame.K_RIGHT:
            # Moving the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reaction to key being released"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Displaying bullets on the screen"""

        # Setting the bullet limit
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Handling the bullets"""

        self.bullets.update()
        # Deleting bullets which are not on the screen anymore
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Reacting to bullet-alien collision"""

        # Checking if any bullet collided with an alien, if so, deleting both the alien and the bullet
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:  # Checking if there are any aliens left on the screen
            self.bullets.empty()
            self._create_fleet()  # If the fleet is dead, displaying a new one

    def _create_fleet(self):
        """Creating aliens fleet"""

        # Creating an alien
        # The distance between aliens is equal to the aliens width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Defining the amount of rows that will fit the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creating the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Creating a new alien"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Updating the placement of every alien in the fleet and changing its direction"""

        self._check_fleet_edges()
        self.aliens.update()

        # Detecting collisions between the spaceship and aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Looking for aliens at the bottom of a screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Reacting to aliens reaching the edge of a screen"""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Moving the aliens down and changing moving direction"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reacting to the ship being hit"""
        self.stats.ships_left -= 1

        # Deleting aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Creating new fleet and centering the ship
        self._create_fleet()
        self.ship.center_ship()
        sleep(1)

    def _check_aliens_bottom(self):
        """Checking if any of the aliens have reached the bottom of the screen"""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def update_screen(self):
        """Updating the pictures on the screen and coming onto the next picture"""

        # Refreshing the screen with every loop iteration
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Displaying the last modified frame
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
