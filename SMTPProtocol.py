#!/usr/bin/python3         
import SocketManager as sm, DB as db, syslog as sy    

sy.openlog("smtp_server", logoption=sy.LOG_PID)  

def receiveMail(clientsocket, addr):
	mail_from, rcpt_to, data, flag = "", [], "", True
	sy.syslog(sy.LOG_INFO, "INFO: Got a connection from {}.".format(addr))
	print("Got a connection from %s" % str(addr))
	while flag:		 
		sm.send(clientsocket, "220 smtp.alvaro.com") 
		val_1 = sm.receive(clientsocket).upper()
		print(val_1)
		if("HELO" in val_1):
			sm.send(clientsocket, "250 Hello, greetings traveler")
			val_1, val_2 = sm.receive(clientsocket).upper().split(":")
			print(val_1, val_2)
			if("MAIL FROM" in val_1):
				mail_from = val_2
				sm.send(clientsocket, "250 Ok")
				val_1, val_2 = sm.receive(clientsocket).upper().split(":")
				print(val_1, val_2)
				while("RCPT TO" in val_1):
					rcpt_to.append(val_2) 
					sm.send(clientsocket, "250 Ok")
					aux = sm.receive(clientsocket).upper()
					print(aux)
					if("DATA" in aux):
						val_1, val_2 = "DATA", ""
					else:
						val_1, val_2 = aux.upper().split(":")
				if(val_1 == "DATA"):
					sm.send(clientsocket, "354 End data with <CR><LF>.<CR><LF>")
					receiving_data = True
					while receiving_data:
						aux = sm.receive(clientsocket, rstrip=False)
						if(".\r\n" in aux):
							data += aux
							receiving_data = False
						else:
							data += aux
					sm.send(clientsocket, "250 Ok: queued as {}".format("x"))
					sy.syslog(sy.LOG_INFO, "INFO: Mail processed succesfully for {}.".format(addr))
					print(mail_from, rcpt_to, data)
					clientsocket.close()
					return mail_from, rcpt_to, data
					flag = False
				else:
					sy.syslog(sy.LOG_ERR, "ERROR: Syntax error in  RCPT TO from {}.".format(addr))
					print("ERROR EN RCPT TO")
					flag = False
			else:
				sy.syslog(sy.LOG_ERR, "ERROR: Syntax error in  MAIL FROM from {}.".format(addr))
				print("Error en MAIL FROM")
				flag = False
		else:
			sy.syslog(sy.LOG_ERR, "ERROR: Syntax error in  HELO from {}.".format(addr))
			print("Error en HELO")
			flag = False

	clientsocket.close()


def redirectMail(clientsocket, mail_from, rcpt_to, data, owner):
	val_1 = sm.receive(clientsocket)
	print(val_1)
	if("220" in val_1):
		sm.send(clientsocket, "HELO alvaro")
		val_1 = sm.receive(clientsocket)
		if("250" in val_1):
			sm.send(clientsocket, "MAIL FROM: <{}>".format(mail_from))
			val_1 = sm.receive(clientsocket)
			print(val_1)
			if("250" in val_1):
				for i in range(len(rcpt_to)):
					if(owner not in rcpt_to[i]):
						sm.send(clientsocket, "RCPT TO: <{}>".format(rcpt_to[i]))
						val_1 = sm.receive(clientsocket)
						print(val_1)
				sm.send(clientsocket, "DATA")
				val_1 = sm.receive(clientsocket)
				print(val_1)
				if("354" in val_1):
					sm.send(clientsocket, data)
					sm.send(clientsocket, ".")
					val_1 = sm.receive(clientsocket)
					print(val_1)
					if("250" in val_1):
						sy.syslog(sy.LOG_INFO, "INFO: Done redirecting mail.")
						print("DONE!")
				else:
					sy.syslog(sy.LOG_ERR, "ERROR: Error sending data")
					print("Error in sending data")
			else:
				sy.syslog(sy.LOG_ERR, "ERROR: Error in mail from")
				print("Error in mail from")
		else:
			sy.syslog(sy.LOG_ERR, "ERROR: Error in helo")
			print("Error in helo")
	else:
		sy.syslog(sy.LOG_ERR, "ERROR: Error stablishing connection")
		print("Error stablishing connection")


def processMail(mail_from, rcpt_to, data, domain, owner):
	for i in range(len(rcpt_to)):
		try:
			user, dom = rcpt_to[i].upper().split("@")
		except:
			user, dom = "",""

		print("received for: {}".format(dom))
		if(owner in dom): #this email is for u :)
			sy.syslog(sy.LOG_INFO, "INFO: New mail received for {}.".format(owner))
			print("NEW MAIL! :\n", data)
			db.saveToDB(mail_from, rcpt_to, data)
		#elif (dom in domain[i][0].upper()):
		elif (len(domain)>0):
			for j in range(len(domain)):
				print("Checking for {}".format(domain[j][0]))
				if (domain[j][0].upper() in dom):
					sy.syslog(sy.LOG_INFO, "INFO: Redirecting mail to: {}".format(dom))
					print("Redirecting mail to: {}".format(dom))
					#clientsocket, addr = createConnection(domain[i][1], domain[i][2])
					clientsocket = sm.ConnectTo(domain[j][1], domain[j][2])
					if(clientsocket!=0):
						redirectMail(clientsocket, mail_from, rcpt_to, data, owner)
						clientsocket.close()
						sy.syslog(sy.LOG_INFO, "INFO: Mail redirected to {}, domain {}, port {}".format(rcpt_to[i], domain[j][1], domain[j][2]))
						print("MAIL REDIRECTED TO {}, domain {}, port {}".format(rcpt_to[i], domain[j][1], domain[j][2]))
					else:
						sy.syslog(sy.LOG_ERR, "ERROR: Could not redirect to {} at {}:{}".format(rcpt_to[i], domain[j][1], domain[j][2]))
						print("Could not redirect to {} at {}:{}".format(rcpt_to[i], domain[j][1], domain[j][2]))
		else:
			sy.syslog(sy.LOG_WARNING, "WARNING: Nothing to do with incoming mail, destroying it.")
			print("Nothing to do with incoming mail. Destroying it...")