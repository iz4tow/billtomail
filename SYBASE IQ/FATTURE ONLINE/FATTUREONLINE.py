# import the library
from appJar import gui
import pyodbc

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#CONNESSIONE A MYSQL
cnxn = pyodbc.connect("DSN=melc6h1_dmcomm")
cursiq = cnxn.cursor()
########FINE MYSQL



##############################################APERTURA FILE INI IMPOSAZIONI###############################################################
file = open("setting.ini", "r") 
for riga in file:
	if riga.find("|")!=-1: #SOLO LE RIGHE DELLE IMPOSTAZIONI CHE CONTENGONO IL | VENGONO CONSIDERATE, GLI ALTRI SONO COMMENTI
		riga=riga.replace(" ","") #TOGLO GLI SPAZI BIANCHI
		impostazione,valore=riga.split("|"); #PRENDE IMPOSTAZIONE E VALORE IMPOSTAZIONE USANDO COME SEPARATORE I :
		if impostazione=='mail':
			fromaddr=valore
			fromaddr=fromaddr.replace("\n","")
		if impostazione=='mailuser':
			user=valore
			user=user.replace("\n","")
		if impostazione=='mailpassword':
			password=valore
			password=password.replace("\n","")
		if impostazione=='contatto_interno':
			contatto_interno=valore
			contatto_interno=contatto_interno.replace("\n","")
##############################################FINE FILE INI IMPOSAZIONI###################################################################



##########################################INVIO MAIL PRIVACY##############################################################################

def privacy():
	global email
	global contatto_interno
	global user
	global password
	global fromaddr
	oggi=time.strftime('%d-%m-%Y')#data di oggi
	fine=oggi #SALVO DIVERSA IMPOSTAZIONE NELLA BANDIERA LA FINE E' OGGI
	mails=email+","+contatto_interno
	privacy = MIMEMultipart()
	privacy['From'] = fromaddr
	privacy['To'] = mails
	privacy['Subject'] = "INVIO FATTURE TELEMATICO MELCHIONI SPA"

	corpo = "Milano, "+oggi+"<br><br>Gentile Cliente,"
	corpo = corpo +"<br>come da Lei richiesto, Le comunichiamo che il servizio di fatturazione cartaceo verrà sostituito dalla versione elettronica."
	corpo = corpo +"<br>Le ricordiamo di contattare la nostra amministrazione per eventuali modifiche."
	corpo = corpo +"<br>Qui di seguito Le riportiamo il suo indirizzo mail: "+email+"<br>"
	corpo = corpo +"<br>Questo messaggio Le viene inviato a seguito della Sua richiesta e nel rispetto della vigente normativa sulla privacy di cui di seguito riportiamo i consensi forniti:"
	corpo = corpo +"<br><li><b>Consenso per le finalità di cui al punto a) Gestione della clientela, adempimento di obblighi contabili e fiscali, programmazione delle attività, servizi di controllo interno, gestione del contenzioso:</b></li>"
	corpo = corpo +"<br><i>Il Cliente acconsente che i propri dati siano utilizzati da Melchioni e/o comunicati a terzi per le finalità di cui al punto a.</i>"
	corpo = corpo +"<br><li><b>Consenso per attività, promozionali di cui al punto b) anche mediante strumenti telematici ai sensi dell’articolo 23 del Decreto Legislativo 30 giugno 2003, n. 196:</b></li>"
	corpo = corpo +"<br><i>Il Cliente consente inoltre che i propri dati anagrafici siano utilizzati da Melchioni e/o comunicanti a terzi che svolgono attività commerciali e promozionali per finalità di marketing, pubblicità, manifestazioni a premi e rilevazione del grado di soddisfazione della clientela, ivi compreso l’invio di materiale illustrativo relativo ai servizi e ai prodotti commercializzati, quali particolari offerte vantaggiose e nuovi servizi.</i>"
	corpo = corpo +"<br><br><br>Cordiali saluti<br>Melchioni S.p.A.<br>Amministrazione Clienti e Credito<br><br>Questo messaggio Le viene inviato a seguito della Sua richiesta e nel rispetto della vigente normativa sulla privacy."

	privacy.attach(MIMEText(corpo, 'html'))
	server = smtplib.SMTP('owa.melchioni.it', 25)
	server.starttls()
	server.login(user, password)
	privacyor = privacy.as_string()
	server.sendmail(fromaddr, mails, privacyor)
	server.quit()

############################################################################################################################



# handle button events
def press(button):
	app.hideLabel("avviso1") #nascondo avviso1 di comodo per avvisi
	if button == "Inserisci":
		global email
		codcli=app.getEntry("codicecliente")
		cursiq.execute("SELECT e_mail FROM DBA.clienti_email where codice_cliente='"+codcli+"'")
		esiste=len(cursiq.fetchall())#lunghezza array estratto, conto le righe insomma...
		if esiste>0:
			app.showLabel("avviso1")
			app.setLabel("avviso1","RECORD DUPLICATO, FORSE VUOI MODIFICARLO?")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		else:
			email=app.getEntry("email")
			cursiq.execute("INSERT INTO DBA.clienti_email (codice_cliente,e_mail) VALUES ('"+codcli+"','"+email+"')")
			cursiq.execute("commit")
			app.showLabel("avviso1") #nascondo avviso1 di comodo per avvisi
			app.setLabel("avviso1","RECORD INSERITO")
			app.setLabelFg("avviso1", "green")#NOMELABEL, COLORE SFONDO
			privacy()
	if button == "Rimuovi":
		codcli=app.getEntry("codicecliente")
		cursiq.execute("SELECT e_mail FROM DBA.clienti_email where codice_cliente='"+codcli+"'")
		esiste=len(cursiq.fetchall())#lunghezza array estratto, conto le righe insomma...
		if esiste>0:
			cursiq.execute("DELETE DBA.clienti_email where codice_cliente='"+codcli+"'")
			cursiq.execute("commit")
			app.showLabel("avviso1")
			app.setLabel("avviso1","RECORD CANCELLATO")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		else:
			app.showLabel("avviso1")
			app.setLabel("avviso1","CLIENTE INESISTENTE")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
	if button == "Ricerca":
		codcli=app.getEntry("codicecliente")
		cursiq.execute("SELECT e_mail FROM DBA.clienti_email where codice_cliente='"+codcli+"'")
		rows=cursiq.fetchall() 
		esiste=len(rows)
		if esiste>0:
			row=rows[0]
			email=row[0]
			app.setEntry("email",email)
		else:
			app.showLabel("avviso1")
			app.setLabel("avviso1","CLIENTE INESISTENTE")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO

	if button == "Modifica":
		codcli=app.getEntry("codicecliente")
		email=app.getEntry("email")
		cursiq.execute("SELECT e_mail FROM DBA.clienti_email where codice_cliente='"+codcli+"'")
		esiste=len(cursiq.fetchall())#lunghezza array estratto, conto le righe insomma...
		if esiste>0:
			cursiq.execute("UPDATE DBA.clienti_email SET e_mail='"+email+"'where codice_cliente='"+codcli+"'")
			cursiq.execute("commit")
			app.showLabel("avviso1")
			app.setLabel("avviso1","RECORD MODIFICATO")
			app.setLabelFg("avviso1", "green")#NOMELABEL, COLORE SFONDO
		else:
			app.showLabel("avviso1")
			app.setLabel("avviso1","CLIENTE INESISTENTE")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO


# create a GUI variable called app
app = gui("Inserimento FATTUREONLINE - By FRANCO AVINO", "600x300")
app.setBg("yellow")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "\nInserimento FATTUREONLINE\n") #NOMELABEL, CONTENUTO
app.setLabelBg("title", "blue")#NOMELABEL, COLORE SFONDO
app.setLabelFg("title", "red") #NOME LABEL, COLORE CARATTERE


app.addLabel("cliente","Codice Cliente") #NOMELABEL, CONTENUTO
app.setLabelFg("cliente", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("codicecliente")
app.setEntryDefault("codicecliente","Codice cliente")
app.addLabel("mail","Indirizzo Mail") #NOMELABEL, CONTENUTO
app.setLabelFg("mail", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("email")
app.setEntryDefault("email","Indirizzo mail")

app.addLabel("avviso1"," ") #NOMELABEL, CONTENUTO
app.hideLabel("avviso1") #nascondo avviso1 di comodo per avvisi

app.addButtons(["Inserisci","Ricerca","Modifica","Rimuovi"], press)





# start the GUI
app.go()