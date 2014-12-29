# import the pygame module, so you can use it
import pygame
import block2
from block2 import block
from gravity2 import gravity
from cells import cells

class gameBoard():
    def __init__(self):
        self.col = 10
        self.row = 20
        self.sS = 32
        self.grid = cells(self.col,self.row)
        self.current = self.grid.next.moveIn()
        self.grid.next = block()
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        pygame.display.set_caption("TetrisBuddies")
        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode(((self.col+6)*self.sS,self.row*self.sS))
        # define a variable to control the main loop
        self.running = True
        self.keys = [False, False, False, False,False, False,False,False]
        # main loop
        self.grav = gravity(1000,5)
        self.saved = None
    def update(self):
        self.screen.fill((55,55,55)) #clear screen
        bkg =pygame.image.load("MaxFaggotry.png")
        self.screen.blit(bkg,(self.col*self.sS,0))
        self.drawBlock(self.current) #draws current block
        self.drawGhost(self.current)
        self.drawBlock(self.grid.next)
        if(self.saved!=None):
            self.drawBlock(self.saved)
        self.drawgrid()
        pygame.display.flip() #updates self.screen
    def drawBlock(self,blk):
        image = pygame.image.load(blk.image)
        image.set_alpha(255)
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    self.screen.blit(image,((x+blk.x)*self.sS,(y+blk.y)*self.sS))
    def drawGhost(self,blk):
        image = pygame.image.load(blk.image)
        ghostBlock = blk.clone()
        image.convert_alpha()
        image.set_alpha(120)
        while 1:
            if self.grid.checkCol(ghostBlock):
                break
            else:
                ghostBlock.y += 1
        for x in range(0,4):
            for y in range(0,4):
                if ghostBlock.array[x][y]:
                    self.screen.blit(image,((x+ghostBlock.x)*self.sS,(ghostBlock.y+y)*self.sS))
    def drawgrid(self):
        for x in range (self.col):
            for y in range(self.row+1):
                if self.grid.filled[x][y]:
                    image = pygame.image.load(self.grid.image[x][y])
                    image.set_alpha(255)
                    self.screen.blit((image),(x*self.sS,y*self.sS))
    def hardDrop(self,blk):
        while 1:
            if(self.grid.checkCol(blk)):
                blk = self.grid.place(blk)
                return blk
            blk.y+=1  
    def sideCol(self,blk,side):
        for a in range (4):
            for b in range (4):
                if blk.array[a][b]:
                    if self.grid.filled[side+blk.x+a][blk.y+b]:
                        return True
        return False
    def flipNudge(self,blk, LR):
        if(blk._arrangement == block2.block_Sq):
            return
        temp = blk.clone()
        temp.rotate(LR)
        while temp.x < 0:
            temp.x+=1
            blk.x+=1
        while (temp.right() == 3 and temp.x >6):
            blk.x -= 1
            temp.x -= 1
        for x in range(4):
            if temp.array[x]:
                if temp.x + x>self.col:
                    blk.x -= 1
                    temp.x -= 1
                    if temp.x +x> self.col:
                        blk.x
                        temp.x -= 1
                    if temp._arrangement == block2.block_S:
                        temp.x -= 1
        if self.sideCol(temp,-1) == True and self.sideCol(temp,1) == True:
            return 'GG'
        if self.sideCol(temp,0) == True:
            for x in range(4):
                for y in range(4):
                    if temp.array[x][y]:
                        if self.grid.filled[temp.x+x][temp.y+y]:
                            if x>1:
                                blk.x-=1
                            else:
                                blk.x+=1
        return None
    


    def run(self):
        while self.running:
            # event handling, gets all event from the eventqueue
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_w or event.key==pygame.K_UP:
                        self.keys[0]=True
                    elif event.key==pygame.K_s or event.key==pygame.K_DOWN:
                        self.keys[1]=True
                    elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
                        self.keys[2]=True
                    elif event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                        self.keys[3]=True
                    elif event.key==pygame.K_t:
                        self.keys[4]=True
                    elif event.key==pygame.K_r:
                        self.keys[5]=True
                    elif event.key==pygame.K_SPACE:
                        self.keys[6]=True
                    elif event.key==pygame.K_c:
                        self.keys[7]=True
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            if self.keys[0]:
                self.flipNudge(self.current,"R")
                self.current.rotate('R')
                self.keys[0]=False
            elif self.keys[1]:
                if self.grid.checkCol(self.current)==False:
                    self.current.y+=1
                else:
                    self.grid.swapped = False
                    self.current = self.grid.place(self.current)
                self.keys[1]=False
            elif self.keys[2]:
                if (self.current.x+self.current.left()>0
                    and self.sideCol(self.current, -1)==False):
                    self.current.x-=1
                self.keys[2]=False
            elif self.keys[3]:
                if (self.current.x+self.current.right()+1<self.col
                    and self.sideCol(self.current, 1)==False):
                    self.current.x+=1
                self.keys[3]=False
            elif self.keys[4]:
                self.flipNudge(self.current,"L")
                self.current.rotate('L')
                self.keys[4]=False
            elif self.keys[5]:
                self.current = self.grid.next.moveIn()
                self.grid.next = block()
                self.grid.addLines(1)
                self.keys[5] = False
            elif self.keys[6]:
                self.current = self.hardDrop(self.current)
                self.grid.swapped = False
                self.keys[6]=False
            elif self.keys[7]:
                if self.saved == None:
                    self.saved = self.current.save()
                    self.current = self.grid.next.moveIn()
                    self.grid.next = block()
                    self.grid.swapped = True
                elif self.grid.swapped==False:
                    temp = self.current
                    self.current = saved.moveIn()
                    self.current.x = 1
                    self.current.y = 1
                    saved = temp.save()
                    self.grid.swapped = True
                self.keys[7]=False
            self.current = self.grav.fall(self.current,self.grid)
            self.update()
g = gameBoard()
g.run()