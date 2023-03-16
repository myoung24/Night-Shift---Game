# First attempt at a game using pygame
# Author: Matt Young
# Date created: March 16, 2023

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 540))
pygame.display.set_caption('Night Shift')  # Title of the window
clock = pygame.time.Clock()

test_surface = pygame.image.load('clouds.webp')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface, (0, 0))


    pygame.display.update()
    clock.tick(60)
