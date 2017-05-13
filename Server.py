import select
import socket
import sys
from Functionality import Functions, Room, Player
import Functionality


host = sys.argv[1]
listen_sock = Functionality.create_socket((host, 5001))

functions = Functions()
connection_list = []
connection_list.append(listen_sock)

while True:
    # Player.fileno()
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock:
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            functions.welcome_new(new_player)

        else:
            msg = player.socket.recv(4096)
            if msg:
                msg = msg.decode().lower()
                functions.handle_msg(player, msg)

            else:
                player.socket.close()
                connection_list.remove(player)
                print 'Client ' + str(player.name) + '  is disconnected'



    for sock in error_sockets:
        sock.close()
        connection_list.remove(sock)