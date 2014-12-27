import random
class block:
   
    xpos = 40
    ypos = 40
    width = 20
    length = 20
    state = 0
    squares = [0,0,0,0,0,0,0,0]
    def __init__(self):
        self.xpos = 40
        self.ypos = 40
        self.width = 20
        self.width = 20
        x = random.randint(0,3)
        self.state=x
    def rotateR(self):
        self.squares=self.squares
        self.state=self.state+1
        if(self.state==4):
            self.state=0
            
    def rotateL(self):
        self.squares=self.squares
        if(self.state==0):
            self.state=3
        else:
            self.state = self.state-1
        
class square:
   
        width = 20 
        length = 20
class block_square(block):
    xpos = 40
    ypos = 40
    width = 40
    height = 40
    squares = [0,0,1,0,0,1,1,1]
    def rotateR(self):
        self.squares=self.squares
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
    def rotateL(self):
        self.squares=self.squares
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
class block_line(block):
    xpos = 40
    ypos = 40
    width = 80
    height = 20
    squares = [0,0,1,0,2,0,3,0]
    def rotateR(self):
        if(self.state==1):
            self.state=0
            self.squares=[0,0,1,0,2,0,3,0]
        else:
            self.state=1
            self.squares=[0,0,0,1,0,2,0,3]
    def rotateL(self):
        if(self.state==1):
            self.state=0
            self.squares=[0,0,1,0,2,0,3,0]
        else:
            self.state=1
            self.squares=[0,0,0,1,0,2,0,3]
            
class block_lzag(block):
    xpos = 40
    ypos = 40
    width = 60
    height = 40
    squares = [0,0,1,0,1,1,2,1]
    def rotateR(self):
        if(self.state==1):
            self.state=0
            self.squares = [0,0,1,0,1,1,2,1]
        else:
            self.state=1
            self.squares = [1,0,0,1,1,1,0,2]
        
    def rotateL(self):
        if(self.state==1):
            self.state=0
            self.squares = [0,0,1,0,1,1,2,1]
        else:
            self.state=1
            self.squares = [1,0,0,1,1,1,0,2]
class block_rzag(block):
    xpos = 40
    ypos = 40
    width = 60
    height = 40
    squares = [0,1,1,1,1,0,2,0]
    def rotateR(self):
        if(self.state==1):
            self.state=0
            self.squares = [0,1,1,1,1,0,2,0]
        else:
            self.state=1
            self.squares = [0,0,0,1,1,1,1,2]
        
    def rotateL(self):
        if(self.state==1):
            self.state=0
            self.squares = [0,1,1,1,1,0,2,0]
        else:
            self.state=1
            self.squares = [0,0,0,1,1,1,1,2]
class block_lhook(block):
    xpos = 40
    ypos = 40
    width = 60
    height = 40
    squares = [0,0,0,1,1,1,2,1]
    def rotateR(self):
        self.squares=self.squares
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
        if(self.state==0):
            self.squares=[0,0,0,1,1,1,2,1]
        elif(self.state==1):
            self.squares=[0,0,1,0,0,1,0,2]
        elif(self.state==2):
            self.squares=[0,0,1,0,2,0,2,1]
        elif(self.state==3):
            self.squares=[1,0,1,1,1,2,0,2]
    def rotateL(self):
        self.squares=self.squares
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
        if(self.state==0):
            self.squares=[0,0,0,1,1,1,2,1]
        elif(self.state==1):
            self.squares=[0,0,1,0,0,1,0,2]
        elif(self.state==2):
            self.squares=[0,0,1,0,2,0,2,1]
        elif(self.state==3):
            self.squares=[1,0,1,1,1,2,0,2]
class block_rhook(block):
    xpos = 40
    ypos = 40
    width = 60
    height = 40
    squares = [0,1,1,1,2,1,2,0]
    def rotateR(self):
        self.squares=self.squares
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
        if(self.state==0):
            self.squares=[0,1,1,1,2,1,2,0]
        elif(self.state==1):
            self.squares=[0,0,0,1,0,2,1,2]
        elif(self.state==2):
            self.squares=[0,0,1,0,2,0,0,1]
        elif(self.state==3):
            self.squares=[0,0,0,1,0,2,1,2]
    def rotateL(self):
        self.squares=self.squares
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
        if(self.state==0):
            self.squares=[0,1,1,1,2,1,2,0]
        elif(self.state==1):
            self.squares=[0,0,0,1,0,2,1,2]
        elif(self.state==2):
            self.squares=[0,0,1,0,2,0,0,1]
        elif(self.state==3):
            self.squares=[0,0,0,1,0,2,1,2]
class block_t(block):
    xpos = 40
    ypos = 40
    width = 60
    height = 40
    squares = [0,1,1,1,1,0,2,1]
    def rotateR(self):
        self.squares=self.squares
        if(self.state==3):
            self.state=0
        else:
            self.state=self.state+1
        if(self.state==0):
            self.squares=[0,1,1,1,1,0,2,1]
        elif(self.state==1):
            self.squares=[1,0,1,1,1,2,2,1]
        elif(self.state==2):
            self.squares=[0,1,1,1,2,1,1,2]
        elif(self.state==3):
            self.squares=[1,0,1,1,1,2,0,1]
            
            
    def rotateL(self):
        self.squares=self.squares
        if(self.state==0):
            self.state=3
        else:
            self.state=self.state-1
        if(self.state==0):
            self.squares=[0,1,1,1,1,0,2,1]
        elif(self.state==1):
            self.squares=[1,0,1,1,1,2,2,1]
        elif(self.state==2):
            self.squares=[0,1,1,1,2,1,1,2]
        elif(self.state==3):
            self.squares=[1,0,1,1,1,2,0,1]
    