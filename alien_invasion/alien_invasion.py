# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the first file in making the Alien Invasion game from Python
Crash Course, chapter 12

on 10/17/18 was about to add high scores
"""

import pygame
from pygame.sprite import Group

from settings import Settings
import ship as space_ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    #creates a display window 1200 x 800 pixels called screen
    pygame.display.set_caption('Alien Invasion')
    
    # Make the play button
    play_button = Button(ai_settings, screen, "PLAY")
    
    #Make a ship
    ship = space_ship.Ship(ai_settings, screen)
    #Make a group to store active bullets in
    bullets = Group()
    # Make a fleet of Ufos
    ufos = Group()
    gf.create_fleet(ai_settings, screen, ship, ufos)
    
    # Create an instance to store game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, stats, screen)
    
    #start main loop for the game
    while True:
        #checks for game events
        gf.check_events(ai_settings, stats, screen, ship, bullets, ufos, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, sb, screen, ship, bullets, ufos)
            gf.update_ufos(ai_settings, stats, screen, ship, bullets, ufos)
        gf.update_screen(ai_settings, stats, sb, screen, ship, bullets, ufos, play_button)

run_game()