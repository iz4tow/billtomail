import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
counterror=0
fromaddr = "f.avino@melchioni.it"
toaddr = "iz4tow@gmail.com"
user = "f.avino@melchionispa"
password = "Fiwoldiois01"

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