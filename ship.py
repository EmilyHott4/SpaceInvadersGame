import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        #display number of ships
        super().__init__()
        self.screen = ai_game.screen

        #adj. ship speed (1)
        
        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()

       
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #_____start each new ship at the bottom center of the screen. 
        self.rect.midbottom = self.screen_rect.midbottom

        #adj. ship speed (2) - store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        #____movement flags
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """_____Update the ship's position based on the movement flag."""
        ##if self.moving_right:
            ##self.rect.x += 1

        #update the ship's x value, not the rect.

        #limit the ship's range (1)
        if self.moving_right and self.rect.right < self.screen_rect.right:
             #adj. ship speed (3) 
            self.x += self.settings.ship_speed

        ##if self.moving_left:
            ##self.rect.x -= 1

        #limit the ship's range (2)
        if self.moving_left and self.rect.left > 0:
            #adj. ship speed (3)
            self.x -= self.settings.ship_speed
        
        #adj. ship speed (4) - update rect obj. from self.x
        self.rect.x =self.x
    
    def blitme(self):
        """____Draw the ship at its current location (midbottom)."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
