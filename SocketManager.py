#!/usr/bin/python3         
import socket, time, syslog as sy    

sy.openlog("smtp_server", logoption=sy.LOG_PID)         

def createConnection(host, port):
	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind((host, port))
		serversocket.listen(5) # queue up to 5 requests
		sy.syslog(sy.LOG_INFO, "INFO: Listening on {}:{}.".format(host, port))
		print("Listening on {}:{} ...".format(host, port))
		clientsocket, addr = serversocket.accept() # establish a connection
	except:
		sy.syslog(sy.LOG_ERR, "ERROR: Error in socket creation to {}:{}.".format(host, port))
		print("Error in socket creation to {}:{}".format(host, port))
		clientsocket, addr = 0, 0
	return clientsocket, addr

def send(clientsocket, mssg):
	msg = mssg + "\r\n"
	clientsocket.send(msg.encode('ascii')) #send

def receive(clientsocket, rstrip=True, size=1024):
	if rstrip: return clientsocket.recv(size).decode('ascii').rstrip() #receive
	return clientsocket.recv(size).decode('ascii')

def ConnectTo(host, port, tries=3):
	while(tries>0):
		try:
			serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			serversocket.connect((host, port))
			sy.syslog(sy.LOG_INFO, "INFO: Connected to {}:{}!".format(host, port))
			print("Connected to {}:{}!".format(host, port))
			return serversocket
		except:
			sy.syslog(sy.LOG_ERR, "ERROR: Error connectiong to {}:{}.".format(host, port))
			print("Error connecting to {}:{}".format(host, port))
			tries = tries -1
			time.sleep(2)
	return 0