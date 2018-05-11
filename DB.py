#!/usr/bin/python3         
import pymysql

# Simple routine to run a query on a database and print the results:
def doQuery( conn, mail_from, rcpt_to, data ) :
	rcpt = ""
	for i in range(len(rcpt_to)):
		rcpt += "<{}>,".format(rcpt_to[i])
	try:	
		subject, content = data.split("\n", maxsplit=1)
		_, subject = subject.split(":")
	except:
		subject, content = "empty", data
		
	cur = conn.cursor()
	q = "INSERT  INTO mails(from_, to_, subject, content, status, type, mark) values(\"{}\", \"{}\", \"{}\", \"{}\",0,0,0 );".format(mail_from, rcpt, subject.strip(), content.rstrip())
	try:
		cur.execute(q)
		conn.commit()
		#for from_ in cur.fetchall() :
        #	print (from_)
	except:
		print("FATAL: Error inserting into database")

def saveToDB(mail_from, rcpt_to, data):
	hostname = 'localhost'
	username = 'alvaro'
	password = 'toor'
	database = 'proyecto1'

	print ("Using pymysql…")
	myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
	doQuery( myConnection, mail_from, rcpt_to, data )
	myConnection.close()