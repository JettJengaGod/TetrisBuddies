import pygame

class gravity():
    def __int__(self,acc,inc):
        self._time = pygame.time.get_ticks()
        self._dropTime = acc
        self._increment = inc
        
    def fall(self,block):
        if pygame.time.get_ticks() - self._time > self._dropTime:
            block.y += 32
            self._time = pygame.time.get_ticks()
            self._dropTime -= self._increment
            