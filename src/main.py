# import the pygame module, so you can use it
import pygame
import random
from pygame.constants import FULLSCREEN
from block import block_square, block_line, block_lzag, block_rzag, block_rhook,\
    block_lhook, block_t
from gravity import gravity
screen_width = 320
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
# define a main function
def main():
    cells = [[0 for x in range(25)] for x in range(11)] 
    #2d array of booleans whole grid if it's filled in or not
    def place(b):#function places a block onto the grid
        for x in range(0,7):
            if(x%2==0):
                cells[int((b.xpos/32)+b.squares[x])][int((b.ypos/32)+b.squares[x+1])]=True
    def checkCollision(block):
        for s in range(0,7):
            if s%2 == 0:
                #print(int(block.xpos/32 + block.squares[s]), int(block.ypos/32 + block.squares[s+1] + 1))
                if (cells[int((block.xpos/32) + block.squares[s])][int((block.ypos/32)+block.squares[s+1]+1)] != 0
                    or block.ypos + block.height >= screen_height):
                        return True
    def random_block():#makes a new random block at the starting spot
        x = random.randint(0,6)
        if(x == 0):
            return block_square()
        elif(x == 1):
            return block_line()
        elif(x == 2):
            return block_lzag()
        elif(x == 3):
            return block_rzag()
        elif(x == 4):
            return block_lhook()
        elif(x == 5):
            return block_rhook()
        else:
            return block_t()
    def drawblock(blk): #draws a block taken as a parameter
        for x in range(0,7):
            if(x%2==0):
                screen.blit(image,(blk.xpos+blk.squares[x]*32,blk.ypos+blk.squares[x+1]*32))
    def fastDrop(block):
        x = 0
        for y in range(0,24):
            for s in range(0,7):
                if s%2 == 0:
                    x = int((block.xpos/32) + block.squares[s])
                    if cells[x][y]:
                        block.ypos = y*32-block.height
                        place(block)
                        block = random_block()
                        return
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("TetrisBuddies")
    keys = [False, False, False, False,False, False,False]
    # create a surface on screen that has the size of 240 x 180
    image = pygame.image.load("block.png")
    # define the position of the block
    # how many pixels we move our block each frame
    step_x = 32
    step_y = 32
    running = True

    current = random_block() #creates first controlable block
    g = gravity(0.1)#initializes gravity class
    # main loop
    while running:
        screen.fill((0,0,0)) #clear screen
        drawblock(current); #draws current block
        #draws all placed squares on the grid
        for x in range(0,10):
            for y in range(0,24):
                if cells[x][y]==1:
                    screen.blit(image,(32*x,32*y))
        pygame.display.flip() #updates screen
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
                elif event.key==pygame.K_t:
                    keys[5]=True
                elif event.key==pygame.K_SPACE:
                    keys[6]=True
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
            current.rotateL()
            keys[4]=False
        elif keys[5]:
            current.rotateR()
            keys[5]=False
        elif keys[6]:
            fastDrop(current)
            keys[6]=False
            

        if current.xpos>screen_width-current.width:
            current.xpos=screen_width-current.width
        for x in range (0,7):
            if x%2 == 0:
                if(current.squares[x])==0:
                    if current.xpos<0:
                        current.xpos=0
        if current.xpos<-32:
            current.xpos=-32   
        if current.ypos>screen_height-current.height:
            current.ypos=screen_height-current.height
        if current.ypos<0:
            current.ypos=0
        
        g.fall(current) #current block affected by gravity
        if checkCollision(current) == True:
            place(current)
            current = random_block()
            g = gravity(0.1)
                
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

        