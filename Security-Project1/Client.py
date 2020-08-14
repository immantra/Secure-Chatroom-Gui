# chat_client.py

import select
import socket
import sys
import threading

from AESCypher import AESCypher, SHA256


class client:

    def __init__(self, app):
        self.app=app

        if (len(sys.argv) < 4):
            print('Usage : python Client_UI.py hostname port username')
            sys.exit()

        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        self.AES = AESCypher('mysecretpassword')
        self.SAH256 = SHA256()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        # connect to server
        try:
            self.s.connect((self.host, self.port))
        except:
            self.app.insert_message('             Unable to connect')
            sys.exit()
        self.app.insert_message('Connected to remote host. You can start sending messages')
        sys.stdout.flush()

        threading.Thread(target=self.recv).start()


    def recv(self):
        # self.app.insert_message('test!!')
        while 1:
            socket_list = [sys.stdin, self.s]

            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

            for sock in ready_to_read:
                if sock == self.s:
                    data = sock.recv(4096)
                    if not data:
                        self.app.insert_message('Disconnected from chat server')
                        sys.exit()
                    else:
                        #'*#@' means that there is a new connected client
                        if(data[0]=='*' and data[1]=='@' and data[2]=='#'):
                            self.app.insert_message(data.split('#')[1])
                            member = data.split('[')[1].split(']')[0]
                            self.app.newConnection(member)
                            print('new member = '+member)
                        else:
                            self.app.insert_message(data)
                        print(data)

    def send(self,msg):

        cypher= self.AES.encrypt(msg)
        hash = self.SAH256.hash(msg)
        toSend=cypher+'@'+hash
        self.s.send(toSend)

