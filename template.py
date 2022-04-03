import pygame
import sys
import math
import time
import os
from pygame.locals import *

def check(now,l,r):
        return (l <= now and now <= r)    

class story:
    def __init__(self, story_name:str, type = "r+"):
        self.name = story_name
        self.type = type
        try:
            self.f = open("./booksdata/"+self.name+".txt", self.type)
            pass
        except IOError:
            self.f = open("./booksdata/"+self.name+".txt", "w+")
         
class Unlocker:  
    #mode -> informations : in_lobby, page, book_num, name, max_page, cur_type
    def __init__(self, mode):
        a,b,c = mode.split("-")
        self.cur_type = a
        self.page = int(c)
        if b == 'L':
            self.in_lobby = True
            self.name = "list"
            self.book_num = -1
            tps = story(self.name)
            cou = 0
            for line in tps.f:
                cou += 1
            self.max_page = math.ceil(cou/5)
        else:
            self.in_lobby = False
            self.book_num = int(b)
            tps = story("list")
            for line in tps.f:
                if line.split(" ")[0] == b:
                    self.name = line.split(" ")[1][:-1] # have "\n"
                    break
            else:
                print("Unlocking Error(Book not found)")
            tps = story(self.name)
            cou = 0
            for line in tps.f:
                cou += 1
            self.max_page = math.ceil(cou/9)
        
class Text:
    def __init__(self):
        self.size = (960,600)
        self.dist = 90
        self.dist_down = 80
        self.screen = pygame.display.set_mode(self.size, RESIZABLE, 32)
        self.word = pygame.font.SysFont("Consolas", 30)
        self.writer_rect = pygame.Rect(720,520,240,80)
        self.reader_rect = pygame.Rect(0,520,240,80)
        self.menu_rect = pygame.Rect(0,0,90,90)
        self.up_button = pygame.Rect(880,340,70,70)
        self.down_button = pygame.Rect(880,410,70,70)
        self.add_button = pygame.Rect(10,self.size[1]-self.dist_down-70,60,60)
        self.pre_mode = ">-w-<"
        self.pre_cou = -1
        self.pre_name = "UNNAMED"
        
    def clear_board(self):
        max_x = self.size[0]
        max_y = self.size[1]
        d = self.dist
        d2 = self.dist_down
        background = pygame.Surface(self.screen.get_size()).convert()
        select_label = pygame.image.load("./icon/index1.png").convert()
        select_label = pygame.transform.scale(select_label, (d, d))
        color_1 = (139,69,19)
        color_2 = (191,40,40)
        word = self.word.render("Readers", True, color_2)
        word2= self.word.render("Writers", True, color_2)
        self.screen.blit(background,(0,0))
        self.screen.fill((255,248,246))
        self.screen.blit(word,(60,545))
        self.screen.blit(word2,(780,545))
        self.screen.blit(select_label,(0,0))
        pygame.draw.line(self.screen,color_1,(0,d),(d,d),3)
        pygame.draw.line(self.screen,color_1,(0,max_y-d2),(max_x,max_y-d2),5)
        pygame.draw.rect(self.screen, color_1, [d,d,780,430], 3)
        pygame.display.update()
    
    def scene(self,mode:int,name:str,change_p = False,add_book = False):
        max_y = self.size[1]
        d = self.dist
        d2 = self.dist_down
        color_1 = (139,69,19)
        color_2 = (191,40,40)
        word3 = self.word.render(name, True, color_2)
        self.screen.blit(word3,(120,30))
        pygame.draw.line(self.screen,color_1,(d,0),(d,max_y-d2),3)
        if mode == 0:  #read_mode
            pygame.draw.line(self.screen,color_1,(720,max_y-d2),(720,max_y),5)
        else:          #write_mode
            pygame.draw.line(self.screen,color_1,(240,max_y-d2),(240,max_y),5)
        if change_p:
            pygame.draw.rect(self.screen,(0,0,0),self.up_button,3)
            pygame.draw.rect(self.screen,(0,0,0),self.down_button,3)
            pygame.draw.polygon(self.screen,(0,0,0),[(915,355),(895,395),(935,395)],3)
            pygame.draw.polygon(self.screen,(0,0,0),[(915,465),(895,425),(935,425)],3)
        if add_book:
            pygame.draw.rect(self.screen,(0,0,0),self.add_button,3)
            addicon = pygame.image.load("./icon/addicon.png").convert()
            self.screen.blit(addicon,(10,self.size[1]-self.dist_down-70))
        pygame.display.update()

    def change_page(self, mode, flag:int): # +1:up page -1:down page
        now = Unlocker(mode)
        if now.page + flag < 1 or now.page + flag > now.max_page:
            return mode
        else:
            if now.book_num != -1:
                mode = now.cur_type+"-"+str(now.book_num)+"-"+str(now.page+flag)
            else:
                mode = now.cur_type+"-"+"L"+"-"+str(now.page+flag)
            self.clear_board()
            if now.cur_type == "e" or now.cur_type == "w":
                tp = 1 #write mode
            else:
                tp = 0 #read mode
            if now.name == "list":
                self.scene(tp,"Index",change_p=True)
            else:
                self.scene(tp,now.name,change_p=True)
            if now.in_lobby != True:
                self.p_book(tp,now.name,now.page+flag)
            return mode

    def print_list(self, page = 1):
        list = story("list")
        cou = 0
        dist = 80
        block_pos = [self.dist+5,self.dist+30]
        st = 0+(page-1)*5
        ed = 4+(page-1)*5
        now = 0
        for lis in list.f:
            if check(now,st,ed):
                flag = True
                tp = ""
                cou += 1
                for k in lis:
                    if k == '\n':
                        word = self.word.render(tp, True, (0,0,0))
                        self.screen.blit(word,block_pos)
                        pygame.draw.line(self.screen,(0,0,0),(block_pos[0]-5,block_pos[1]+50),(870,block_pos[1]+50),3) 
                        block_pos[1] += dist
                    elif k == ' ' and flag == True:
                        tp += "    "
                        flag = False
                    else:
                        tp += k
            if now > ed:
                break
            now += 1
        pygame.display.update()
        self.pre_cou = cou
        return cou
    
    def trans_book(self, name):
        book = story(name)
        tp = []
        for lines in book.f:
            while len(lines) > 46:
                tps = lines[:45]
                if tps[-1] != '\n':
                    tps = tps + '\n'
                tp.append(tps)
                lines = lines[45:]
            else:
                tp.append(lines)
        book.f.close()
        book = story(name,"w+")
        for i in tp:
            book.f.write(i)
        book.f.close()
        return
    
    def p_book(self,mode,name,page = 1):
        self.clear_board()
        self.scene(mode,name,change_p=True)
        self.trans_book(name)
        book = story(name)
        st = 0+(page-1)*9
        ed = 8+(page-1)*9
        now = 0
        cou = 0
        for lines in book.f:
            if check(now,st,ed):
                tp = ""
                for ch in lines:
                    if ch == '\n':
                        word = self.word.render(tp, True, (0,0,0))
                        self.screen.blit(word,(self.dist+5,self.dist+cou*(self.dist/2)+15))
                        cou += 1
                    else: 
                        tp += ch
            if now > ed:
                break
            now += 1
        pygame.display.update()

    def edit_book(self,event,mode):
        if event.type != MOUSEBUTTONDOWN and event.type != KEYDOWN:
            return mode
        now = Unlocker(mode)
        name = now.name
        text = story(name)
        self.pre_mode = mode
        pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "w-L-1"
        if self.reader_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "r-L-1"
        if self.writer_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "w-L-1"
        if self.up_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            page = now.max_page
            mode = self.change_page(mode,-1)
            return mode
        if self.down_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            page = now.max_page
            mode = self.change_page(mode,1)
            return mode

        lines = text.f.readlines()
        line = len(lines)-1
        text.f.close()
        if(lines == []):
            lines.append("\n")
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if len(lines[line]) == 0:
                    if line > 0:
                        text.pop()
                        line -= 1
                    else:
                        pass
                else:
                    if(len(lines[line]) == 1):
                        lines.pop()
                        line -= 1
                    else:
                        lines[line] = lines[line][:-2]
                        lines[line] += '\n'
            elif event.key == K_RETURN:
                if len(lines[line]) < 46:
                    lines.append("\n")
                line += 1
            elif event.key == K_TAB:
                lines[line] = lines[line][:-1]
                lines[line] += "    "
                if len(lines[line]) >= 45:
                    left = len(lines[line]-45)
                    lines[line] = lines[line][:-left]
                lines[line] += "\n"
            else:
                lines[line] = lines[line][:-1]
                lines[line] += event.unicode
                i=0
                while len(lines[line+i]) >= 45:
                    tp = lines[line+i][45:]
                    lines.append("\n")
                    lines[line+i+1] = tp + lines[line+i+1]
                    lines[line+i] = lines[line+i][:45]
                    lines[line+i] += '\n'
                    lines[line+i+1] = lines[line+i+1][:-1]
                    i+=1
                if i != 0:
                    lines[line+i] += '\n'
                else:
                    lines[line] += "\n"
                line += i  
            
            text = story(name,"w+")
            for i in lines:
                text.f.write(i)
            text.f.close()
            self.clear_board()
            self.scene(1,name,change_p=True)
            self.p_book(1,name,now.page)
        return mode

    def to_write(self,event,mode):
        now = Unlocker(mode)
        if mode == self.pre_mode:
            cou = self.pre_cou
        else:
            if now.in_lobby == True:
                self.clear_board()
                self.scene(1,"Index",change_p=True,add_book=True)
                cou = self.print_list(page = now.page)
            else:
                print("to_write mode error")
                return "-1-1-1-1-1-"
        self.pre_mode = mode
        
        pos = pygame.mouse.get_pos()
        if now.in_lobby == True and event.type == MOUSEBUTTONDOWN:
            all_list = story("list")
            d = self.dist
            for i in range(cou):
                if check(pos[0],d,870) and check(pos[1],d+i*80,d+(i+1)*80):
                    cou2 = -(now.page-1)*5
                    for line in all_list.f:
                        if(i != cou2):
                            cou2 += 1
                            continue
                        else:
                            tp = ""
                            cou = 0
                            for ch in line:
                                if ch == ' ':
                                    cou += 1
                                elif ch == '\n':
                                    self.clear_board()
                                    self.scene(1,tp,change_p=True)
                                    self.p_book(1,tp)
                                    return "e-"+str(i+1+(now.page-1)*5)+"-1"
                                elif cou > 0:
                                    tp += ch
        
        if self.reader_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "r-L-1"
        if self.menu_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "w-L-1"
        if self.up_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            mode = self.change_page(mode,-1)
            return mode
        if self.down_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            mode = self.change_page(mode,1)
            return mode
        if self.add_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            mode = self.add_new_book()
            return mode
        return mode
    
    def to_read(self,event,mode):
        now = Unlocker(mode)
        if mode == self.pre_mode:
            cou = self.pre_cou
            name = self.pre_name
        else:
            if now.in_lobby == True:
                self.clear_board()
                self.scene(0,"Index",change_p=True)
                cou = self.print_list(now.page)
                name = "list"
            else:
                name = now.name
                self.p_book(0,name,page = now.page)
        self.pre_mode = mode
        self.pre_name = name
        pos = pygame.mouse.get_pos()
        if now.in_lobby == True:
            if event.type == MOUSEBUTTONDOWN:
                for i in range(0,cou):
                    if (check(pos[0],self.dist,870) and 
                        check(pos[1],self.dist+i*80,self.dist+(i+1)*80)):
                        all_list = story("list")
                        cou2 = -(now.page-1)*5
                        for line in all_list.f:
                            if(i != cou2):
                                cou2 += 1
                                continue
                            else:
                                tp = ""
                                cou = 0
                                for ch in line:
                                    if ch == ' ':
                                        cou += 1
                                    elif ch == '\n':
                                        self.p_book(0,tp)
                                        return "r-"+str(i+(now.page-1)*5+1)+"-1" # to read
                                    elif cou > 0:
                                        tp += ch
        
        if self.menu_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "r-L-1"
        if self.writer_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            return "w-L-1"
        if self.up_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            mode = self.change_page(mode,-1)
            return mode
        if self.down_button.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
            mode = self.change_page(mode,1)
            return mode
        return mode
        
    def add_new_book(self):
        self.clear_board()
        self.scene(1,"Add New Book",change_p=False)
        book_name = ""

        while True:
            self.pre_mode = "adding"
            event = pygame.event.poll()
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                return "1-1-1-1-1"
            elif((self.menu_rect.collidepoint(pos) or self.writer_rect.collidepoint(pos))
                and event.type == MOUSEBUTTONDOWN):
                return "w-L-1"
            elif(self.reader_rect.collidepoint(pos) and event.type == MOUSEBUTTONDOWN):
                return "r-L-1"
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(book_name) == 0:
                        continue
                    else:
                        book_name = book_name[:-1]
                        self.clear_board()
                        self.scene(1,"Add New Book")
                elif(event.key == K_TAB or event.unicode == '\\' or event.unicode == '/'
                    or event.unicode == '?' or event.unicode == '\"' or event.unicode == '*'
                    or event.unicode == '|' or event.unicode == '<' or event.unicode == '>'
                    or event.unicode == ':'):
                    continue
                elif event.key == K_SPACE:
                    book_name += "_"
                elif event.key == K_RETURN:
                    list = story("list")
                    cou = 0
                    for line in list.f:
                        cou += 1
                        if line.split(" ")[1][:-1] == book_name:
                            return "w-L-1"
                    list.f.write(str(cou+1)+" "+book_name+"\n")
                    list.f.close()
                    tp = story(book_name)
                    tp.f.close()
                    return "w-L-1"
                else:
                    book_name += event.unicode
                    self.clear_board()
                    self.scene(1,"Add New Book")
                while len(book_name) >= 40:
                    book_name = book_name[:-1]
                o_text = self.word.render(book_name, True, (0,0,0))
                self.screen.blit(o_text, (self.dist+5,self.dist+15))
                pygame.display.update()
