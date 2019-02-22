#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:43:27 2018

Code for tracking the game statistics for alien invasion

@author: matt
"""

class GameStats():
    """Tracks game statistics for Alien Invasion"""
    
    def __init__(self, ai_settings):
        """Initializes statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #Start game in inactive state
        self.game_active = False
        self.score = 0
        
    def reset_stats(self):
        """Initializes statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0