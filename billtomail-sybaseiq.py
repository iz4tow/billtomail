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
fromaddr = "f.avino@melchioni.it"
user = "f.avino@melchionispa"
password = "Fiwoldiois01"

oggi=time.strftime('%Y%m%d')#data di oggi
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


#SELEZIONO LE FATTURE DA INVIARE SU SYBASE IQ
sql = "SELECT distinct substr(dba.artfatt3.f_cliente,1,8) as f_cliente, dba.artfatt3.cli_invio_doc, dba.artfatt3.numero_fattura, dba.artfatt3.data_fattura, dba.clienti_email.E_mail FROM dba.artfatt3 LEFT OUTER JOIN dba.clienti_email ON (dba.artfatt3.cli_invio_doc = dba.clienti_email.Codice_cliente) WHERE dba.clienti_email.E_mail is not null and dba.artfatt3.data_fattura>='"+inizio+"' and dba.artfatt3.data_fattura<'"+fine+"'"
cursiq.execute(sql)
fatture = cursiq.fetchall()
#MI SALVO I CAMPI ESTRATTI DA SYBASE IQ SU MYSQL DI COMODO
cursm.execute("TRUNCATE TABLE invio")#svuoto la tabella degli invii su mysql
for fattura in fatture:  
	cliente=fattura[0]
	cliente_invio=fattura[1]
	numfatt=fattura[2]
	datafatt=fattura[3]
	mail=fattura[4]
	datafatt=str(datafatt) #rendo il campo datetime una stringa
	annocorto=datafatt[2:4]#substring per ottenere l'anno corto (caratteri 3 e 4)
	#INSERISCO I DATI LETTI SU MYSQL NELLA TABELLA DI COMODO INVIO
	cursm.execute("INSERT INTO invio (fattura,data,anno,cod_cliente,cod_cliente_invio,mail) VALUES ('"+numfatt+"','"+datafatt+"','"+annocorto+"','"+cliente+"','"+cliente_invio+"','"+mail+"')")
cursiq.close()#SYBASE IQ NON SERVE ORA




#cursm.execute("TRUNCATE TABLE bandiera") #da inserire alla fine????