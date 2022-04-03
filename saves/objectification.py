import time
import pygame
import random,sys,os,math
from pygame.locals import *

pygame.init()

fps = 60


size = width,height = 960,600
F11size = width,height = 1920,1080
fullscreen = False
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("A Lovely Tool For Writers and Readers")
background = pygame.Surface(screen.get_size()).convert()
clock = pygame.time.Clock()
position = background.get_rect()
font = pygame.font.SysFont("mingliu.ttc", 40)
word = font.render("Click To Start!", True, (0,255,0))


running = True

class Text:
    
    def __init__(self):
        self.line = 0
        self.first = True
        self.in_box = False
        self.text = [""]
        self.x = [0,200]
        self.y = [0,200]
        self.lenx = self.x[1] - self.x[0]
        self.leny = self.y[1] - self.y[0]
        pass
        
#text box
tb = Text()

def start(event):
    global tb
    pos = pygame.mouse.get_pos()
    
    if (tb.x[0] <= pos[0] and pos[0] <= tb.x[1]
    and tb.y[0] <= pos[1] and pos[1] <= tb.y[1]
    and event.type == MOUSEBUTTONDOWN):
        tb.in_box = True
    elif (((tb.x[0] > pos[0] or pos[0] > tb.x[1])
    or (tb.y[0] > pos[1] or pos[1] > tb.y[1]))
    and event.type == MOUSEBUTTONDOWN):
        tb.in_box = False
    if tb.in_box:
        if tb.first:
            clear_board()
            tb.first = False
        inbox(event)
        
def inbox(event):
    pos = pygame.mouse.get_pos()
    text_in(event, pos)
    
def text_in(event, pos):
    global tb
    
    if event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
            if len(tb.text[tb.line]) == 0:
                if tb.line > 0:
                    tb.text.pop()
                    tb.line -= 1
                else:
                    pass
            else:
                tb.text[tb.line] = tb.text[tb.line][:-1]
        elif event.key == K_TAB:
            tb.text[tb.line] += "    "   
        elif event.key == K_RETURN:
            tb.text.append("")
            tb.line += 1
        else:
            tb.text[tb.line] += event.unicode
        clear_board()
        p_text(tb.text, tb.line)

def clear_board():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (90,0,0), [0,0,200,200], 2)
    pygame.display.update()
        
def p_text(text, line):
    k = 0
    for i in text:
        o_text = font.render(i, True, (0,255,0))
        screen.blit(o_text, (0,25*k))
        k += 1
    pygame.display.update()
    
    
#pygame init        
screen.blit(background,(0,0))
screen.fill((255,255,255))
screen.blit(word,position)
pygame.draw.rect(screen, (90,0,0), [0,0,200,200], 2)
pygame.display.update()
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_F11:
                fullscreen = not fullscreen
                continue
                if fullscreen:
                    screen = pygame.display.set_mode(F11size, FULLSCREEN | HWSURFACE, 32)
                    pygame.display.update()
                    continue
                else:
                    screen = pygame.display.set_mode(size)
                    pygame.display.update()
                    continue
            elif event.key == K_ESCAPE:
                fullscreen = False
                screen = pygame.display.set_mode(size)
                pygame.display.update()
                continue
                
        start(event)
        
    clock.tick(fps)