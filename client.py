import socket
import util

class Client:
    def __init__(self):
        # Game representation
        """
             0 -> empty
             1 -> O
            -1 -> X
        """
        self.table = [[0,0,0], [0,0,0], [0,0,0]]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Get server ip and port from the user
        self.serverIP, self.serverPORT = util.getIP_PORT()
        # Try to connect to the server
        try:
            self.sock.connect((self.serverIP, self.serverPORT))
            print("[CONNECTED TO SERVER]")
        except:
            print("[COULDN'T CONNECT TO THE SERVER]")
            exit()

        # Get code to know if we have to wait for the other player
        code = util.recvCode(self.sock)
        # First player to connect get 'O'
        self.symbol = -1
        if code == util.WAIT_OPPONENT_CONNECTION:
            print("[WAITING FOR OTHER PLAYER TO CONNECT]")
            self.symbol = 1
            # Second player connected
            code = util.recvCode(self.sock)

    def run(self):
        while True:
            util.clear_screen()
            util.print_table(self.table)

            code = util.recvCode(self.sock)
            # My turn
            if code == util.PLAY:
                # Get play from user
                while True:
                    move = util.getMove()
                    if move[0] > 2 or move[1] > 2 or move[0] < 0 or move[1] < 0:
                        print("[PICK A VALID POSITION]")
                        continue
                    if self.table[move[0]][move[1]] != 0:
                        print("[POSITION TAKEN]")
                        continue
                    # Legal move, exit loop
                    break

                # Update the game state
                self.table[move[0]][move[1]] = self.symbol
                # Send to the server the play
                util.sendMove(self.sock, move)
            # Opponent's turn
            elif code == util.WAIT:
                print("[OPPONET'S TURN...]")
                # Get opponent's play
                move = util.recvMove(self.sock)
                # Update game state
                self.table[move[0]][move[1]] = self.symbol * (-1)
            elif code == util.WON:
                print("YOU WON!!!")
                break
            elif code == util.LOST:
                print("YOU LOST :(")
                break
            elif code == util.TIE:
                print("IT'S A TIE!")
                break
            

    def shutdown(self):
        self.sock.close()
        print("[EXITING...]")

c = Client()
c.run()
c.shutdown()
