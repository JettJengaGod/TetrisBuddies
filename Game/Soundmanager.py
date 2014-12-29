import winsound
from random import randint

class soundmanager():
    def __init__(self):
        '''
        x=randint(1,12)
        if x<=2:
        '''
        # 200 MB of music is too much to work with, so I limited it to
        # 1 background track. Chose madoka since it's the smallest file...
        # and probably the most relevant
        winsound.PlaySound('madokatetris.wav', winsound.SND_ASYNC)

        '''
        elif x<=4:
            winsound.PlaySound('restofmylife.wav', winsound.SND_ASYNC)
        elif x<=6:
            winsound.PlaySound('heyea.wav', winsound.SND_ASYNC)
        elif x<=8:
            winsound.PlaySound('rmcinsanity.wav', winsound.SND_ASYNC)
        elif x<=10:
            winsound.PlaySound('ninjabang.wav', winsound.SND_ASYNC)
        elif x<=12:
            winsound.PlaySound('killself.wav', winsound.SND_ASYNC)
        '''
        
    def playsound(self, soundname):
        if soundname=='singleline':
            winsound.PlaySound('linecomplete.wav', winsound.SND_ASYNC)
        elif soundname=='fourline':
            winsound.PlaySound('tetriscomplete.wav', winsound.SND_ASYNC)
        elif soundname=='youfail':
            winsound.PlaySound('youfail.wav', winsound.SND_ASYNC)
        else:
            print("WHAT THE FUCK I CAN'T FIND THE SOUND FILE HELP!!!!")
