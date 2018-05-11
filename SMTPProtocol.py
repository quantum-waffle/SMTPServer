#!/usr/bin/python3         
import SocketManager as sm, DB as db

def receiveMail(clientsocket, addr):
	mail_from, rcpt_to, data, flag = "", [], "", True
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
		try:
			user, dom = rcpt_to[i].upper().split("@")
		except:
			user, dom = "",""

		print("received for: {}".format(dom))
		if(owner in dom): #this email is for u :)
			print("NEW MAIL! :\n", data)
			db.saveToDB(mail_from, rcpt_to, data)
		#elif (dom in domain[i][0].upper()):
		elif (dom == "EDDY"):
			print("Redirecting mail to: {}".format(dom))
			#clientsocket, addr = createConnection(domain[i][1], domain[i][2])
			clientsocket, addr = createConnection("192.168.1.10", 25)
			redirectMail(clientsocket, mail_from, rcpt_to, data, owner)
			print("MAIL REDIRECTED TO {}, domain {}, port {}".format(rcpt_to[i], domain[i][1], domain[i][2]))
		else:
			print("Nothing to do with incoming mail. Destroying it...")