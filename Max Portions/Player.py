from Global import *

class Player:
    # Constructor
    def __init__(self):
        # Make blank names
        self.name = ''
        self.addr = ''

    # Name accessor, setter
    def getName(self): return self.name
    def setName(self, newName): self.name = newName

    def getAddr(self): return self.addr
    def setAddr(self, newAddr): self.addr = newAddr
