import pygame
import random
import sys
import os
from pygame.locals import *

pygame.init()
size = width,height = 960,600
F11size = width,height = 1920,1080
fullscreen=False
screen = pygame.display.set_mode(size, 0, 32)
background = pygame.Surface(screen.get_size()).convert() 
pygame.display.set_caption("A Lovely Tool For Writers and Readers")
font = pygame.font.SysFont("Consolas", 48)
word = font.render("Hello world!", True, (0,255,0))
position = background.get_rect()
pos = (300,240,500,300)
running=True
while running:
    screen.blit(background,(0,0))
    screen.fill((255,255,255))
    screen.blit(word,pos)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(F11size, FULLSCREEN | HWSURFACE, 32)
                else:
                    screen = pygame.display.set_mode(size)
            elif event.key == K_ESCAPE:
                         fullscreen = False
                         screen = pygame.display.set_mode(size)
        else:
            pass
pygame.quit()
