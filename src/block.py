import random
class block:
    xpos = 0
    ypos = 0
    width = 0
    height = 0
    state = 0
    squares=[0,0,0,0,0,0,0,0]
    def setSquares(self):
        self.squares=[0,0,0,0,0,0,0,0]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.height = 20
        x = random.randint(0,3)
        self.state=x
    def rotateR(self):
        
        self.state=self.state+1
        if(self.state==4):
            self.state=0
            
    def rotateL(self):
        
        if(self.state==0):
            self.state=3
        else:
            self.state = self.state-1
class block_square(block):
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 40
        self.height = 40
        self.squares = [0,0,1,0,0,1,1,1]
    def rotateR(self):
        
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
    def rotateL(self):
        
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
class block_line(block):
    def setSquares(self):
        if(self.state==1):
            self.squares=[0,0,1,0,2,0,3,0]
        else:
            self.squares=[0,0,0,1,0,2,0,3]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 80
        self.height = 20
        x = random.randint(0,1)
        self.state=x
        self.setSquares()
    def rotateR(self):
        if(self.state==1):
            self.state=0
        else:
            self.state=1
        self.setSquares()
    def rotateL(self):
        if(self.state==1):
            self.state=0
        else:
            self.state=1
        self.setSquares()
            
class block_lzag(block):
    def setSquares(self):
        if(self.state==1):
            self.squares = [0,0,1,0,1,1,2,1]
        else:
            self.squares = [1,0,0,1,1,1,0,2]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.width = 20
        x = random.randint(0,3)
        self.state=x
        self.setSquares()

    def rotateR(self):
        if(self.state==1):
            self.state=0
        else:
            self.state=1
        self.setSquares()
    def rotateL(self):
        if(self.state==1):
            self.state=0
        else:
            self.state=1
        self.setSquares()
class block_rzag(block):
    def setSquares(self):
        if(self.state==1):
            self.squares = [0,1,1,1,1,0,2,0]
        else:
            self.squares = [0,0,0,1,1,1,1,2]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.width = 20
        x = random.randint(0,3)
        self.state=x
        self.setSquares()
    def rotateR(self):
        if(self.state==1):
            self.state=0
        else:
            self.state=1
        self.setSquares()
    def rotateL(self):
        if(self.state==1):
            self.state=0
        else:
            self.state=1
        self.setSquares()
class block_lhook(block):
    def setSquares(self):
        if(self.state==0):
            self.squares=[0,0,0,1,1,1,2,1]
        elif(self.state==1):
            self.squares=[0,0,1,0,0,1,0,2]
        elif(self.state==2):
            self.squares=[0,0,1,0,2,0,2,1]
        elif(self.state==3):
            self.squares=[1,0,1,1,1,2,0,2]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.width = 20
        x = random.randint(0,3)
        self.state=x
        self.setSquares()
    def rotateR(self):
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
        self.setSquares()
    def rotateL(self):
        
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
        self.setSquares()
class block_rhook(block):
    def setSquares(self):
        if(self.state==0):
            self.squares=[0,1,1,1,2,1,2,0]
        elif(self.state==1):
            self.squares=[0,0,0,1,0,2,1,2]
        elif(self.state==2):
            self.squares=[0,0,1,0,2,0,0,1]
        elif(self.state==3):
            self.squares=[0,0,0,1,0,2,1,2]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.width = 20
        x = random.randint(0,3)
        self.state=x
        self.setSquares()
    def rotateR(self):
        
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
        self.setSquares()
    def rotateL(self):
        
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
        self.setSquares()
class block_t(block):
    def setSquares(self):
        if(self.state==0):
            self.squares=[0,1,1,1,1,0,2,1]
        elif(self.state==1):
            self.squares=[1,0,1,1,1,2,2,1]
        elif(self.state==2):
            self.squares=[0,1,1,1,2,1,1,2]
        elif(self.state==3):
            self.squares=[1,0,1,1,1,2,0,1]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.width = 20
        x = random.randint(0,3)
        self.state=x
        self.setSquares()
    def rotateR(self):
        
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
        self.setSquares()
    def rotateL(self):
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
        self.setSquares()
    