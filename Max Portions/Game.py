import Global
import pygame
import pickle
from Player import *
from NetworkManager import NetworkManager

'''
STATES
    Lobby - Looking for available games
    Hosting - Hosting a room that is available for play
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
        pygame.init()
        self.clock = pygame.time.Clock()

    # Accessors
    def getRoomList(self): return self.roomList
    def getState(self): return self.state
    def getIsRunning(self): return self.isRunning

    # Setters
    def setState(self, newState): self.state = newState

    # Lets Game handle everything here
    def run(self):
        # Force game to run roughly at 60FPS
        self.clock.tick(60)

        while self.isRunning:
            self.update()
        
    def update(self):
        # Separation text
        print()
        print('---------------------------------------------------------------')
        print()

        # The first thing to do is give yourself a name
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
            print("'1', '2', '3', ... to join a room")
            
            self.state = 'Lobby'

        # If in lobby, then browse for games or become a host
        elif self.state == 'Lobby':
            key = input("Enter a command: ")
            print()
            
            # Become a host
            if key == 'h':
                self.state = 'Hosting'
                self.isHost = True

                print('You are now hosting a game')
                print()
                print("Changed state to Hosting")
                print("Instructions:")
                print("'l' to leave as host")

            # Look for rooms
            elif key == 'v':
                print('Rooms:')
                print(self.roomList)
                for roomIndex in range(len(self.roomList)):
                    print('Room ' + str(roomIndex) + ' - ' + self.roomList[roomIndex])
                Global.NetworkManager.requestRooms()
                print()

            # Else display instructions
            else:
                # Checks if the key is a number
                try:
                    roomIndex = int(key)
                except ValueError:
                    print("Invalid command")
                    print()
                    print("Instructions:")
                    print("'h' to host a room") 
                    print("'v' to view available rooms")
                    return
                
                # If it is then check if it is within range of the roomList
                if roomIndex in range(len(self.roomList)):
                    # room[0] returns the username of the host
                    # room[1] returns the Network IP address of the room
                    room = roomList[roomIndex]
                    Global.opponent.setName(room[0])
                    Global.opponent.setAddr(room[1])

                    # Block and wait for other side to respond
                    self.clock.tick()
                    timer = 0

                    response = ['LobbyChallenge', Global.player.getName()]
                    packet = pickle.dumps(response)

                    # Send a join request
                    Global.NetworkManager.getSocket().sendto(bytes(packet), (Global.opponent.getAddr(), 6969))

                    # Will poll for a message back, with a TTL of 5 seconds (5000 milliseconds)
                    while timer <= 5000:
                        timer += self.clock.tick()
                        if Global.NetworkManager.getMessageQueue():
                            Global.NetworkManager.messageLock.acquire()
                            data, addr = Global.NetworkManager.getMessageQueue().popLeft()
                            Global.NetworkManager.messageLock.release()

                            command = data[0]

                            # If host rejects, then we just return to normal lobby activity
                            if command == 'HostReject':
                                print('The host rejected your challenge')
                                print()
                                return
                            # Else we start playing the game
                            elif command == 'HostAccept':
                                print('The host accepted your challenge')
                                print()
                                self.state = 'Playing'
                                return
                    
                    print('Challenge request timed out')

                else:
                    print("Invalid room number")

        # If hosting
        elif self.state == 'Hosting':
            key = input("Enter a command: ")
            print()
            
            # Return to lobby and quit as host
            if key == 'l':
                self.state = 'Lobby'
                self.isHost = False

                print('You left as host')
                print()
                print("Changed state to Lobby")
                print("Instructions:")
                print("'h' to host a room")
                print("'v' to view available rooms")
                print("'1', '2', '3', ... to join a room")

            # Else display instructions
            else:
                print("Invalid command")
                print()
                print("Instructions:")
                print("'l' to leave as host")

        elif self.state == 'Playing':
            # If playing, continuously send information to other person
            print('PLAYING GAME')
            response = ['Playing', Global.player.getName()]
            packet = pickle.dumps(response)
            Global.NetworkManager.getSocket().sendto(bytes(packet), (Global.opponent.getAddr(), 6969))
