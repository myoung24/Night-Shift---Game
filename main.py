# First attempt at a game using pygame
# Author: Matt Young
# Date created: March 16, 2023

import pygame

pygame.init()

w, h = 950, 650
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Night Shift')  # Title of the window
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 140)

bg_black = pygame.Surface((w, h))
bg_black.fill('black')

bg_clouds = pygame.image.load('clouds.webp')
bg_clouds.set_alpha(150)

fg_test = pygame.image.load('template.jpeg')

text_surface = test_font.render("NIGHT SHIFT", True, "white")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg_black, (0, 0))
    screen.blit(bg_clouds, (0, 0))
    screen.blit(fg_test, (100, 300))
    screen.blit(text_surface, (180, 110))




    pygame.display.update()
    clock.tick(60)
