class block:
   
    xpos = 40
    ypos = 40
    width = 20
    length = 20
    squares = [0,0,0,0,0,0,0,0]
class square:
   
        width = 20 
        length = 20
class block_square(block):
        xpos = 40
        ypos = 40
        width = 40
        height = 40
        squares = [0,0,1,0,0,1,1,1]
class block_line(block):
        xpos = 40
        ypos = 40
        width = 80
        height = 20
        squares = [0,0,1,0,2,0,3,0]
class block_lzag(block):
        xpos = 40
        ypos = 40
        width = 60
        height = 40
        squares = [0,0,1,0,1,1,2,1]
class block_rzag(block):
        xpos = 40
        ypos = 40
        width = 60
        height = 40
        squares = [0,1,1,1,1,0,2,0]
class block_lhook(block):
        xpos = 40
        ypos = 40
        width = 60
        height = 40
        squares = [0,0,0,1,1,1,2,1]
class block_rhook(block):
        xpos = 40
        ypos = 40
        width = 60
        height = 40
        squares = [0,1,1,1,2,1,2,0]