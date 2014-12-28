# import the pygame module, so you can use it
import pygame
from block2 import block
from gravity2 import gravity
from cells import cells
# define a main function

def main():
    col = 10
    row = 20
    sS = 32
    grid = cells(col,row)
    def drawBlock(blk):
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    screen.blit(blk.image,((x+blk.x)*sS,(y+blk.y)*sS))
    def drawgrid():
        for x in range (col+1):
            for y in range(row+1):
                if grid.filled[x][y]:
                    screen.blit(grid.image[x][y],(x*sS,y*sS))
    def place(blk):
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    grid.filled[blk.x+x][blk.y+y]=1
                    grid.image[blk.x+x][blk.y+y]=blk.image
        grid.rowFilled()
    def checkCol(blk):
        for y in range(row+1):
            for x in range(4):
                if blk.bottom()[x]!=-1:
                    if grid.filled[blk.x+x][blk.y+blk.bottom()[x]+1]:
                        return True
        return False        
    def hardDrop(blk):
        while 1:
            if(checkCol(blk)):
                place(blk)
                return
            blk.y+=1  
    def sideCol(blk,side):
        for a in range (4):
            for b in range (4):
                if blk.array[a][b]:
                    if grid.filled[side+blk.x+a][blk.y+b]:
                        return True
        return False
    current = block(1,1)
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    
    pygame.display.set_caption("TetrisBuddies")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((col*sS,row*sS))
    
    # define a variable to control the main loop
    running = True
    keys = [False, False, False, False,False, False,False]
    # main loop
    grav = gravity(1000,10)
    while running:
        if checkCol(current)==False:
            grav.fall(current)
        else:
            place(current)
            current = block(1,1)

        screen.fill((0,0,0)) #clear screen
        drawBlock(current); #draws current block
        drawgrid()
        pygame.display.flip() #updates screen
        # event handling, gets all event from the eventqueue
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
                elif event.key==pygame.K_t:
                    keys[4]=True
                elif event.key==pygame.K_r:
                    keys[5]=True
                elif event.key==pygame.K_SPACE:
                    keys[6]=True
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        if keys[0]:
            current.rotate("R")
            keys[0]=False
        elif keys[1]:
            if checkCol(current)==False:
                current.y+=1
            else:
                place(current)
                current = block(1,1)
            keys[1]=False
        elif keys[2]:
            if (current.x+current.left()>0
                and sideCol(current, -1)==False):
                current.x-=1
            keys[2]=False
        elif keys[3]:
            if (current.x+current.right()+1<col
                and sideCol(current, 1)==False):
                current.x+=1
            keys[3]=False
        elif keys[4]:
            current.rotate("L")
            keys[4]=False
        elif keys[5]:
            current = block(1,1)
            keys[5] = False
        elif keys[6]:
            hardDrop(current)
            current = block(1,1)
            keys[6]=False
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
