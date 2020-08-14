#!/usr/bin/env python
# coding: utf-8

import socket
from AESLibrary import AESLibrary

HOST = "localhost"
PORT = 19876
aes=AESLibrary('mysecretpassword')

#Open a connection with the server
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
print ("Connection on {}:{}".format(HOST,PORT))

#Get msg, encrypt it with AES and hash it with SHA2
msg=input('type your message: ')

while(msg!='quit'):
    encrypted=aes.encrypt(msg)
    hash=aes.SHA2(msg)

    #Format and send the text to the server
    text=(encrypted.decode('utf-8')+'@'+hash).encode('utf-8')
    socket.send(text)

    #Get the response from the server
    server=socket.recv(255)
    print(server.decode('utf-8'))
    msg=input('Type your message: ')

#Connection closed
print ("Close")
socket.close()
