from template import *

pygame.init()

#text box
tb = Text()

#main loop
def main():
    if not os.path.isdir("./booksdata"):
        os.makedirs("./booksdata")
    fps = 60
    running = True
    clicked = False
    pygame.display.set_caption("A Lovely Tool For Writers and Readers")
    clock = pygame.time.Clock()
    pygame.display.update()
    tb.scene(0,"Index")
    MOD = 1 
    ''' 
    mode = 1 -> reading mode 
        >w< r-L-3 (reader,lobby,page) or r-3-3 (reader,book num,page)
    mode = 2 -> writing mode 
        >w< w-L-3 (writer,lobby,page) or w-3-3 (writer,book num,page) or w-a (writer,add book)
    mode = 3 -> edit book mode 
        >w< e-3-3 (edit,book num,page)
    '''
    mode = "r-L-1"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if mode[0] == 'r':
                mode = tb.to_read(event,mode)
            elif mode[0] == 'w':
                mode = tb.to_write(event,mode)
            elif mode[0] == 'e':
                mode = tb.edit_book(event,mode)
            else:
                print("MOD Error!", mode)
                running = False
                pygame.quit()
                sys.exit()
        clock.tick(fps)

if __name__ == '__main__':
    main()
