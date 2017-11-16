import jaydebeapi
import jpype

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
counterror=0
fromaddr = "f.avino@melchioni.it"
user = "f.avino@melchionispa"
password = "Fiwoldiois01"

oggi=time.strftime('%Y-%m-%d')#data di oggi
arrivo=oggi
##########################################################################################################################################
##########################################################################################################################################
##############################################CONNESSIONE DBs#############################################################################
#CONNESSIONE A MYSQL
jar = 'C:\IBM\jdbcmysql.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
con1=jaydebeapi.connect('com.mysql.jdbc.Driver', 'jdbc:mysql://localhost:3306/billtomail',['billtomail','billtomail']) #connessione al db2
cursm=con1.cursor()
########FINE MYSQL

#CONNESSIONE A DB2
jar = 'C:\IBM\db2jcc4.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
conn=jaydebeapi.connect('com.ibm.db2.jcc.DB2Driver', 'jdbc:db2://10.1.12.71:50000/s71mk0pu',['db2inst1','db2inst1']) #connessione al db2
curs=conn.cursor()
#########FINE DB2


#NB: 	curs=cursore DB2 su conn Db2
#		cursm=cursore mysql su con1 mysql
#########################################################FINE CONNESSIONI A DBs###########################################################
##########################################################################################################################################
##########################################################################################################################################



#SOSTITUTO DEL FILE BANDIERA, FARE PAGINA WEB PER MODIFICHE
cursm.execute("SELECT * FROM bandiera")
datas=cursm.fetchall()
data=data[0] #seleziono riga 0
inizio_bandiera=data[0] #seleziono i campi
fine_bandiera=data[1] #seleziono i campi
forzata=data[2] #seleziono i campi
###############################################################FINE BANDIERA

inizio=inizio_bandiera#LA DATA DI INIZIO è COMUNQUE DETTATA DALLA BANDIERA, FORZATA O MENO
if forzata!=0:
	fine=fine_bandiera
	print ("!!!!!!!!!!!!!!!!!!!!!!!!!DATA FORZATA DA UTENTE!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	
print ("DATA INIZIO: " + inizio + "\n")
print ("DATA FINE: " + fine + "\n")

cursm.execute("TRUNCATE TABLE bandiera") #da inserire alla fine????


#query="SELECT * FROM DIGI.TABUTE_FG003 WHERE data_fattura>='"+partenza+"' AND data_fattura<'"+arrivo+"'"
#curs.execute("SELECT * FROM TABUTE_FG003 WHERE data_fattura>=''")
query="SELECT * FROM DIGI.TABUTE_FG0003 LEFT OUTER JOIN DIGI.AZ_FRANCO ON (DIGI.TABUTE_FG0003.MK_CLIENTE = DIGI.AZ_FRANCO.MK_CONTROPARTE) WHERE DIGI.AZ_FRANCO.DG_INDIRIZZO_EMAIL IS NOT NULL AND DIGI.AZ_FRANCO.FATT_MAIL!='0' AND DIGI.TABUTE_FG0003.MK_DATAFA>='2002-01-30' and DIGI.TABUTE_FG0003.MK_DATAFA<'2017-10-31'"
curs.execute(query)
rows = curs.fetchall()
for row in rows:
	print(row) #SELEZIONO LA RIGA COME ARRAY
	toaddr=row[0] #SELEZIONO IL CAMPO DG_INDIRIZZO_EMAIL
	
	
#####################################################INIZIO INVIO MAIL!#################	
	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "SUBJECT OF THE EMAIL"
	
	body = "TEXT YOU WANT TO SEND"
	
	msg.attach(MIMEText(body, 'plain'))
	
	filename = "prova.docx"
	errore=0
	try:
		attachment = open(filename, "rb")
	except IOError:
		print ("File open failed!")
		errore=1
		counterror=counterror+1
	
	if errore==0:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		
		msg.attach(part)
		
		server = smtplib.SMTP('owa.melchioni.it', 25)
		server.starttls()
		server.login(user, password)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
	else:
		print ("non sarà inviata la mail")
		print (counterror)
#####################################################FINE INVIO MAIL!#################		
		
	
curs.close()
conn.close()
