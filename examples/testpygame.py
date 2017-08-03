import pygame, sys, os
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((100, 100))

player = pygame.image.load(os.path.join(os.path.dirname( __file__ ),"textures/crate.gif"))
player.convert()

while True:
    screen.blit(player, (10, 10))
    pygame.display.flip()

pygame.quit()