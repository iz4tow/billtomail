# import the library
import pyodbc
import jaydebeapi
import jpype
import time
import os 


#CONNESSIONE A SYBASE IQ
cnxn = pyodbc.connect("DSN=melc6h1_dmcomm")
cursiq = cnxn.cursor()
########FINE SYBASE IQ
#CONNESSIONE A DB2
jar = 'db2jcc4.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
conn=jaydebeapi.connect('com.ibm.db2.jcc.DB2Driver', 'jdbc:db2://10.1.12.69:50000/s69mk0su',['db2inst1','db2inst1']) #connessione al db2
curs=conn.cursor()
#########FINE DB2

#######BACKUP DATI SU DB2
print ("INIZIO ESPORTAZIONE TABELLA DA DB2 PER BACKUP")
oggi=time.strftime('%d-%m-%Y')#data di oggi
curs.execute("SELECT * FROM DIGI.TABUTE_AZMAIL")
rows=curs.fetchall()

backup="AZMAIL-BACKUP"+oggi+".txt"

if os.path.isfile(backup):
	print ("ESISTE")
	controllo1 = input("Esiste già un backup con la data di oggi, sovrascrivo? SI-NO ")
	if controllo1=="SI" or controllo1=="si" or controllo1=="Si":
		controllo2 = input("Sei sicuro? SI-NO")
		if controllo2=="SI" or controllo2=="si" or controllo2=="Si":
			print ("PROVO A SOVRASCRIVERE IL FILE...\n")
		else:
			exit()
	else:
		exit()

	

file = open(backup,"w") 
for row in rows:
	controllocampo1=0
	for field in row:
		field=str(field)
		field=field.replace("None","")#ELIMINO I NULL ESTRATTI...
		if controllocampo1>0: #IL PRIMO CAMPO NON è PRECEDUTO DA ","
			file.write(',"'+field+'"')
		else:
			file.write('"'+field+'"')
		controllocampo1=controllocampo1+1
	file.write ("\n")
file.close()
########FINE BACKUP


	

