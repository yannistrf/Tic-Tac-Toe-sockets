import socket
import util


class Server:
    def __init__(self):
        # Game representation
        """
             0 -> empty
             1 -> O
            -1 -> X
        """
        self.table = [[0,0,0], [0,0,0], [0,0,0]]

        self.port = int(input("ENTER THE PORT YOU WANT TO RUN THE GAME ON: "))
        self.acceptSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to setup the socket        
        try:
            self.acceptSock.bind(("", self.port))
        except socket.error:
            print("[PORT IS USED FROM ANOTHER SERVICE]")
            print("[EXITING...]")
            exit(-1)

        self.acceptSock.listen(2)
        print("[SERVER SETUP COMPLETE]")

    def acceptConnections(self):
        print("[WAITING FOR PLAYERS TO CONNECT]")

        self.sockP1, self.addrP1 = self.acceptSock.accept()
        print(f"[PLAYER 1 CONNECTED {self.addrP1[0]}:{self.addrP1[1]}]")
        # Inform the first player he needs to wait
        util.sendCode(self.sockP1, util.WAIT_OPPONENT_CONNECTION)

        self.sockP2, self.addrP2 = self.acceptSock.accept()
        print(f"[PLAYER 2 CONNECTED {self.addrP2[0]}:{self.addrP2[1]}]")
        # Inform both players that the game is starting
        util.sendCode(self.sockP1, util.GAME_BEGINS)
        util.sendCode(self.sockP2, util.GAME_BEGINS)

        self.acceptSock.close()

    def run(self):
        playingSock = self.sockP1
        waitingSock = self.sockP2
        symbol = 1

        while True:
            # Check if the game has ended
            status = util.check_status(self.table)
            if status == 1:
                util.sendCode(self.sockP1, util.WON)
                util.sendCode(self.sockP2, util.LOST)
                print("[PLAYER 1 WON]")
                break
            elif status == -1:
                util.sendCode(self.sockP1, util.LOST)
                util.sendCode(self.sockP2, util.WON)
                print("[PLAYER 2 WON]")
                break
            elif status == 2:
                util.sendCode(self.sockP1, util.TIE)
                util.sendCode(self.sockP2, util.TIE)
                print("[TIE]")
                break

            # If the game continues
            util.sendCode(playingSock, util.PLAY)
            util.sendCode(waitingSock, util.WAIT)
            
            move = util.recvMove(playingSock)
            self.table[move[0]][move[1]] = symbol

            util.sendMove(waitingSock, move)

            # Log the plays of each player
            if symbol == 1:
                print(f"[PLAYER 1 -> {(move[0]+1, move[1]+1)}]")
            else:
                print(f"[PLAYER 2 -> {(move[0]+1, move[1]+1)}]")	
		
            # Swap the roles of the clients
            temp = waitingSock
            waitingSock = playingSock
            playingSock = temp
            symbol = symbol * (-1)


    def shutdown(self):
        self.sockP1.close()
        self.sockP2.close()
        self.acceptSock.close()

ser = Server()
ser.acceptConnections()
ser.run()
ser.shutdown()