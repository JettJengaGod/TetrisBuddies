import pygame

class gravity:
    def __init__(self,acc,inc):
        self._time = pygame.time.get_ticks()
        self._dropTime = acc
        self._increment = inc
        
    def fall(self,block):
        if pygame.time.get_ticks() - self._time > self._dropTime:
            block.y += 1
            self._time = pygame.time.get_ticks()
            self._dropTime -= self._increment
            