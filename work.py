import pygame
import sys,math,time
from pygame.locals import *

pygame.init()

class story:
    global tb
    def __init__(self, story_name):
        self.name = story_name
        try:
            self.f = open(self.name+".txt", "r+")
            pass    
        except IOError:
            error_word = tb.word.render("Can not open the file", True, (250,0,0))
            tb.screen.blit(error_word, (100,100))
            pygame.display.update()
            
class Text:
    
    def __init__(self):
        self.size = (960,600)
        self.dist = 90
        self.dist_down = 80
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        self.word = pygame.font.SysFont("Arial", 55)
        
    def clear_board(self):
        self.screen.fill((255,255,255))
        pygame.display.update()
        
    def scene(self,mode,name):
        global tb
        max_x = self.size[0]
        max_y = self.size[1]
        d = self.dist
        d2 = self.dist_down
        background = pygame.Surface(tb.screen.get_size()).convert() 
        select_label = pygame.image.load("index1.png").convert()
        select_label = pygame.transform.scale(select_label, (d, d))
        color_1 = (139,69,19)
        color_2 = (191,40,40)
        word = tb.word.render("Readers", True, color_2)
        word2= tb.word.render("Writers", True, color_2)
        word3= tb.word.render(name, True, color_2)
        tb.screen.blit(background,(0,0))
        tb.screen.fill((255,248,246))
        tb.screen.blit(word,(40,545))
        tb.screen.blit(word2,(780,545))
        tb.screen.blit(word3,(120,30))
        tb.screen.blit(select_label,(0,0))
        
        #draw.line (surface,color,start_pos,end_pos,width)
        pygame.draw.line(tb.screen,color_1,(d,0),(d,max_y-d2),3) 
        if mode == 0:
            pygame.draw.line(tb.screen,color_1,(720,max_y-d2),(720,max_y),5) 
        else:
            pygame.draw.line(tb.screen,color_1,(240,max_y-d2),(240,max_y),5)
            
        pygame.draw.line(tb.screen,color_1,(0,d),(d,d),3) 
        pygame.draw.line(tb.screen,color_1,(0,max_y-d2),(max_x,max_y-d2),5)
        
        #draw.rect (surface,color,[start_x,start_y,length,width], string_width)
        pygame.draw.rect(tb.screen, color_1, [d,d,780,430], 3)
        pygame.display.update()
        
    
    def print_list(self):
        global tb
        
        list = story("list")
        cou = 0
        block_pos = [self.dist+5,self.dist+30]
        
        # print all the list
        for i in list.f:
            tp = ""
            cou += 1
            for k in i:
                if k == '\n':
                    word = tb.word.render(tp, True, (0,0,0))
                    tb.screen.blit(word,block_pos)
                    pygame.draw.line(tb.screen,(0,0,0),(block_pos[0]-5,block_pos[1]+60),(870,block_pos[1]+60),3) 
                    block_pos[1] += self.dist
                    
                elif k == ' ':
                    tp += "   "
                else:
                    tp += k
        pygame.display.update()
        
        return cou
     
    def p_book(self,name):
        global QwQ
        
        self.clear_board()
        self.scene(0,name)
        list = story(name)
        
        cou = 0
        for i in list.f:
            tp = ""
            for k in i:
                if k == '\n':
                    word = tb.word.render(tp, True, (0,0,0))
                    tb.screen.blit(word,(self.dist+5,self.dist+cou*(self.dist/2)+15))
                    cou += 1
                else: 
                    tp += k
        pygame.display.update()
        QwQ = True
        #print("!")
        
        while(1):
            event = pygame.event.poll()
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if (720 <= pos[0] and pos[0] <= self.size[0] 
                and self.size[1]-self.dist_down <= pos[1] and pos[1] <= self.size[1]):
                    self.to_write()
                    break
                    
                elif (0 <= pos[0] and pos[0] <= 90 and 0 <= pos[1] and pos[1] <= 90):
                    self.clear_board()
                    self.scene(0,"Index")
                    QwQ = False
                    break
                    
    def edit_book(self,name):
        global tb
        
        self.clear_board()
        self.scene(1,name)
        list = story(name)
        line = 0
        tp = ""
        
        cou = 0
        for i in list.f:
            tp = ""
            for k in i:
                if k == K_TAB:
                    tp += "    "
                    
                elif k == '\n':
                    word = tb.word.render(tp, True, (0,0,0))
                    tb.screen.blit(word,(self.dist+5,self.dist+cou*(self.dist/2)+15))
                    cou += 1
                    
                else: 
                    tp += k
                    
        pygame.display.update()
        
        while(1):
            event = pygame.event.poll()
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif (0 <= pos[0] and pos[0] <= 90 and 0 <= pos[1] and pos[1] <= 90):
                    if event.type == MOUSEBUTTONDOWN:
                        self.to_write()
                        return
                        
            elif (0 <= pos[0] and pos[0] <= 240
            and self.size[1]-self.dist_down <= pos[1] and pos[1] <= self.size[1]):
                if event.type == MOUSEBUTTONDOWN:
                # if clicked reader --> read
                        self.to_read()
                        return
                        
            list = story(name)
            text = list.f.readlines()
            #print(text)
            
            if(text == []):
                text.append("\n")
                
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(text[line]) == 0:
                        if line > 0:
                            text.pop()
                            line -= 1
                        else:
                            pass
                            
                    else:
                        if(len(text[line]) == 1):
                            text.pop()
                            line -= 1
                        else:
                            text[line] = text[line][:-2]
                            text[line] += '\n'
                            
                elif event.key == K_TAB:
                    text[line] = text[line][:-1]
                    text[line] += "    "   
                    text[line] += "\n"
                    
                elif event.key == K_RETURN:
                    text.append("\n")
                    line += 1
                    
                else:
                    text[line] = text[line][:-1]
                    text[line] += event.unicode
                    text[line] += '\n'
                    
                self.clear_board()
                self.scene(1,name)
                
                #print all text and put text into file
                idx = 0
                f = open(name+".txt","w+")
                for i in text:
                    tp_text = ""
                    for tp in i:
                        if(tp != '\n'):
                            tp_text += tp
                            
                    o_text = tb.word.render(tp_text, True, (0,0,0))
                    tb.screen.blit(o_text, (self.dist+5,self.dist+idx*(self.dist/2)+15))
                    f.write(text[idx])
                    idx += 1
                    
                f.close()
                pygame.display.update()  
                
        
    def to_write(self):
        self.clear_board()
        self.scene(1,"Index")
        cou = self.print_list()
        list2 = story("list")
        d = self.dist
        block_pos = [self.dist,self.dist]
        
        tppp = 1
        while(1):
            event = pygame.event.poll()
            pos = pygame.mouse.get_pos()
           
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif (0 <= pos[0] and pos[0] <= 240 
            and self.size[1]-self.dist_down <= pos[1] and pos[1] <= self.size[1]):
                if event.type == MOUSEBUTTONDOWN:  
                    self.to_read()
                    return
            
            for i in range(0,cou):
                if (block_pos[0] <= pos[0] and pos[0] <= 870
                and block_pos[1]+i*d <= pos[1] and pos[1] <= block_pos[1]+(i+1)*d):
                    
                    if event.type == MOUSEBUTTONDOWN:
                        cou2 = 0
                        for t in list2.f:
                            if(i != cou2): 
                                cou2 += 1
                                continue
                            else:
                                tp = ""
                                cou = 0
                                for tt in t:
                                    if tt == ' ':
                                        cou += 1
                                    elif tt == '\n':
                                        #print(tp)
                                        self.edit_book(tp)
                                        return
                                    elif cou > 0:
                                        tp += tt 
                                        
    def to_read(self):
        self.clear_board()
        self.scene(0,"Index")
        cou = self.print_list()
        d = self.dist
        block_pos = [self.dist,self.dist]
        
        while(1):
            event = pygame.event.poll()
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif (720 <= pos[0] and pos[0] <= self.size[0] 
            and self.size[1]-self.dist_down <= pos[1] and pos[1] <= self.size[1]):
                if event.type == MOUSEBUTTONDOWN:
                    self.to_write()
                    return
                    
            for i in range(0,cou):
                if (block_pos[0] <= pos[0] and pos[0] <= 870
                and block_pos[1]+i*d <= pos[1] and pos[1] <= block_pos[1]+(i+1)*d):
                    if event.type == MOUSEBUTTONDOWN:
                        list2 = story("list")
                        cou2 = 0
                        for t in list2.f:
                            if(i != cou2): 
                                cou2 += 1
                                continue
                            else:
                                tp = ""
                                cou = 0
                                for tt in t:
                                    if tt == ' ':
                                        cou += 1
                                    elif tt == '\n':
                                        #print(tp)
                                        self.p_book(tp)
                                        return
                                    elif cou > 0:
                                        tp += tt 
                                        
#text box
tb = Text()
QwQ = False

def main():
    global tb,QwQ
    
    fps = 60
    running = True
    clicked = False
    pygame.display.set_caption("A Lovely Tool For Writers and Readers")
    background = pygame.Surface(tb.screen.get_size()).convert() 
    clock = pygame.time.Clock()
    word = tb.word.render("Click To Start!", True, (0,255,0))
    position = background.get_rect()
    tb.screen.blit(background,(0,0))
    tb.screen.fill((255,255,255))
    tb.screen.blit(word,position)
    pygame.display.update()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif QwQ == True:
                continue
            elif clicked == True:
                tb.to_read()
            elif event.type == MOUSEBUTTONDOWN:
                tb.clear_board()
                tb.scene(0,"Index")
                clicked = True
            #if clicked == True:
                #tb.start(event)  
        clock.tick(fps)

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
