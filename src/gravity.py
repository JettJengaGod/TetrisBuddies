import pygame

class gravity():
    def __init__(self,speed):
        self._time = pygame.time.get_ticks()
        self._acc = pygame.time.get_ticks()
        self._speed = speed
    
    def fall(self,block):
        if (pygame.time.get_ticks() - self._time) > 10:
            block.ypos += self._speed
            self._time = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - self._acc) > 4000:
            self._speed += self._speed
            self._acc = pygame.time.get_ticks()