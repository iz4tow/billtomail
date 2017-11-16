import pyodbc
import jaydebeapi
import jpype

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
counterror=0
countok=0
contatore=0
fromaddr = "inviofatture@melchioni.it"
user = "inviofatture@melchionispa"
password = "invio123"

oggi=time.strftime('%Y%m%d')#data di oggi
fine=oggi

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

#CONNESSIONE A SYBASE IQ
cnxn = pyodbc.connect("DSN=melc6h1_dmcomm")
cursiq = cnxn.cursor()
########FINE MYSQL
#NB: 	cursiq=cursore SYBASE IQ su cnxn SYBASE IQ
#		cursm=cursore mysql su con1 mysql
#########################################################FINE CONNESSIONI A DBs###########################################################
##########################################################################################################################################
##########################################################################################################################################

#SOSTITUTO DEL FILE BANDIERA, FARE PAGINA WEB PER MODIFICHE
cursm.execute("SELECT * FROM bandiera")
datas=cursm.fetchall()
data=datas[0] #seleziono riga 0
idbandiera=str(data[0])#seleziono i campi convertendoli in stringa
inizio_bandiera=data[1] #seleziono i campi
fine_bandiera=data[2] #seleziono i campi
forzata=data[3] #seleziono i campi
esecuzione=data[4] #seleziono i campi
###############################################################FINE BANDIERA
cursm.execute("UPDATE bandiera SET esecuzione='1' WHERE id='"+idbandiera+"'")


inizio=inizio_bandiera#LA DATA DI INIZIO è COMUNQUE DETTATA DALLA BANDIERA, FORZATA O MENO
if forzata!=0:
	fine=fine_bandiera
	print ("!!!!!!!!!!!!!!!!!!!!!!!!!DATA FORZATA DA UTENTE!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	

if esecuzione!=0:
	print ("!!!!!!!!!!!!!!!!!!!!!!!!!REINIZIO DA DOVE MI ERO INTERROTTO SALTANDO L'IMPORTAZIONE!!!!!!!!!!!!!!!!!!!!!!!!!")
	print ("!!!!!!!!!!!!!!!!!!!!!!!!!DATA FORZATA DA ERRORE PRECEDENTE ESECUZIONE!!!!!!!!!!!!!!!!!!!!!!!!!\n")
	fine=fine_bandiera

print ("DATA INIZIO: " + inizio + "\n")
print ("DATA FINE: " + fine + "\n")
	
if esecuzione==0: #SOLO SE L'esecuzione precedente è terminata correttamente reimporto i dati da sybase iq altrimenti torno sulla tabella degli invii a completare l'opera
	##SELEZIONO LE FATTURE DA INVIARE SU SYBASE IQ
	#sql = "SELECT distinct substr(dba.artfatt3.f_cliente,1,8) as f_cliente, dba.artfatt3.cli_invio_doc, dba.artfatt3.numero_fattura, dba.artfatt3.data_fattura, dba.clienti_email.E_mail FROM dba.artfatt3 LEFT OUTER JOIN dba.clienti_email ON (dba.artfatt3.cli_invio_doc = dba.clienti_email.Codice_cliente) WHERE dba.clienti_email.E_mail is not null and dba.artfatt3.data_fattura>='"+inizio+"' and dba.artfatt3.data_fattura<'"+fine+"'"
	#cursiq.execute(sql)
	#fatture = cursiq.fetchall()
	##MI SALVO I CAMPI ESTRATTI DA SYBASE IQ SU MYSQL DI COMODO
	#for fattura in fatture:  
	#	cliente=fattura[0]
	#	cliente_invio=fattura[1]
	#	numfatt=fattura[2]
	#	datafatt=fattura[3]
	#	mail=fattura[4]
	#	datafatt=str(datafatt) #rendo il campo datetime una stringa
	#	anno=datafatt[:4]#substring per ottenere l'anno  (caratteri 1 a 4)
	#	#INSERISCO I DATI LETTI SU MYSQL NELLA TABELLA DI COMODO INVIO
	#	cursm.execute("INSERT INTO invio (fattura,data,anno,cod_cliente,cod_cliente_invio,mail) VALUES ('"+numfatt+"','"+datafatt+"','"+anno+"','"+cliente+"','"+cliente_invio+"','"+mail+"')")
	#cursiq.close()#SYBASE IQ NON SERVE ORA
	print("IMPORTAZIONE RECORD DA SYBASE IQ TERMINATA")


	
#RILEGGO LA TABELLA DI COMODO PER COMINCIARE GLI INVII....
cursm.execute("SELECT * FROM invio")
fatture = cursm.fetchall()
for fattura in fatture:
	idinvio=str(fattura[0])
	numfattura=fattura[1]
	data=fattura[2]
	anno=fattura[3]
	cod_cliente=fattura[4]
	cod_cliente_invio=fattura[5]
	toaddr=fattura[6]
	annocorto=anno[2:4]#substring per ottenere l'anno di 2 cifre
	documento=numfattura+"_"+annocorto+".pdf"#nome documento
#################################################################################################INVIO MAIL
	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "INVIO FATTURE TELEMATICO MELCHIONI S.P.A."
	
	body = "In allegato la fattura in formato PDF"
	
	msg.attach(MIMEText(body, 'plain'))
	
	filename = "S:\\PDFATTURE\\"+anno+"\\"+documento
	errore=0
	try:
		attachment = open(filename, "rb")
	except IOError:
		errore=1
		counterror=counterror+1
	
	if errore==0:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read()) #CARICA l'ALLEGATO
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % documento)	#preparo l'allegato nell'header, la variabile documento è il nome
		msg.attach(part)#allego il file		
		server = smtplib.SMTP('owa.melchioni.it', 25)
		server.starttls()
		server.login(user, password)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
		countok=countok+1
		print ("\n\n\n\n\n\n ----------------------------------------MAIL INVIATA A " +toaddr)
		print ("CODICE CLIENTE: " + cod_cliente + "  CLIENTE INVIO:" + cod_cliente_invio)
		print ("FATTURA:" +documento+ " DEL " +data)
		cursm.execute("DELETE FROM invio WHERE id='"+idinvio+"'")#CANCELLO I RECORD SPEDITI CORRETTAMENTE
	else:
		print ("\n\n\n\n\n\n ----------------------------------------MAIL NON INVIATA A " +toaddr)
		print ("CODICE CLIENTE: " + cod_cliente + "  CLIENTE INVIO:" + cod_cliente_invio)
		print ("FATTURA MANCANTE:" +documento+ " DEL " +data+ " non trovata!")
	contatore=contatore+1
#################################################################################################FINE INVIO MAIL
#CONVERTO I CONTATORI A STRINGA PER POTERLI STAMPARE A VIDEO
countok=str(countok)
counterror=str(counterror)
contatore=str(contatore)
print ("\n\n\n\n\n\n\nTOTALE MAIL INVIATE: "+countok)
print ("TOTALE ERRORI: " +counterror)
print ("TOTALE: "+contatore)

if counterror=='0': #SE NON CI SONO STATI ERRORI
	cursm.execute("TRUNCATE TABLE invio")#svuoto la tabella degli invii su mysql
	cursm.execute("TRUNCATE TABLE bandiera") #svuoto la bandiera
	cursm.execute("INSERT INTO bandiera (inizio,fine,forzata,esecuzione) VALUES ('"+fine+"','0','0','0')")#CREO LA NUOVA BANDIERA CON DATA INIZIO= FINE DI OGGI e FORZATA=0 ed esecuzione a 0