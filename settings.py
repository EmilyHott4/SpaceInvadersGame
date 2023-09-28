class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings. Controls game's appearance and ship's speed"""
        
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #adj. ship speed - ship speed will now move 1.5 pixels rather than 1 pixel on each pass through the loop 
        self.ship_speed = 1.5
        #responding to alien and ship collisions
        self.ship_limit = 3

        #add bullet setting
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3 #limit num bullets - limits plater to 3 bullets


        #moving aliens right - control the speed of ea alien
        #Alien sttings
        #self.alien_speed = 1.0

        #create setting for fleet directions
        self.fleet_drop_speed = 10 #controls how quickly the fleet drops down the screenea time alien reaches either edge
        #fleet_direction of 1 rep. right; -1 rep. left
        #self.fleet_direction = 1

        #how quikcly the game speeds up
        self.speedup_scale = 1.1

        #how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        #updating the score as aliens are shot down
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings"""

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *=self.speedup_scale

        #increasing point value
        self.alien_points = int(self.alien_points * self.score_scale)
        
        #used to check increasing point value
        #print(self.alien_points)
        