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
        blk.image.set_alpha(255)
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    screen.blit(blk.image,((x+blk.x)*sS,(y+blk.y)*sS))
    def drawGhost(blk):
        ghostBlock = blk.clone()
        ghostBlock.image.convert_alpha()
        ghostBlock.image.set_alpha(120)
        while 1:
            if grid.checkCol(ghostBlock):
                break
            else:
                ghostBlock.y += 1
        for x in range(0,4):
            for y in range(0,4):
                if ghostBlock.array[x][y]:
                    screen.blit(ghostBlock.image,((x+ghostBlock.x)*sS,(ghostBlock.y+y)*sS))
    def drawgrid():
        for x in range (col+1):
            for y in range(row+1):
                if grid.filled[x][y]:
                    grid.image[x][y].set_alpha(255)
                    screen.blit(grid.image[x][y],(x*sS,y*sS))
    def hardDrop(blk):
        while 1:
            if(grid.checkCol(blk)):
                blk = grid.place(blk)
                return blk
            blk.y+=1  
    def sideCol(blk,side):
        for a in range (4):
            for b in range (4):
                if blk.array[a][b]:
                    if grid.filled[side+blk.x+a][blk.y+b]:
                        return True
        return False
    current = grid.next.moveIn()
    grid.next = block()
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    
    pygame.display.set_caption("TetrisBuddies")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(((col+6)*sS,row*sS))
    
    # define a variable to control the main loop
    running = True
    keys = [False, False, False, False,False, False,False,False]
    # main loop
    grav = gravity(1000,5)
    saved = None
    while running:
        print(current.y)
        screen.fill((0,0,0)) #clear screen
        bkg =pygame.image.load("MaxFaggotry.png")
        screen.blit(bkg,(col*sS,0))
        drawBlock(current) #draws current block
        drawGhost(current)
        drawBlock(grid.next)
        if(saved!=None):
            drawBlock(saved)
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
                elif event.key==pygame.K_c:
                    keys[7]=True
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        if keys[0]:
            current.rotate("R")
            keys[0]=False
        elif keys[1]:
            if grid.checkCol(current)==False:
                current.y+=1
            else:
                grid.swapped = False
                current = grid.place(current)
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
            current = grid.next.moveIn()
            grid.next = block()
            keys[5] = False
        elif keys[6]:
            current = hardDrop(current)
            grid.swapped = False
            keys[6]=False
        elif keys[7]:
            if saved == None:
                saved = current.save()
                current = grid.next.moveIn()
                grid.next = block()
                grid.swapped = True
            elif grid.swapped==False:
                temp = current
                current = saved.moveIn()
                current.x = 1
                current.y = 1
                saved = temp.save()
                grid.swapped = True
            keys[7]=False
        current = grav.fall(current,grid)
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
