import pygame
import random,sys,os,math,time
from pygame.locals import *

pygame.init()
initii = True
class Text:
    
    def __init__(self):
        self.line = 0
        self.first = True
        self.in_box = False
        self.f = open("story.txt", "r+")
        self.text = self.f.readlines()
        if(self.text == []):
            self.text.append("")
        self.f.close()
        self.x = [0,200]
        self.y = [0,200]
        self.lenx = self.x[1] - self.x[0]
        self.leny = self.y[1] - self.y[0]
        self.size = (960,600)
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        self.word = pygame.font.SysFont("mingliu.ttc", 40)
        pass
    
    def start(self, event):
        pos = pygame.mouse.get_pos()
        
        global initii
        #print(initii)
        if(initii):
            if (self.x[0] <= pos[0] and pos[0] <= self.x[1]
            and self.y[0] <= pos[1] and pos[1] <= self.y[1]):
                if(event.type == MOUSEBUTTONDOWN):
                    if(self.text != ""):
                        self.clear_board()
                        self.p_text(self.text)    
                        initii = False
                        self.in_box = True
                        return
        
        if (self.x[0] <= pos[0] and pos[0] <= self.x[1]
        and self.y[0] <= pos[1] and pos[1] <= self.y[1]
        and event.type == MOUSEBUTTONDOWN):
            self.in_box = True
            
        elif (((self.x[0] > pos[0] or pos[0] > self.x[1])
        or (self.y[0] > pos[1] or pos[1] > self.y[1]))
        and event.type == MOUSEBUTTONDOWN):
            self.in_box = False
        if self.in_box:
            self.inbox(event)
            
    def inbox(self, event):
        pos = pygame.mouse.get_pos()
        self.text_in(event, pos)

    def text_in(self, event, pos):
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if len(self.text[self.line]) == 0:
                    if self.line > 0:
                        self.text.pop()
                        self.line -= 1
                    else:
                        pass
                else:
                    if(self.text[self.line][-1] == "\n"):
                        if(len(self.text[self.line]) == 1):
                            self.text.pop()
                            self.line -= 1
                        else:
                            self.text[self.line] = self.text[self.line][:-2]
                    else:
                        self.text[self.line] = self.text[self.line][:-1]
            elif event.key == K_TAB:
                self.text[self.line] += "    "   
            elif event.key == K_RETURN:
                self.text[self.line] += "\n"
                self.text.append("")
                self.line += 1
                return
            else:
                self.text[self.line] += event.unicode
            self.clear_board()
            self.p_text(self.text)

    def clear_board(self):
        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen, (90,0,0), [0,0,200,200], 2)
        pygame.display.update()
        
    def p_text(self, text):
        k = 0
        idx = 0
        
        f = open("story.txt","w+")
        
        for i in text:
            tp_text = ""
            for tp in i:
                if(tp != "\n"):
                    tp_text += tp
            o_text = self.word.render(tp_text, True, (0,255,0))
            self.screen.blit(o_text, (0,25*k))
            k += 1
            f.write(text[idx])
            idx += 1
            
        f.close()
        '''
        f = open("story.txt","r+")
        str = f.readlines()
        print(str)
        f.close()
        '''
        pygame.display.update()

#text box
tb = Text()

def main():
    global tb
    
    fps = 60
    running = True
    pygame.display.set_caption("A Lovely Tool For Writers and Readers")
    background = pygame.Surface(tb.screen.get_size()).convert() 
    clock = pygame.time.Clock()
    position = background.get_rect()
    word = tb.word.render("Click To Start!", True, (0,255,0))

    tb.screen.blit(background,(0,0))
    tb.screen.fill((255,255,255))
    tb.screen.blit(word,position)
    pygame.draw.rect(tb.screen, (90,0,0), [0,0,200,200], 2)
    pygame.display.update()
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            tb.start(event)
            
        clock.tick(fps)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()