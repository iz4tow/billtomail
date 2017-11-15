import smtplib

server = smtplib.SMTP('owa.melchioni.it', 25)
server.starttls()
server.login("f.avino@melchionispa", "Fiwoldiois01")

msg = "YOUR MESSAGE!"
server.sendmail("f.avino@melchioni.it", "iz4tow@gmail.com", msg)
server.quit()