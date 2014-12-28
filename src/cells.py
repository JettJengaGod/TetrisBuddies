import pygame
class cells:
    def __init__(self,col,row):
        self.col = col
        self.row = row
        image = pygame.image.load("blockB.png")
        self.default = image
        self.filled = [[0 for x in range(row+1)] for x in range(col+1)]
        self.image = [[image for x in range(row +1)]for x in range(col+1)]
        for x in range(col+1):
            self.filled[x][row]=1
    def rowFilled(self):
        print("*")
        for y in range (self.row-1,0,-1):
            for x in range(self.col):
                if self.filled[x][y]!=1:
                    break
                if x == self.col-1:
                    self.clear(y)
    def clear(self,y):
        print("**")
        for x in range(self.col+1):
            self.filled[x][y] = 0
            self.image[x][y] = self.default
        for b in range (y,0,-1):
            for x in range(self.col+1):
                self.filled[x][b]=self.filled[x][b-1]
                self.image[x][b]=self.image[x][b-1]
                    