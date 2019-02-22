#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 20:07:16 2018

Module containing the game functions for Alien Invasion

@author: matt
"""

import sys
from time import sleep

import pygame

from bullet import Bullet
from ufo import Ufo

def check_keydown_events(event, ai_settings, stats, screen, ship, bullets, ufos):
    """Responds to keypresses"""
    if event.key == pygame.K_RIGHT:
        #Right move flag on
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #Left move flag on
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Press space to fire bullets
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        # Press q to quit
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_p:
        # Press p to play
        pygame.mouse.set_visible(False)
        game_reset(ai_settings, screen, stats, ship, bullets, ufos)
        stats.game_active = True

def check_keyup_events(event, ship):
    """responds to key releases"""
    if event.key == pygame.K_RIGHT:
        #Right move flag off
        ship.moving_right = False            
    elif event.key == pygame.K_LEFT:
        #Left move flag off
        ship.moving_left = False
        
def check_play_button(ai_settings, stats, screen, ship, bullets, ufos, play_button, mouse_x, mouse_y):
    """Starts a new game when play button is pressed."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset dynamic game settings
        ai_settings.initialize_dynamic_settings()
        #Hide the mouse cursor and reset the game
        pygame.mouse.set_visible(False)
        game_reset(ai_settings, screen, stats, ship, bullets, ufos)
        stats.game_active = True

def check_events(ai_settings, stats, screen, ship, bullets, ufos, play_button):
    """responds to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, ship, bullets, ufos)             
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse clicked')
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, screen, ship, bullets, ufos, play_button, mouse_x, mouse_y)
            
def update_screen(ai_settings, stats, sb, screen, ship, bullets, ufos, play_button):
    """updates images on screen and flip to new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    ship.update()
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    ufos.draw(screen)
    sb.prep_score()
    sb.show_score()
    
    if stats.game_active == False:
        play_button.draw_button()
        pygame.mouse.set_visible(True)
    
    # Make the most recently drawn screen visible
    pygame.display.flip()
    
def update_bullets(ai_settings, stats, sb, screen, ship, bullets, ufos):
    """updates position of bullets and gets ride of old bullets"""
    #update bullet positions
    bullets.update()
    # Removes old bullets from bullets group
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collisions(ai_settings, stats, sb, screen, ship, bullets, ufos)
            
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not yet reached"""
    #Create a new bullet and add it to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def check_bullet_collisions(ai_settings, stats, sb, screen, ship, bullets, ufos):
    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    if collisions:
        for ufo in collisions.values():
            stats.score += ai_settings.ufo_points * len(ufo)
            sb.prep_score()
            
    # Restores fleet and speeds up the game upon destruction of entire fleet
    if len(ufos) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, ufos)
        
def check_ship_collisions(ai_settings, stats, screen, ship, bullets, ufos):
    if pygame.sprite.spritecollideany(ship, ufos):
        ship_hit(ai_settings, stats, screen, ship, bullets, ufos)

def create_fleet(ai_settings, screen, ship, ufos):
    """Creates a fleet of UFOs based on available screen size"""
    # Create a UFO and find number of ufos in a row
    # Space beteween each ufo is equal to one ufo length/width
    ufo = Ufo(ai_settings, screen)
    ufo_width = ufo.rect.width
    number_of_ufos_x = get_number_of_ufos_x(ai_settings, ufo_width)
    number_of_rows = get_number_of_rows(ai_settings, ship.rect.height, ufo.rect.height)
    
    #Creates the rows of UFOs
    for row_number in range(number_of_rows):
        for ufo_number in range(number_of_ufos_x):
            create_ufo(ai_settings, screen, ufos, ufo_number, row_number)
        
def get_number_of_ufos_x(ai_settings, ufo_width):
    """determine number of aliens that fit into a row"""
    available_x_space = ai_settings.screen_width - (2 * ufo_width)
    number_of_ufos_x = int(available_x_space / (2 * ufo_width))
    return number_of_ufos_x    

def create_ufo(ai_settings, screen, ufos, ufo_number, row_number):
    """creates a ufo and place it in each row"""
    ufo = Ufo(ai_settings, screen)
    ufo_width = ufo.rect.width
    ufo.x = ufo_width + (2 * ufo_width * ufo_number)
    ufo.rect.x = ufo.x
    ufo.rect.y = ufo.rect.height + 2 * ufo.rect.height * row_number
    ufos.add(ufo)
    
def get_number_of_rows(ai_settings, ship_height, ufo_height):
    """Determine the number of rows to be in the alien fleet"""
    available_space_y = ai_settings.screen_height - (3 * ufo_height) - ship_height
    number_of_rows = int(available_space_y / (2 * ufo_height))
    return number_of_rows

def update_ufos(ai_settings, stats, screen, ship, bullets, ufos):
    """
    First checks to see if fleet has reached an edge,
    then checks for collisions with the ship or the bottom of the screen
    then updates the position of all the ufos"""
    check_fleet_edges(ai_settings, ufos)
    check_ship_collisions(ai_settings, stats, screen, ship, bullets, ufos)
    check_ufos_bottom(ai_settings, stats, screen, ship, bullets, ufos)
    ufos.update()
    
def check_fleet_edges(ai_settings, ufos):
    """checks to see if any ufos in the fleet are touching the edge"""
    for ufo in ufos.sprites():
        if ufo.check_edges():
            change_fleet_direction(ai_settings, ufos)
            break

def change_fleet_direction(ai_settings, ufos):
    """Drops the fleet closer to ship, changes the fleet direction"""
    for ufo in ufos.sprites():
        ufo.rect.y += ai_settings.fleet_drop_factor
    ai_settings.fleet_direction *= -1
        
def ship_hit(ai_settings, stats, screen, ship, bullets, ufos):
    """Responds to ship being hit by ufos"""
    # Checks to see how many ships are left
    print(stats.ships_left)
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1
        #Empty list of ufos and bullets
        ufos.empty()
        bullets.empty()
        #Create new fleet and recenter the ship
        create_fleet(ai_settings, screen, ship, ufos)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        print('You destroyed', stats.score, 'fleets of UFOs!')
    
def check_ufos_bottom(ai_settings, stats, screen, ship, bullets, ufos):
    """checks to see if ufos have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for ufo in ufos.sprites():
        if ufo.rect.bottom >= screen_rect.bottom:
            #Treat this as the same as if a ship was hit (lose condition)
            ship_hit(ai_settings, stats, screen, ship, bullets, ufos)
            break
        
def game_reset(ai_settings, screen, stats, ship, bullets, ufos):
    """resets the game after all ships are destroyed"""
    #Reset game stats
    stats.reset_stats()
    # Empty ufos and bullets
    ufos.empty()
    bullets.empty()
    # Create new fleet and recenter the ship
    create_fleet(ai_settings, screen, ship, ufos)
    ship.center_ship()
