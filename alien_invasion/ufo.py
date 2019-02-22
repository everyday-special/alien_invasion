#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 13:06:29 2018

Code related to the UFOs for Alien Invasion

@author: matt
"""

import pygame
from pygame.sprite import Sprite

class Ufo(Sprite):
    """A class to represent a single alien in the fleet"""
    
    def __init__(self, ai_settings, screen):
        """initialize UFO and set its starting position"""
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the UFO image and it its rect attribute
        self.image = pygame.image.load('images/ufo.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Store UFOs exact position
        self.x = float(self.rect.x)
        
    def blitme(self):
        """draw the UFO at its current position"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """updates the UFOs position"""
        self.x += (self.ai_settings.ufo_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
