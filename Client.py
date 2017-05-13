import select
import socket
import sys
import Functionality

if len(sys.argv) < 2:
    print("Please provide Host!")
    sys.exit(1)
else:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.connect((sys.argv[1], 5001))

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection:
            msg = s.recv(4096)
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                if msg == Functionality.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())
                    if 'Please tell us your name' in msg.decode():
                        msg_prefix = 'username: '
                    else:
                        msg_prefix = ''
        else:
            msg = msg_prefix + sys.stdin.readline()
            server_connection.sendall(msg.encode())