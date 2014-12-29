import pygame
from block2 import block
class cells:
    def __init__(self,col,row):
        self.col = col
        self.row = row
        self.next = block()
        self.swapped = False
        image = pygame.image.load("block1.png")
        self.default = image
        self.filled = [[0 for x in range(row+1)] for x in range(col+1)]
        self.image = [[image for x in range(row +1)]for x in range(col+1)]
        for x in range(col+1):
            self.filled[x][row]=1
    def rowFilled(self):
        for y in range (self.row):
            clear = True
            for x in range(self.col):
                if self.filled[x][y]!=1:
                    clear = False
                if x == self.col-1 and clear:
                    self.clear(y)
    def place(self,blk):
        self.swapped = False
        for x in range(0,4):
            for y in range(0,4):
                if blk.array[x][y]:
                    self.filled[blk.x+x][blk.y+y]=1
                    self.image[blk.x+x][blk.y+y]=blk.image
        self.rowFilled()
        blk = self.next.moveIn()
        self.next = block()
        return blk
    def checkCol(self,blk):
        for y in range(self.row+1):
            for x in range(4):
                if blk.bottom()[x]!=-1:
                    if self.filled[blk.x+x][blk.y+blk.bottom()[x]+1]:
                        return True
        return False     
    def clear(self,y):
        for x in range(self.col+1):
            self.filled[x][y] = 0
            self.image[x][y] = self.default
        for b in range (y,0,-1):
            for x in range(self.col+1):
                self.filled[x][b]=self.filled[x][b-1]
                self.image[x][b]=self.image[x][b-1]
                    