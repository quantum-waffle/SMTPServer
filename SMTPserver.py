#!/usr/bin/python3         
import socket                                         

server_ip, server_port = "0.0.0.0", 666

dominio = [["eddy", "10.8.0.10", 25],\
		   ["michelle", "10.8.0.x", 25],\
		   ["mauricio", "10.8.0.x", 25],\
		   ["esmeralda", "10.8.0.9", 25]]

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

def run(clientsocket, addr):
	mail_from, rcpt_to, data, flag = "", [], "", True
	print("Got a connection from %s" % str(addr))
	while flag:		 
		send(clientsocket, "220 smtp.alvaro.com") 
		val_1 = receive(clientsocket).upper()
		print(val_1)
		if("HELO" in val_1):
			send(clientsocket, "250 Hello, greetings traveler")
			val_1, val_2 = receive(clientsocket).upper().split(":")
			print(val_1, val_2)
			if("MAIL FROM" in val_1):
				mail_from = val_2
				send(clientsocket, "250 Ok")
				val_1, val_2 = receive(clientsocket).upper().split(":")
				print(val_1, val_2)
				while("RCPT TO" in val_1):
					rcpt_to.append(val_2) 
					send(clientsocket, "250 Ok")
					aux = receive(clientsocket).upper()
					print(aux)
					if("DATA" in aux):
						val_1, val_2 = "DATA", ""
					else:
						val_1, val_2 = aux.upper().split(":")
				if(val_1 == "DATA"):
					send(clientsocket, "354 End data with <CR><LF>.<CR><LF>")
					receiving_data = True
					while receiving_data:
						aux = receive(clientsocket, rstrip=False)
						if(".\r\n" in aux):
							data += aux
							receiving_data = False
						else:
							data += aux
					send(clientsocket, "250 Ok: queued as {}".format("x"))
					print(mail_from, rcpt_to, data)
					clientsocket.close()
					return mail_from, rcpt_to, data
					flag = False
				else:
					print("ERROR EN RCPT TO")
					flag = False
			else:
				print("Error en MAIL FROM")
				flag = False
		else:
			print("Error en HELO")
			flag = False

	clientsocket.close()


def redirectMail(clientsocket, mail_from, rcpt_to, data, owner):
	val_1 = receive(clientsocket)
	print(val_1)
	if("220" in val_1):
		send(clientsocket, "HELO alvaro")
		val_1 = receive(clientsocket)
		if("250" in val_1):
			send(clientsocket, "MAIL FROM: <{}>".format(mail_from))
			val_1 = receive(clientsocket)
			print(val_1)
			if("250" in val_1):
				for i in range(len(rcpt_to)):
					if(owner not in rcpt_to[i]):
						send(clientsocket, "RCPT TO: <{}>".format(rcpt_to[i]))
						val_1 = receive(clientsocket)
						print(val_1)
				send(clientsocket, "DATA")
				val_1 = receive(clientsocket)
				print(val_1)
				if("354" in val_1):
					send(clientsocket, data)
					send(clientsocket, ".")
					val_1 = receive(clientsocket)
					print(val_1)
					if("250" in val_1):
						print("DONE!")
				else:
					print("Error in sending data")
			else:
				print("Error in mail from")
		else:
			print("Error in helo")
	else:
		print("Error stablishing connection")


def processMail(mail_from, rcpt_to, data, domain, owner):
	for i in range(len(rcpt_to)):
		user, dom = rcpt_to[i].upper().split("@")
		print("received for: {}".format(dom))
		if("ALVARO" in dom): #this email is for u :)
			print("NEW MAIL! :\n", data)
		elif (domain[i][0].upper() in dom):
			print("Redirecting mail to: {}".format(dom))
			clientsocket, addr = createConnection(domain[i][1], domain[i][2])
			redirectMail(clientsocket, mail_from, rcpt_to, data, owner)
			print("MAIL REDIRECTED TO {}, domain {}, port {}".format(rcpt_to[i], domain[i][1], domain[i][2]))
		else:
			print("Nothing to do with incoming mail. Destroying it...")

def main():
	print("SMTP Server is up!")
	tries = 0
	while(tries < 3):
		clientsocket, addr = createConnection(server_ip, server_port)
		try:
			mail_from, rcpt_to, data = run(clientsocket, addr)
		except:
			print("FATAL: Error reading SMTP protocol")
			clientsocket.close()
			tries += 1
		else:
			processMail(mail_from, rcpt_to, data, dominio, "ALVAR0")
	print("Max number of tries reached, disconnecting...")
main()