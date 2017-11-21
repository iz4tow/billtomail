import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


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
		if impostazione=='origine_fatture':
			percorso=valore
			percorso=percorso.replace("\n","")
		if impostazione=='contatto_interno':
			contatto_interno=valore
			contatto_interno=contatto_interno.replace("\n","")
##############################################FINE FILE INI IMPOSAZIONI###################################################################

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = contatto_interno
msg['Subject'] = "INVIO FATTURE TELEMATICO MELCHIONI S.P.A."

body = "In allegato il log del billtomail"

msg.attach(MIMEText(body, 'plain'))

filename = "log.txt"

attachment = open(filename, "rb")
	

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read()) #CARICA l'ALLEGATO
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)	#preparo l'allegato nell'header, la variabile documento è il nome
msg.attach(part)#allego il file		
server = smtplib.SMTP('owa.melchioni.it', 25)
server.starttls()
server.login(user, password)
text = msg.as_string()
server.sendmail(fromaddr, contatto_interno, text)
server.quit()