#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 22:43:09 2018

Module containing the player's ship and the enemy UFO

@author: matt
"""

import pygame

class Ship():
    
    def __init__(self, ai_settings, screen):
        """initializes the ship and its starting position"""
        self.screen = screen
        self.ai_settings = ai_settings
        
        #load the ship image and get its rect.
        self.image = pygame.image.load('images/spaceship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #Ship movement flags
        self.moving_right = False
        self.moving_left = False
        
        # Start each new ship at the bottom of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
    
        #Store Decimal value for the ships center
        self.center = float(self.rect.centerx)
    
    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """Update ships movement based on movement flags"""
        #update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Update rect object from self.center
        self.rect.centerx = self.center
                         
    def center_ship(self):
        """centers the ship on the screen"""
        self.center = self.screen_rect.centerx