import sys
#responding to alien and ship collisions
from time import sleep

import pygame

from settings import Settings

#responding to alien and ship collisions
from game_stats import GameStats

#making a scoreboard
from scoreboard import Scoreboard


#drawing the button to the screen
from button import Button

from ship import Ship
#firing bullet
from bullet import Bullet
#create alien instance
from alien import Alien

class AlienInvasion:
    #class create pygame window and responding to user input - inc: init the game & create the game resc.
    """Overall class to manage game assets and behavior. Settings, screen, and ship instance are created"""

    def __init__(self):
        """Initialize the game, and create game resources."""

        pygame.init()

        self.settings = Settings()

        #run game in fullscreen mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #tells pygame to figure window size to fill screen
        self.settings.screen_width = self.screen.get_rect().width #width determine will update settings obj.
        self.settings.screen_height = self.screen.get_rect().height #height detemine will update settings obj.

        ##self.screen = pygame.display.set_mode((1200, 800)) #use before setting class set-up; creates screen size
        #helps to create an instance of setting
        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game statistics and create a scoreboard

        #responding to alien and ship collisions - create an instance to store game statistics
        self.stats = GameStats(self)

        #make a scoreboard
        self.sb = Scoreboard(self)

        #draws the ship to the screen (1)
        self.ship = Ship(self)

        #storing bullets in a group
        self.bullets = pygame.sprite.Group()

        #create alien instance
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        #draw the button to the screen
        self.play_button = Button(self, "Play")

        #Set the background color
        self.bg_color = (230, 230, 230)
        

    def run_game(self):
        """start the main loop for the game."""
        while True:
            #create the check events method 
            self._check_events()

            #identifying when parts of the game should run
            if self.stats.game_active:

                #allowing continuous movement 
                self.ship.update()

                #create the _update_bullet method
                self. _update_bullets()

                #moving alien right
                self._update_aliens()

                #create the update screen method 
            self._update_screen()

    #create the check events method 
    def _check_events(self):
        #watch for the keyboard and mouse events; manage movements.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                #refactoring _check_events()
                self._check_keydown_events(event)
                
            #allow continuous movement 
            elif event.type == pygame.KEYUP:
                #refactoring _check_events()
                self._check_keyup_events(event)
            
            #starting the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

     #starting the game           
    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks play"""
        #deactivating the play button
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset the game settings
            self.settings.initialize_dynamic_settings()
        #if self.play_button.rect.collidepoint(mouse_pos):
            #reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            #resetting the score
            self.sb.prep_score()
            
            #displaying the level
            self.sb.prep_level()

            #displaying number of ships
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor
            pygame.mouse.set_visible(False)

    #refactoring _check_events()            
    def _check_keydown_events(self, event):
        '''respond to keypresses'''
        if event.key == pygame.K_RIGHT:
            #allow continuous movement 
            self.ship.moving_right = True
            #moving both left and right - more accurate; if both keys are held down, ship stops moving 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #pressing q to quit
        elif event.key == pygame.K_q:
            sys.exit()
        #firing bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    #refactoring _check_events()
    def _check_keyup_events(self, event):
        '''respond to keyreleases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            #moving both left and right - more accurate
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    #firing bullets
    def _fire_bullet(self):
        """create a new bullet and add it to the bullet group"""
        #limit bullets - player presses spacebar -> len of bullets checked; allows bullets to fire in groups of 3
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    #create update bullet method
    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        #update bullet positions
        
        #storing bullets in a group
        self.bullets.update()

        #delete old bullets - get rid of bullets that have diappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets)) - used to verify bullets were deleted

        #refactoring_update_bullets()
        self._check_bullet_alien_collisions()
    
    #refactoring_update_bullets()
    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions"""
        #remove any bullets and alies that have collided

        #detecting bullet collisions - check for any bullets that have hit aliens
        #if so, get rid of the bullet and the aliem
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #updating the score as aliens are shot down
        if collisions:
            #making sure to score all hits
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            #self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            #high scores
            self.sb.check_high_score()


        #repopulating fleet - check whether alien group is empty (has to be completely empty)
        if not self.aliens:
            #destroy exsisting bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()   
            self.settings.increase_speed() 

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """check if the fleet is at an edge, then update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        """update the positions of all aliens in the fleet"""
        self.aliens.update()

        #detecting alien and ship collisions - look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!!")
            self._ship_hit()
        
        #look for aliens hitting the bottom fo the screen
        self._check_aliens_bottom()
        

    #create instance of alien
    def _create_fleet(self):
        """create the fleet of aliens"""
        #create an alien and find the number of aliens ina a row
        #space between each alien is equal to one alien width

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        #formula to determine how many aliens fit in a row
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x// (2 * alien_width)

        #determine the num of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            #create the first row of aliens
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    #refactoring _create_fleet
    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the rown
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    #dropping the fleet and changing direction
    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """responding to the ship being hit by an alien"""
        #game over - ends game when player runs out of ships
        if self.stats.ships_left > 0:
            #decrements ships_left, and update scoreboard
            self.stats.ships_left -= 1

            self.sb.prep_ships()
            
            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    #aliens that reach the bottom of the screen
    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit
                self._ship_hit()
                break

    #create the update screen method (2)
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #Redraw the screen during each pass through the loop

        ##self.screen.fill(self.bg_color) #use before setting class set-up
        self.screen.fill(self.settings.bg_color)

        #draws the ship to the screen (2)
        self.ship.blitme()

        #firing bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #create alien instance
        self.aliens.draw(self.screen)

        self.sb.show_score()

        #draw the play button is the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

         #Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
