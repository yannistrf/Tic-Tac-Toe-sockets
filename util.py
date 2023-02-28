# Print the game table to the terminal
def print_table(table):
    for row in range(0, 3):
        print("-------------")
        for col in range(0, 3):
            if table[row][col] == 1:
                symbol = "O"
            elif table[row][col] == -1:
                symbol = "X"
            else:
                symbol = " "

            print(f"| {symbol} ", end="")

            if col == 2:
                print("|")   
    print("-------------")

from os import system, name

def clear_screen():

    if name == "nt":
        system("cls")
    elif name == "posix":
        system("clear")


'''
(These are only for the server)

STATUS CODES
 1 -> player 1 won
-1 -> player 2 won
 0 -> nothing
 2 -> tie
'''

def check_status(table):
    # Check horizontal
    for row in range(0,3):
        if table[row][0] != 0 and table[row][0] == table[row][1] and table[row][1] == table[row][2]:
            return table[row][0]

    # Check columns
    for col in range(0, 3):
        if table[0][col] != 0 and table[0][col] == table[1][col] and table[1][col] == table[2][col]:
            return table[0][col]

    # Check diagonals
    if table[0][0] != 0 and table[0][0] == table[1][1] and table[1][1] == table[2][2]:
        return table[0][0]
    if table[0][2] != 0 and table[0][2] == table[1][1] and table[1][1] == table[2][0]:
        return table[0][2]
    
    # Check for tie
    found_0 = False
    for row in range(0, 3):
        for col in range(0, 3):
            if table[row][col] == 0:
                found_0 = True
    if not found_0:
        return 2

    return 0

def getIP_PORT():
    ip = input("Enter server's IP address: ")
    port = int(input("Enter the port the server is listening to: "))

    return ip, port

def getMove():
    # Make sure the user gives us an integer
    while True:
        try:
            row = int(input("Enter row: ")) - 1
            col = int(input("Enter column: ")) - 1
            break
        except ValueError:
            print("[PLEASE ENTER A NUMBER]")
    return row, col

# Message size
HEADER = 3
""" These are the codes the server sents to the clients """
WAIT_OPPONENT_CONNECTION = 101
GAME_BEGINS = 100
PLAY = 201
WAIT = 202
WON = 999
LOST = 666
TIE = 777

# Used only from the server
# Sends code to client
def sendCode(sock, code):
    sock.send(str(code).encode())

# Used only from the client
# Receives code from server
def recvCode(sock):
    data = sock.recv(HEADER)
    code = int(data.decode())
    return code

# Used both from client and server
def sendMove(sock, move):
    msg = str(move[0]) + " " + str(move[1])
    sock.send(msg.encode())

# Used both from client and server
def recvMove(sock):
    msg = sock.recv(HEADER).decode()
    move = (int(msg[0]), int(msg[2]))
    return move
