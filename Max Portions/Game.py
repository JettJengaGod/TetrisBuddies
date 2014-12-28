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

            # Looks for available hosts
            response = ['LobbyRequest']
            packet = pickle.dumps(response)
            Global.NetworkManager.getSocket().sendto(bytes(packet), ('<broadcast>', 6969))


            Global.player.setName(name)
            print('Hello ' + Global.player.getName() + '!')
            print()
            print("Changed state to Lobby")
            print("Instructions:")
            print("'h' to host a room")
            print("'v' to view available rooms")
            print("'0', '1', '2', ... to join a room")
            
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
                print("'Esc' to leave as host")

            # Look for rooms
            elif key == 'v':
                print('Rooms:')
                for roomIndex in range(len(self.roomList)):
                    print('Room', str(roomIndex), '-', self.roomList[roomIndex][0], '-', self.roomList[roomIndex][1])
                print()

                # Reset room list so we remove duplicates and offline players
                self.roomList = []

                response = ['LobbyRequest']
                packet = pickle.dumps(response)
                Global.NetworkManager.getSocket().sendto(bytes(packet), ('<broadcast>', 6969))
                print('Broadcasted packet', response)

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
                    print("'0', '1', '2', ... to join a room number")
                    return

                # If it is then check if it is within range of the roomList
                if roomIndex in range(len(self.roomList)):
                    # room[0] returns the username of the host
                    # room[1] returns the Network IP address of the room
                    room = self.roomList[roomIndex]
                    Global.opponent.setName(room[0])
                    Global.opponent.setAddr(room[1])

                    # Block and wait for other side to respond
                    self.clock.tick()
                    timer = 0

                    response = ['LobbyChallenge', Global.player.getName()]
                    packet = pickle.dumps(response)

                    # Send a join request
                    Global.NetworkManager.getSocket().sendto(bytes(packet), (Global.opponent.getAddr(), 6969))
                    print('Sent packet', response, Global.opponent.getAddr())

                    # Will poll for a message back, with a TTL of 5 seconds (5000 milliseconds)
                    while timer <= 10000:
                        timer += self.clock.tick()
                        print('.')
                        while Global.NetworkManager.getMessageQueue():
                            print('XXXXXXXXXXXXXXXXXXXXXX')
                            Global.NetworkManager.messageLock.acquire()
                            data, addr = Global.NetworkManager.getMessageQueue().popleft()
                            Global.NetworkManager.messageLock.release()

                            print('data', data)
                            command = data[0]

                            # If host rejects, then we just return to normal lobby activity
                            if command == 'HostingReject':
                                print('The host rejected your challenge')
                                print()
                                return
                            # Else we start playing the game
                            elif command == 'HostingAccept':
                                print('The host accepted your challenge')
                                print()
                                self.state = 'Playing'
                                return
                            else:
                                continue
                    
                    print('Challenge request timed out')

                else:
                    print('Invalid room number')

        # If hosting
        elif self.state == 'Hosting':
            print("Waiting for challengers, 'Esc' to leave...")

            # Block until we receive a challengeRequest
            # The message thread will spit out an exception here that we
            # will then catch
            try:
                import msvcrt
                while True:
                    if msvcrt.kbhit():
                        ascii = ord(msvcrt.getch())

                        # Escape key
                        if ascii == 27:
                            self.state = 'Lobby'
                            self.isHost = False
                                    
                            print('You left as host')
                            print()
                            print("Changed state to Lobby")
                            print("Instructions:")
                            print("'h' to host a room")
                            print("'v' to view available rooms")
                            print("'0', '1', '2', ... to join a room number")
                            return

            except KeyboardInterrupt:
                validInput = False

                data = None
                addr = None

                # Block until we get the right message in the queue
                while Global.NetworkManager.getMessageQueue():
                    Global.NetworkManager.messageLock.acquire()
                    data, addr = Global.NetworkManager.getMessageQueue().popleft()
                    Global.NetworkManager.messageLock.release()

                    if not data[0] == 'LobbyChallenge':
                        continue
                    else:
                        break

                while not validInput:
                    response = input('Accept challenge by ' + data[1] + ' (y/n)? ')
                    if response == 'y':
                        validInput = True
                        response = ['HostingAccept']
                        packet = pickle.dumps(response)
                        Global.NetworkManager.getSocket().sendto(bytes(packet), addr)
                        print('Sent packet', response, addr[0])

                        Global.Game.setState('Playing')
                        Global.opponent.setName(data[1])
                        Global.opponent.setAddr(addr[0])

                    elif response == 'n':
                        validInput = True
                        response = ['HostingReject']
                        packet = pickle.dumps(response)
                        Global.NetworkManager.getSocket().sendto(bytes(packet), addr)
                        print('Sent packet', response, addr[0])
                return

        elif self.state == 'Playing':
            # If playing, continuously send information to other person
            print('PLAYING GAME')
            response = ['Playing', Global.player.getName()]
            packet = pickle.dumps(response)
            Global.NetworkManager.getSocket().sendto(bytes(packet), (Global.opponent.getAddr(), 6969))
            print('Sent packet', response, Global.opponent.getAddr())
