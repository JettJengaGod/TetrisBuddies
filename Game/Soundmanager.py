import winsound
from random import randint

class soundmanager():
    def __init__(self):
        x=randint(1,12)
        if x<=2:
            winsound.PlaySound('madokatetris.wav', winsound.SND_LOOP)
        elif x<=4:
            winsound.PlaySound('restofmylife.wav', winsound.SND_LOOP)
        elif x<=6:
            winsound.PlaySound('heyea.wav', winsound.SND_LOOP)
        elif x<=8:
            winsound.PlaySound('rmcinsanity.wav', winsound.SND_LOOP)
        elif x<=10:
            winsound.PlaySound('ninjabang.wav', winsound.SND_LOOP)
        elif x<=12:
            winsound.PlaySound('killself.wav', winsound.SND_LOOP)
        
    def playsound(self, soundname):
        if soundname=='singleline':
            winsound.PlaySound('linecomplete.wav', winsound.SND_LOOP)
        elif soundname=='fourline':
            winsound.PlaySound('tetriscomplete.wav', winsound.SND_LOOP)
        elif soundname=='youfail':
            winsound.PlaySound('youfail.wav', winsound.SND_LOOP)
        else:
            print("WHAT THE FUCK I CAN'T FIND THE SOUND FILE HELP!!!!")
