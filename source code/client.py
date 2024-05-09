import socket
import threading
import sys

import Interface_functions
def create_sock():
    try:
        global check
        check=False
        global host
        global port
        global client
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as msg:
        print('a socket was not created', str(msg))
        
create_sock()
try:
    client.connect(('127.0.0.1',9999))
    print("connection established")
    
except socket.error as msg:
    print("connection didn't go well;",str(msg))
    sys.exit(1)
    #check=Truek
    
Interface_functions.signup(client)

