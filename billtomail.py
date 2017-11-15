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

oggi=time.strftime('%Y%m%d')#data di oggi
arrivo=oggi
partenza=oggi

jar = 'C:\IBM\jdbcmysql.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
con1=jaydebeapi.connect('com.mysql.jdbc.Driver', 'jdbc:mysql://localhost:3306/billtomail',['billtomail','billtomail']) #connessione al db2
cursm=con1.cursor()
cursm.execute("SELECT * FROM date")
#cursm.fetchall()

jar = 'C:\IBM\db2jcc4.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)

conn=jaydebeapi.connect('com.ibm.db2.jcc.DB2Driver', 'jdbc:db2://10.1.12.71:50000/s71mk0pu',['db2inst1','db2inst1']) #connessione al db2

curs=conn.cursor()

#query="SELECT * FROM DIGI.TABUTE_FG003 WHERE data_fattura>='"+partenza+"' AND data_fattura<'"+arrivo+"'"
#curs.execute("SELECT * FROM TABUTE_FG003 WHERE data_fattura>=''")
curs.execute("SELECT DG_INDIRIZZO_EMAIL,FATT_MAIL FROM DIGI.AZ_FRANCO WHERE MK_TIPO_CONTROPART='CLIENT' AND MK_UNITA_ORGANIZ='CNTFOR' AND FATT_MAIL!='0'")
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
