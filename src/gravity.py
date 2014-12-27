import pygame

class gravity():
    def __init__(self):
        self._time = pygame.time.get_ticks()
    
    def fall(self,block,speed):
        if (pygame.time.get_ticks() - self._time) > 10:
            block.ypos += speed
            self._time = pygame.time.get_ticks()