#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 20:13:17 2018

Code for the scoreboard in the Alien Invasion game

@author: matt
"""

import pygame.font

class Scoreboard():
    """A class to report scoring information"""
    
    def __init__(self, ai_settings, stats, screen):
        """initialize scoreboard attributes"""
        self.stats = stats
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Font settings and information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        # Prepare the initial score image
        self.prep_score()
        
    def prep_score(self):
        """Turn the score into a rendered image"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # Display the score in the upper right corner of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def show_score(self):
        """Draw the score onto the screen"""
        self.screen.blit(self.score_image, self.score_rect)