#!/usr/bin/python3         
import time, SMTPProtocol as smtp, SocketManager as sm                                    

server_ip, server_port, owner = "0.0.0.0", 6666, "alvaro"
dominio = [["eddy", "10.8.0.10", 25],\
		   ["michelle", "10.8.0.x", 25],\
		   ["mauricio", "10.8.0.x", 25],\
		   ["esmeralda", "10.8.0.9", 25]]

def main():
	print("SMTP Server is up!")
	tries, socket_created = 0, False
	while(tries < 3):
		while not socket_created:
			try:
				print("Creating connection...")
				clientsocket, addr = sm.createConnection(server_ip, server_port)
			except:
				print("Exception creating socket connection, retrying in 10 seconds...")
				time.sleep(10)
			else:
				if(clientsocket==0):
					print("Cannot create socket connection, retrying in 10 seconds...")
					time.sleep(10)
				else:
					socket_created = True
		try:
			mail_from, rcpt_to, data = smtp.receiveMail(clientsocket, addr)
		except:
			print("FATAL: Error reading SMTP protocol")
			clientsocket.close()
			tries += 1
		else:
			socket_created = False
			smtp.processMail(mail_from, rcpt_to, data, dominio, owner.upper())
			print("Everytings done!\n")
			time.sleep(1)
	print("Max number of tries reached, disconnecting...")

main()