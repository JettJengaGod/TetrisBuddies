import pygame
class cells:
    def __init__(self,col,row):
        image = pygame.image.load("blockB.png")
        self.filled = [[0 for x in range(row+1)] for x in range(col+1)]
        self.image = [[image for x in range(row +1)]for x in range(col+1)]