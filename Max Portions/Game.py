import Global
from Player import *
from NetworkManager import NetworkManager

'''
STATES
    Lobby - Looking for available games
    Hosting - Hosting a room that is available for play
    Joining - Attemping to join a room
    Challenge - Host is challenged by a joiner
    Playing - Playing a game
    Results - After playing a game, wait in the room
'''

class Game:
    isHost = False
    isRunning = True
    roomList = []

    # Constructor
    def __init__(self):
        # Start off by looking for a game
        self.state = 'NameSelection'

    # initialize() is ran after the constructor because we may
    # need access to member variables that aren't constructed yet
    def initialize(self):
        Global.NetworkManager = NetworkManager()
        Global.player = Player()
        Global.opponent = Player()

    def getRoomList(self): return self.roomList
    def getState(self): return self.state
    def getIsRunning(self): return self.isRunning

    # Lets Game handle everything here
    def run(self):
        while self.isRunning:
            self.update()

    def update(self):
        Global.NetworkManager.update()

        print()
        print('---------------------------------------------------------------')
        print()
        if self.state == 'NameSelection':
            name = input('To get started, enter a name: ')

            Global.NetworkManager.requestRooms()

            Global.player.setName(name)
            print('Hello ' + Global.player.getName() + '!')
            print()
            print("Changed state to Lobby")
            print("Instructions:")
            print("'h' to host a room")
            print("'v' to view available rooms")
            print("'1' through '9' to join rooms 1 through 9")
            
            self.state = 'Lobby'

        elif self.state == 'Lobby':
            key = input("Enter a command: ")
            print()

            if key == 'h':
                self.state = 'Hosting'
                self.isHost = True

                print('You are now hosting a game')
                print()
                print("Changed state to Hosting")
                print("Instructions:")
                print("'l' to leave as host")

            elif key == 'v':
                Global.NetworkManager.requestRooms()
                print('Rooms:')
                print(self.roomList)
                for roomIndex in range(len(self.roomList)):
                    print('Room ' + roomIndex + '- ' + self.roomList[roomIndex])
                print()

            else:
                print("Invalid command")
                print()
                print("Instructions:")
                print("'h' to host a room") 
                print("'v' to view available rooms")

        elif self.state == 'Hosting':
            key = input("Enter a command: ")
            print()
            
            if key == 'l':
                self.state = 'Lobby'
                self.isHost = True

                print('You left as host')
                print()
                print("Changed state to Lobby")
                print("Instructions:")
                print("'h' to host a room")
                print("'v' to view available rooms")
                print("'1' through '9' to join rooms 1 through 9")

            else:
                print("Invalid command")
                print()
                print("Instructions:")
                print("'l' to leave as host")
