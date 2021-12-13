import pygame.font

class Button():
    """Handling the game button"""
    def __init__(self, ai_game, screen, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.scree.get_rect()

        # Defining dimensions of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # Green
        self.text_color = (255, 255, 255)  # White
        self.font = pygame.font.SysFont(None, 48)

        # Displaying the button in the middle of the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        """Displaying a centered text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Displaying an empty button on the screen and filling it with text"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)