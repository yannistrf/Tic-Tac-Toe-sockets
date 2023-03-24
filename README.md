# Online Tic-Tac-Toe using python sockets

### Description
Client-Server model over TCP connection
The server accepts incoming connections, then listens for each players's
move and informs his opponent up until someone loses. In that case the connection
is terminated properly.
Each client tries to connect to the server, then they send to the server their
selected play each time and wait for their opponent's move.
Basically the two clients communicate with each other with the server being the middle-man.

### Run
To run localy we will need three terminals.
In the first terminal we execute server.py where we will get a prompt asking for a listening port.
Type whatever port you don't currently run a service on (> 1024).

In the other two terminals we run client.py. When asking for the server's ip we provide localhost or
127.0.0.1 and then the port that the server is listening to.

After both of the clients are connected the game begins.

Of course the game can be run on different computers on different networks with the proper network
configurations. However, it's not recommended since security issues may occur (exposure to the whole internet)

### util.py
Just a python file with functions and constants that is used from both the server and the clients.
When executing the scripts make sure that util.py is in the same directory.
