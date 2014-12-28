# import the pygame module, so you can use it
import pygame
import block2
from block2 import block
# define a main function

def main():
    col = 10
    row = 20
    sS = 32
    cells =[[0 for x in range(row+2)] for x in range(col+1)] 
    for x in range(col+1):
        cells[x][row+1]=1
    def drawBlock(blk):
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    screen.blit(image,((x+blk.x)*sS,(y+blk.y)*sS))
    def drawCells():
        for x in range (col+1):
            for y in range(row+1):
                if cells[x][y]:
                    screen.blit(image,(x*sS,y*sS))
    def place(blk):
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    cells[blk.x+x][blk.y+y]=True
    current = block(1,1)
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    image = pygame.image.load("blockB.png")
    pygame.display.set_icon(image)
    pygame.display.set_caption("TetrisBuddies")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((col*sS,row*sS))
    
    # define a variable to control the main loop
    running = True
    keys = [False, False, False, False,False, False,False]
    # main loop
    while running:
        screen.fill((0,0,0)) #clear screen
        drawBlock(current); #draws current block
        drawCells()
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
            current.y+=1
            keys[1]=False
        elif keys[2]:
            if current.x+current.left()>0:
                current.x-=1
            keys[2]=False
        elif keys[3]:
            if current.x+current.right()+1<col:
                current.x+=1
            keys[3]=False
        elif keys[4]:
            current.rotate("L")
            keys[4]=False
        elif keys[5]:
            current = block(1,1)
            keys[5] = False
        elif keys[6]:
            place(current)
            current = block(1,1)
            keys[6]=False
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
