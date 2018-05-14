#!/usr/bin/python3         
import time, SMTPProtocol as smtp, SocketManager as sm, syslog as sy    

sy.openlog("smtp_server", logoption=sy.LOG_PID)                    

server_ip, server_port, owner = "0.0.0.0", 25, "alvaro"
dominio = [["eddy", "192.168.1.10", 25],\
		   ["michelle", "10.8.0.x", 25],\
		   ["yo", "127.0.0.1", 2525],\
		   ["mauricio", "10.8.0.x", 25],\
		   ["esmeralda", "10.8.0.9", 25]]

def main():
	sy.syslog(sy.LOG_INFO, 'INFO: Server SMTP is up.')
	print("SMTP Server is up!")
	tries, socket_created = 0, False
	while(tries < 3):
		while not socket_created:
			try:
				sy.syslog(sy.LOG_INFO, 'INFO: Creating socket connection.')
				print("Creating connection...")
				clientsocket, addr = sm.createConnection(server_ip, server_port)
			except:
				sy.syslog(sy.LOG_ERR, 'ERROR: Exception creating socket connection, retrying in 10 seconds...')
				print("Exception creating socket connection, retrying in 10 seconds...")
				time.sleep(10)
			else:
				if(clientsocket==0):
					sy.syslog(sy.LOG_ERR, 'ERROR: Cannot create socket connection, retrying in 10 seconds....')
					print("Cannot create socket connection, retrying in 10 seconds...")
					time.sleep(10)
				else:
					socket_created = True
		try:
			mail_from, rcpt_to, data = smtp.receiveMail(clientsocket, addr)
		except:
			sy.syslog(sy.LOG_ERR, 'ERROR: Error reading SMTP protocol.')
			print("FATAL: Error reading SMTP protocol")
			clientsocket.close()
			socket_created = False
			tries += 1
		else:
			socket_created = False
			smtp.processMail(mail_from, rcpt_to, data, dominio, owner.upper())
			sy.syslog(sy.LOG_INFO, 'INFO: Everyting done with mail received.')
			print("Everytings done!\n")
			time.sleep(1)
	sy.syslog(sy.LOG_ERR, 'ERROR: Max number of tries reached, server shuting down.')
	print("Max number of tries reached, disconnecting...")

main()