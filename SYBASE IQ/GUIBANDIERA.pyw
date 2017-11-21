# import the library
from appJar import gui
import jaydebeapi
import jpype

#CONNESSIONE A MYSQL
jar = 'C:\IBM\jdbcmysql.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
con1=jaydebeapi.connect('com.mysql.jdbc.Driver', 'jdbc:mysql://10.1.12.144:3306/billtomail',['billtomail','billtomail']) #connessione al db2
cursm=con1.cursor()
########FINE MYSQL



#SOSTITUTO DEL FILE BANDIERA CHIAMATO DA FUNZIONE###################################################
def bandiera(): #il parametro global prima delle variabili serve a passare alla funzione la variabile globale invece che crearne una globale
	global idbandiera
	global inizio_bandiera
	global fine_bandiera
	global forzata
	global esecuzione
	global errore
	global tot_mail
	global rimanenti
	global rimanentistring
	cursm.execute("SELECT * FROM bandiera")
	datas=cursm.fetchall() 
	data=datas[0] #seleziono riga 0
	idbandiera=str(data[0])#seleziono i campi convertendoli in stringa
	inizio_bandiera=data[1] #seleziono i campi
	fine_bandiera=data[2] #seleziono i campi
	forzata=data[3] #seleziono i campi
	esecuzione=data[4] #seleziono i campi
	errore=data[6] #seleziono i campi
	tot_mail=str(data[5]) #seleziono i campi
	cursm.execute("SELECT COUNT(*) FROM invio")
	rimanenti=cursm.fetchone()[0]#CONTO LE RIGHE
	rimanentistring=str(rimanenti)
###############################################################FINE BANDIERA
##############################################################################FUNZIONE REFRESH
def ricarica():
	bandiera()
	app.setLabel("invii", "MANCANO "+rimanentistring+" INVII SU "+tot_mail) #NOMELABEL, CONTENUTO
	app.setEntry("inizio",inizio_bandiera)#ricarico da DB
	app.setEntry("fine",fine_bandiera)#ricarico da DB
	if forzata!=0:
		print ("FORZATA!!!")
		app.setLabelFg("forzata", "red")#NOME LABEL, COLORE CARATTERE
	else:
		app.setLabelFg("forzata", "yellow")#NOME LABEL, COLORE CARATTERE
	if esecuzione!=0:
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ESECUZIONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		app.setLabelFg("esecuzione", "red")#NOME LABEL, COLORE CARATTERE
		app.hideButton("Modifica") #NASCONDE IL TASTO
	else:
		app.setLabelFg("esecuzione", "yellow")
		app.showButton("Modifica") #SVELA IL TASTO
	if rimanenti!=0:
		app.setLabelFg("invii", "green") #NOME LABEL, COLORE CARATTERE
		if esecuzione==0:
			app.setLabelFg("invii", "red") #NOME LABEL, COLORE CARATTERE
	else:
		app.setLabelFg("invii", "yellow") #NOME LABEL, COLORE CARATTERE
	if errore!=0:
		app.setLabelFg("errore", "red") #NOME LABEL, COLORE CARATTERE
		app.showButton("Rimuovi Errore") #SVELA IL TASTO
	else:
		app.setLabelFg("errore", "yellow") #NOME LABEL, COLORE CARATTERE
		app.hideButton("Rimuovi Errore") #NASCONDE IL TASTO
###################################################################################################################FINE REFRESH


bandiera()




# handle button events
def press(button):
	if button == "Ricarica":
		ricarica()

	if button == "Modifica":
		inizio=app.getEntry("inizio")
		fine=app.getEntry("fine")
		cursm.execute("UPDATE BANDIERA SET inizio="+inizio+",fine="+fine+",forzata='1' WHERE id='"+idbandiera+"'")
	
	if button == "Rimuovi Errore":
		cursm.execute("UPDATE BANDIERA SET errore='0' WHERE id='"+idbandiera+"'")
		ricarica()
		


# create a GUI variable called app
app = gui("BANDIERA BILLTOMAIL By Franco Avino", "600x300")
app.setBg("yellow")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "\nModifica bandiera BILLTOMAIL\n") #NOMELABEL, CONTENUTO
app.setLabelBg("title", "blue")#NOMELABEL, COLORE SFONDO
app.setLabelFg("title", "red") #NOME LABEL, COLORE CARATTERE


app.addLabel("datai","Data inizio") #NOMELABEL, CONTENUTO
app.setLabelFg("datai", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("inizio")
app.addLabel("dataf","Data fine")#NOMELABEL, CONTENUTO
app.setLabelFg("dataf", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("fine")
app.setEntryDefault("inizio",inizio_bandiera)#l'aggiunta di Default permette di mettere un valore default alla label text
app.setEntryDefault("fine",fine_bandiera)#l'aggiunta di Default permette di mettere un valore default alla label text

app.addLabel("invii", "MANCANO "+rimanentistring+" INVII SU "+tot_mail) #NOMELABEL, CONTENUTO
if rimanenti!=0:
	app.setLabelFg("invii", "green") #NOME LABEL, COLORE CARATTERE
	if esecuzione==0:
		app.setLabelFg("invii", "red") #NOME LABEL, COLORE CARATTERE
else:
	app.setLabelFg("invii", "yellow") #NOME LABEL, COLORE CARATTERE



app.addLabel("forzata","DATA FORZATA")#NOMELABEL, CONTENUTO
if forzata!=0:
	app.setLabelFg("forzata", "red")#NOME LABEL, COLORE CARATTERE
else:
	app.setLabelFg("forzata", "yellow")#NOME LABEL, COLORE CARATTERE

app.addLabel("esecuzione","BILLTOMAIL IN ESECUZIONE")#NOMELABEL, CONTENUTO
if esecuzione!=0:
	app.setLabelFg("esecuzione", "red")#NOME LABEL, COLORE CARATTERE
else:
	app.setLabelFg("esecuzione", "yellow")#NOME LABEL, COLORE CARATTERE

	
app.addLabel("errore","BILLTOMAIL TERMINATO IN ERRORE")#NOMELABEL, CONTENUTO
if errore!=0:
	app.setLabelFg("errore", "red")#NOME LABEL, COLORE CARATTERE
else:
	app.setLabelFg("errore", "yellow")#NOME LABEL, COLORE CARATTERE
	

app.addButtons(["Modifica","Ricarica","Rimuovi Errore"], press)
if esecuzione!=0:
	app.hideButton("Modifica") #NASCONDE IL TASTO
if errore==0:
	app.hideButton("Rimuovi Errore")

# start the GUI
app.go()