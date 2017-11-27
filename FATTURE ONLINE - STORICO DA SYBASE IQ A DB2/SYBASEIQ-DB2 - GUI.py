# import the library
import pyodbc
import jaydebeapi
import jpype
import time
import os 
from appJar import gui

start_time = time.time()

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

#######BACKUP DATI SU DB2#################################################################
def export_db2():
	app.showLabel("tempo")
	app.setLabel("tempo","ESPORTAZIONE DATI DA DB2") 
	app.hideButton("Esegui")
	app.hideButton("Dump DB2")
	app.hideButton("Dump SYBASEIQ")
	oggi=time.strftime('%d-%m-%Y')#data di oggi
	
	backup="DB2-AZMAIL-BACKUP"+oggi+".txt"
	
	if os.path.isfile(backup):
		controllo1 =app.yesNoBox("CONFERMA", "Esiste già un backup con la data di oggi, sovrascrivo?", parent=None)
		if controllo1:
			controllo2 = app.yesNoBox("CONFERMA", "Sei sicuro?", parent=None)
			if controllo2:
				print ("PROVO A SOVRASCRIVERE IL FILE...\n")
			else:
				exit()
		else:
			exit()
	
		
	iniz_bck_time=time.time()
	curs.execute("SELECT * FROM DIGI.TABUTE_AZMAIL")
	rows=curs.fetchall()
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
	bck_fine_time=time.time()
	tempo=str(int(bck_fine_time-iniz_bck_time))
	app.showLabel("tempo") #nascondo avviso1 di comodo per avvisi
	app.setLabel("tempo","TEMPO PER L'ESPORTAZIONE: "+tempo+" secondi")
	app.showButton("Esegui")
	app.showButton("Dump DB2")
	app.showButton("Dump SYBASEIQ")
	
#######BACKUP DATI SYBASE IQ#################################################################
def export_iq():
	app.showLabel("tempo")
	app.setLabel("tempo","ESPORTAZIONE DATI DA SYBASE IQ") 
	app.hideButton("Esegui")
	app.hideButton("Dump DB2")
	app.hideButton("Dump SYBASEIQ")
	oggi=time.strftime('%d-%m-%Y')#data di oggi
	
	backup="SYBASEIQ-AZMAIL-BACKUP"+oggi+".txt"
	
	if os.path.isfile(backup):
		controllo1 =app.yesNoBox("CONFERMA", "Esiste già un backup con la data di oggi, sovrascrivo?", parent=None)
		if controllo1:
			controllo2 = app.yesNoBox("CONFERMA", "Sei sicuro?", parent=None)
			if controllo2:
				print ("PROVO A SOVRASCRIVERE IL FILE...\n")
			else:
				exit()
		else:
			exit()
	
		
	iniz_bck_time=time.time()
	curs.execute("SELECT * FROM DIGI.TABUTE_AZMAIL")
	rows=curs.fetchall()
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
	bck_fine_time=time.time()
	tempo=str(int(bck_fine_time-iniz_bck_time))
	app.showLabel("tempo") #nascondo avviso1 di comodo per avvisi
	app.setLabel("tempo","TEMPO PER L'ESPORTAZIONE: "+tempo+" secondi")
	app.showButton("Esegui")
	app.showButton("Dump DB2")
	app.showButton("Dump SYBASEIQ")



########PROCEDURA SYBASE -> DB2
def sydb2():
	app.showLabel("tempo")
	app.setLabel("tempo","BACKUP DATI SU DB2") 
	app.hideButton("Esegui")
	app.hideButton("Dump DB2")
	app.hideButton("Dump SYBASEIQ")
	start_time=time.time()
	export_db2()
	app.setLabel("tempo","...PROCEDURA MIGRAZIONE...") 
	cursiq.execute("SELECT codice_cliente,e_mail FROM DBA.clienti_email") #SELEZIONO TUTTA LA TABELLA
	rows=cursiq.fetchall()
	daimportare=len(rows)
	countmodificate=0
	countnuove=0
	for row in rows: #per ogni riga
		codcli=row[0]
		email=row[1]
		curs.execute("SELECT DG_INDIRIZZO_EMAIL FROM DIGI.TABUTE_AZMAIL WHERE MK_CONTROPARTE='"+codcli+"' AND MK_TIPO_CONTROPART='CLIENT' AND MK_UNITA_ORGANIZ='CNTFOR'")
		esisteibm=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
		if esisteibm>0: #SE GIA ESISTE AGGIORNO SOLO LA MAIL
			curs.execute("UPDATE DIGI.TABUTE_AZMAIL SET DG_INDIRIZZO_EMAIL='"+email+"',MK_FATT_MAIL='1' WHERE MK_CONTROPARTE='"+codcli+"'")
			curs.execute("commit")
			countmodificate=countmodificate+1
		else:#ALTRIMENTI LO INSERISCO
			curs.execute("INSERT INTO DIGI.TABUTE_AZMAIL (DG_C_SOC,DG_C_DIVS,DG_C_VERS,MK_DIVISIONE,MK_TIPO_CONTROPART,MK_CONTROPARTE,MK_UNITA_ORGANIZ,MK_PROGR_2,DG_INDIRIZZO_EMAIL,MK_FATT_MAIL) VALUES ('0100','00','00','00','CLIENT','"+codcli+"','CNTFOR','1','"+email+"','1')")
			curs.execute("commit")
			countnuove=countnuove+1
	
	end_time=time.time()
	tempo=str(int(end_time-start_time))
	app.showLabel("tempo") #nascondo avviso1 di comodo per avvisi
	app.setLabel("tempo","TEMPO PER IL PASSAGGIO: "+tempo+" secondi")
	
	daimportare=str(daimportare)
	countnuove=str(countnuove)
	countmodificate=str(countmodificate)
	
	app.infoBox("IMPORTAZIONE COMPLETATA", "RIGHE SU SYBASE IQ: "+daimportare+"\nRIGHE INSERITE SU DB2: "+countnuove+"\nRIGHE MODIFICATE SU DB2: "+countmodificate, parent=None)
	app.showButton("Esegui")
	app.showButton("Dump DB2")
	app.showButton("Dump SYBASEIQ")
	


def press(button):
	if button == "Esegui":
		sydb2()
	if button == "Dump DB2":
		export_db2()
	if button == "Dump SYBASEIQ":
		export_iq()
		






app = gui("MIGRAZIONE CLIENTI MAIL SYBASE IQ -> DB2", "600x300")
app.setBg("yellow")
app.setFont(18)
app.addLabel("title", "\nCLIENTI MAIL SYBASE IQ -> DB2\n") #NOMELABEL, CONTENUTO
app.setLabelBg("title", "blue")#NOMELABEL, COLORE SFONDO
app.setLabelFg("title", "red") #NOME LABEL, COLORE CARATTERE

app.addLabel("tempo"," ") #NOMELABEL, CONTENUTO
app.hideLabel("tempo") #nascondo avviso1 di comodo per avvisi

app.addButtons(["Esegui","Dump DB2","Dump SYBASEIQ"], press)
app.go()