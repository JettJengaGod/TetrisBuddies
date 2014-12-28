import threading
import Global
import pickle # pickle is used to package objects to be sent through sockets
from collections import deque
from socket import *

'''
PACKET

data[0]: command
    PlayingUpdate - Tells the receiver the sending player's gameboard info
    PlayingLine - Tells the receiver to add a line to gameboard
    PlayingLose - Tells the receiver that the sender lost
    PlayingWin - Tells the receiver that the sender won

    HostingInfo - Gives the receiver the sender's username info

    LobbyRequest - Tells the host receiver to give the sender info
    LobbyChallenge - Tells the host receiver that the sender is attempting to join

    HostAccept - Tells the joining receiver that the host accepted challenge
    HostReject - Tells the joining receiver that the host rejected challenge

            # If the current player is playing the game
            if Game.state == 'Playing':
                # If he receives an game update
                if command == 'PlayingUpdate':
                    print('placeholder')
                    # TODO: Update game board
                elif command == 'PlayingLine':
                    print('placeholder')
                elif command == 'PlayingLose':
                    Game.state = 'Results'
                    # TODO: Confirmation
                elif command == 'PlayingWin':
                    Game.state = 'Results'
                    # TODO: Confirmation

            # If the current player is joining
            elif Game.state == 'Joining':
                #If he gets an accepted challenge request
                if command == 'ChallengeAccept':
                    Game.state = 'Playing'
                    # TODO: Accept message
                #If he gets a denied request
                elif command == 'ChallengeDenied':
                    Game.state = 'Lobby'
                    # TODO: Deny message

            # If the current player is waiting in results
            elif Game.state == 'Result':
                # If the current player is a host and 
                if command == 'ResultRematch':
                    print('placeholder')
'''

# Handles basically all the networking things
class NetworkManager:

    # Constructor
    def __init__(self):
        # Start off by looking for a game
        self.state = 'Lobby'
        
        # Socket for sending and receiving data
        self.socket = socket(AF_INET, SOCK_DGRAM)

        # Gets the IP address of person running this program
        self.host = gethostbyname(gethostname())

        # bind() tells the socket to receive messages on port 6969
        self.socket.bind(('', 6969))

        # Setting some more specific socket options so that
        # we can broadcast messages to all clients in the LAN
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # Allows us to reuse an address, not entirely sure if needed
        # but probably safer to do so then not
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # The socket will receive messages and put them into this queue
        # The queue will then be popped off and the messages will be
        # responded to one by one
        self.messageQueue = deque()

        # Used for locking the messageQueuing so there are no synchronization
        # issues between threads
        self.messageLock = threading.Lock()

        # Starts the message thread
        # The parameter is target= because we are skipping the first argument
        # of the thread constructor and setting the second one directly
        self.messageThread = threading.Thread(target=self.checkForMessages)
        # Daemon tells the thread that it should stop if the main program stops
        self.messageThread.daemon = True
        self.messageThread.start()

    def getSocket(self): return self.socket
    def getMessageQueue(self): return self.messageQueue
    def getMessageLock(self): return self.messageLock

    # Receives packets(messages) and puts them into queue
    def checkForMessages(self):
        while Global.Game.getIsRunning():
            # recvfrom() will block the application until it receives a packet
            # The 4096 indicates that the socket will receive up to 4096 bytes
            # data is what the socket received
            # addr is where the information came from
            pickledData, addr = self.socket.recvfrom(4096)
            data = pickle.loads(pickledData)

            # Skip over packets if we have the same addresses
            if self.host == addr[0]:
                continue

            print('Received packet:', data)

            command = data[0]

            # Remember to lock so that we don't run into conflict accessing it
            self.messageLock.acquire()

            # These need to be check within the checkForMessages() thread because
            # they need to be responded immediately. If we put these sections in
            # the main thread they may get blocked when the Game() update() is waiting 
            # for input
            # If the current player is waiting in the Lobby
            if Global.Game.getState() == 'Lobby':
                # If new hosting info comes in
                if command == 'HostingInfo':
                    # Add username to the list of rooms
                    Global.Game.getRoomList().append(data[1])

            # If the current player is hosting
            elif Global.Game.getState() == 'Hosting':
                # If he gets a request for information then send it
                if command == 'LobbyRequest':
                    response = ['HostingInfo', Global.player.getName()]
                    packet = pickle.dumps(response)
                    self.socket.sendto(bytes(packet), addr)
                    print('Sent packet:', response)

                # If he gets a join request, then move to challenge
                elif command == 'LobbyChallenge':
                    invalidInput = True
                    
                    while invalidInput:
                        response = input('Accept challenge by ' + data[1] + ' (y/n)? ')
                        if response == 'y':
                            invalidInput = True
                            response = ['HostAccept']
                            packet = pickle.dumps(response)
                            self.socket.sendto(bytes(packet), addr)
                            print('Sent packet', response)

                            Global.Game.setState('Playing')
                            Global.opponent.setName(data[1])
                            Global.opponent.setAddr(addr[0])

                        elif response == 'n':
                            invalidInput = True
                            response = ['HostReject']
                            packet = pickle.dumps(response)
                            self.socket.sendto(bytes(packet), addr)
                            print('Sent packet', response)

            self.messageLock.release()
