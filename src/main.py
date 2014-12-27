# import the pygame module, so you can use it
import pygame
import block
import random
from pygame.constants import FULLSCREEN
from block import block_square, block_line, block_lzag, block_rzag, block_rhook,\
    block_lhook
screen_width = 200
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height))
# define a main function
def main():
    cells = [[0 for x in range(25)] for x in range(11)] 
    def place(b):
        for x in range(0,7):
            if(x%2==0):
                cells[(int)(b.xpos/20+b.squares[x])][(int)(b.ypos/20+b.squares[x+1])]=True
                
            
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("minimal program")
    keys = [False, False, False, False,False]
    # create a surface on screen that has the size of 240 x 180
    image = pygame.image.load("block.png")
    screen.blit(image, (20,20))
    pygame.display.flip()
    # define the position of the block
    # how many pixels we move our block each frame
    step_x = 20
    step_y = 20
    running = True
    # main loop
    def random_block():
        x = random.randint(0,5)
        if(x == 0):
            return block_square
        elif(x == 1):
            return block_line
        elif(x == 2):
            return block_lzag
        elif(x == 3):
            return block_rzag
        elif(x == 4):
            return block_lhook
        else:
            return block_rhook
    def drawblock(blk):
        for x in range(0,7):
            if(x%2==0):
                screen.blit(image,(blk.xpos+blk.squares[x]*20,blk.ypos+blk.squares[x+1]*20))
    current = random_block()
    while running:
        # event handling, gets all event from the eventqueue
        screen.fill((0,0,0))
        drawblock(current);
        # and update the screen (dont forget that!)
       
        for x in range(0,10):
            for y in range(0,24):
                if cells[x][y]==1:
                    screen.blit(image,(20*x,20*y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    keys[0]=True
                elif event.key==pygame.K_s:
                    keys[1]=True
                elif event.key==pygame.K_a:
                    keys[2]=True
                elif event.key==pygame.K_d:
                    keys[3]=True
                elif event.key==pygame.K_r:
                    keys[4]=True
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    
        if keys[0]:
            current.ypos-=step_y
            keys[0]=False
        elif keys[1]:
            current.ypos+=step_y
            keys[1]=False
        elif keys[2]:
            current.xpos-=step_x
            keys[2]=False
        elif keys[3]:
            current.xpos+=step_x
            keys[3]=False
        elif keys[4]:
            place(current)
            current = random_block()
            keys[4]=False
        if current.xpos>screen_width-current.width:
            current.xpos=screen_width-current.width
        if current.xpos<0:
            current.xpos=0
        if current.ypos>screen_height-current.height:
            current.ypos=screen_height-current.height
        if current.ypos<0:
            current.ypos=0
                
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

        