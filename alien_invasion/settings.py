#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 22:30:21 2018

Settings for Alien Invasion game

@author: matt
"""

class Settings():
    """A Class to store all the settings for Alien Invasion"""
    
    def __init__(self):
        """initialize the games settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (180, 180, 255)
        
        #ship settings
        self.ship_limit = 3
    
        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        # ufo settings
        self.fleet_drop_factor = 20
        
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        
    def initialize_dynamic_settings(self):
        """Initializes settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.ufo_speed_factor = 1
        self.bullet_speed_factor = 1
        self.ufo_points = 50
        
        # Direction of 1 is to the right
        # Direction of -1 is to the left
        self.fleet_direction = 1
    
    def increase_speed(self):
        """increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.ufo_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.ufo_points = int(self.ufo_points * self.speedup_scale)