#!/usr/bin/env python
# coding: utf-8

import socket
from AESLibrary import AESLibrary
import threading

PORT=19876
aes=AESLibrary('mysecretpassword')

def AesDecrypt(encryptedText):
	return aes.decrypt(encryptedText)


class ClientThread(threading.Thread):
	def __init__(self, ip, port, clientsocket):
		threading.Thread.__init__(self)
		self.address = ip
		self.port = port
		self.client = clientsocket

	def run(self):
		# Recieve message from the client in this format : cryptedMsg@hash
		response = client.recv(255)

		while	response != "":

			text = response.decode('utf-8').split('@')

			# Decrypt the text
			message = AesDecrypt(text[0].encode('utf-8'))

			# Hash the message
			hash = aes.SHA2(message)
			print(message)

			# Verify that the hash of this msg is = to the one sent by the client
			if (hash == text[1]):
				#print("The integrity of the message is verified!")
				print('(The integrity of this msg is vérified!)')

			# reply to the client
			reply = input("Type your response: ")
			client.send(reply.encode('utf-8'))
			response = client.recv(255)






print('Listening on port '+str(PORT))
#Listening ...
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', PORT))

while True:
	socket.listen(5)
	# Client is connected to the server
	(client, (address, port)) = socket.accept()
	print ("{} connected".format( address ))

	#Démarrer un thread pour gérer ce client
	newthread = ClientThread(address, port, client)
	newthread.start()



#Server Down
print ("Close")
client.close()
stock.close()

