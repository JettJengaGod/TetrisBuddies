import threading
import Global
import pickle # pickle is used 
from collections import deque
from socket import *

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

    # Receives packets(messages) and puts them into queue
    def checkForMessages(self):
        while Global.Game.getIsRunning():
            # recvfrom() will block the application until it receives a packet
            # The 4096 indicates that the socket will receive up to 4096 bytes
            # data is what the socket received
            # addr is where the information came from
            pickledData, addr = self.socket.recvfrom(4096)
            data = pickle.loads(pickledData)

            # Remember to lock so that we don't run into conflict accessing it
            self.messageLock.acquire()
            # Puts the received info into the queue
            self.messageQueue.append((data, addr))
            self.messageLock.release()

    # Processes the messages
    def processMessages(self):
        # Empty queues are False
        while self.messageQueue:
            # Pop off message and respond to it
            self.messageLock.acquire()
            data, addr = self.messageQueue.popleft()
            self.messageLock.release()

            print()
            print('Processed packet:')
            print(data, addr)

            command = data[0]

            # If the current player is waiting in the Lobby
            if Global.Game.getState() == 'Lobby':
                # If new hosting info comes in
                if command == 'HostingInfo':
                    # TODO: Update current rommList information
                    Global.Game.getRoomList().append(data[1])

            # If the current player is hosting
            elif Global.Game.getState() == 'Hosting':
                # If he gets a request for information then send it
                if command == 'LobbyRequest':
                    response = ['HostingInfo', Global.player.getName()]
                    packet = pickle.dumps(response)
                    self.socket.sendto(bytes(packet), addr)
                # If he gets a join request, then move to challenge
                elif command == 'JoiningChallenge':
                    Global.Game.state = 'Challenge'
                    # TODO: Give host choice to accept or reject offer

    # Handles processing and sending messages
    def update(self):
        self.processMessages()
 
    # Broadcasts a message looking for available room info
    def requestRooms(self):
        response = ['LobbyRequest']
        packet = pickle.dumps(response)
        print('Sent broadcast')
        self.socket.sendto(bytes(packet), ('<broadcast>', 6969))

'''
PACKET

data[0]: command
    PlayingUpdate - Tells the receiver the sending player's gameboard info
    PlayingLine - Tells the receiver to add a line to gameboard
    PlayingLose - Tells the receiver that the sender lost
    PlayingWin - Tells the receiver that the sender won

    HostingInfo - Gives the receiver the sender's username info

    LobbyRequest - Tells the host receiver to give the sender info
    JoiningChallenge - Tells the host receiver that the sender is attempting to join

    ChallengeAccept - Tells the joining receiver that the host accepted challenge
    ChallengeReject - Tells the joining receiver that the host rejected challenge

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
