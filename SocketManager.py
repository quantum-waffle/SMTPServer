#!/usr/bin/python3         
import socket

def createConnection(host, port):
	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind((host, port))
		serversocket.listen(5) # queue up to 5 requests
		print("Listening on {}:{} ...".format(host, port))
		clientsocket, addr = serversocket.accept() # establish a connection
	except:
		print("Error in socket creation")
		clientsocket, addr = 0, 0
	return clientsocket, addr

def send(clientsocket, mssg):
	msg = mssg + "\r\n"
	clientsocket.send(msg.encode('ascii')) #send

def receive(clientsocket, rstrip=True, size=1024):
	if rstrip: return clientsocket.recv(size).decode('ascii').rstrip() #receive
	return clientsocket.recv(size).decode('ascii')