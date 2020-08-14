# -*- coding: utf-8 -*-
    # chat_server.py

import select
import socket
import sys
import threading
import time

from AESCypher import AESCypher, SHA256
from __builtin__ import raw_input


class Server():

    def __init__(self,app,filename):
        self.available = []
        self.app=app
        #filename='logs.log'
        self.HOST = ''
        self.SOCKET_LIST = []
        self.RECV_BUFFER = 4096
        self.PORT = 9009
        self.AES = AESCypher('mysecretpassword')
        self.SHA256 = SHA256()
        self.logfile = open(filename, 'a', buffering=0)
        self.logfile.write(time.strftime("%c")+" # Starting server ...\n")
        self.app.addlog(time.strftime("%c") + " # Starting server ...\n")

        threading.Thread(target=self.chat_server).start()


    def chat_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen(10)

        self.SOCKET_LIST.append(server_socket)

        print("Chat server started on port " + str(self.PORT))
        self.logfile.write(time.strftime("%c") + " # Chat server started on port " + str(self.PORT))
        self.app.addlog(time.strftime("%c") + " # Chat server started on port " + str(self.PORT))
        while 1:

            ready_to_read, ready_to_write, in_error = select.select(self.SOCKET_LIST, [], [], 0)

            for sock in ready_to_read:
                # a new connection request recieved
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    self.send_List_Connections(sockfd)
                    self.SOCKET_LIST.append(sockfd)
                    print("Client (%s, %s) connected" % addr)
                    self.logfile.write(time.strftime("%c")+" # Client (%s, %s) connected\n" % addr)
                    self.app.addlog(time.strftime("%c")+" # Client (%s, %s) connected\n" % addr)

                    self.available.append(addr)
                    self.app.setChatlist(self.available)
                    self.broadcast(server_socket, sockfd, "*@#[%s:%s] entered our chatting room\n" % addr)

                # a message from a client, not a new connection
                else:
                    # process data = AES + SHA256
                    try:

                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            # print(data)
                            response = data.split('@')

                            # # Decrypt the text
                            message = self.AES.decrypt(response[0])
                            #hash de deceypted text
                            hash = self.SHA256.hash(message)
                            #hash=self.SHA256.hash('c2d0c09b9d98ac647361b7411bb2a12d846c9f4e5ce14dc48579ae06584b3c5a')
                            # print(hash)

                            if (hash == response[1]):
                                message = message+' (V)'
                            else:
                                message = message+' (X)'


                            self.broadcast(server_socket, sock,'[' + str(sock.getpeername()) + '] ' + message)
                            self.logfile.write(time.strftime("%c")+" # "+data)
                            self.app.addlog(time.strftime("%c")+" # "+data)
                            self.app.addlog(time.strftime("%c") + " # " + message)
                        else:

                            if sock in self.SOCKET_LIST:
                                self.SOCKET_LIST.remove(sock)

                            # at this stage, no data means probably the connection has been broken
                                self.broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                            self.logfile.write(time.strftime("%c")+" # "+"Client (%s, %s) is offline\n" % addr)
                            self.app.addlog(time.strftime("%c")+" # "+"Client (%s, %s) is offline\n" % addr)

                            # exception
                    except Exception as err:
                        self.broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                        print("Unexpected error:", err)
                        continue

        server_socket.close()


    # send message to all connected clients
    def broadcast(self, server_socket, sock, message):
        for socket in self.SOCKET_LIST:

            if socket != server_socket and socket != sock:
                try:
                    socket.send(message)
                except:

                    socket.close()

                    if socket in self.SOCKET_LIST:
                        self.SOCKET_LIST.remove(socket)

    def send_List_Connections(self,sockfd):
        s='*@#['
        for soc in self.SOCKET_LIST[1:]:
            s=s+str(soc.getsockname())+" - "
        sockfd.send(s+'] are now connected!')


if __name__ == "__main__":
    filename = raw_input('Enter the file name where you want to save log otherwise enter "NO"')
    sys.exit(Server(filename).chat_server())