##############################################APERTURA FILE INI IMPOSAZIONI###############################################################
file = open("setting.ini", "r") 
for riga in file:
	if riga.find("|")!=-1: #SOLO LE RIGHE DELLE IMPOSTAZIONI CHE CONTENGONO IL | VENGONO CONSIDERATE, GLI ALTRI SONO COMMENTI
		riga=riga.replace(" ","") #TOGLO GLI SPAZI BIANCHI
		impostazione,valore=riga.split("|"); #PRENDE IMPOSTAZIONE E VALORE IMPOSTAZIONE USANDO COME SEPARATORE I :
		if impostazione=='mail':
			fromaddr=valore
		if impostazione=='mailuser':
			user=valore
		if impostazione=='mailpassword':
			password=valore
		if impostazione=='origine_fatture':
			percorso=valore
##############################################FINE FILE INI IMPOSAZIONI###################################################################

print (fromaddr)
print (user)
print (password)
print (percorso)