import pyodbc
import jaydebeapi
import jpype
cnxn = pyodbc.connect("DSN=melc6h1_dmcomm")
cursiq = cnxn.cursor()
jar = 'C:\IBM\jdbcmysql.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
con1=jaydebeapi.connect('com.mysql.jdbc.Driver', 'jdbc:mysql://localhost:3306/billtomail',['billtomail','billtomail']) #connessione al db2
cursm=con1.cursor()
cursm.execute("TRUNCATE TABLE invio")
#SELEZIONO LE FATTURE DA INVIARE SU SYBASE IQ
sql = "SELECT distinct substr(dba.artfatt3.f_cliente,1,8) as f_cliente, dba.artfatt3.cli_invio_doc, dba.artfatt3.numero_fattura, dba.artfatt3.data_fattura, dba.clienti_email.E_mail FROM dba.artfatt3 LEFT OUTER JOIN dba.clienti_email ON (dba.artfatt3.cli_invio_doc = dba.clienti_email.Codice_cliente) WHERE dba.clienti_email.E_mail is not null and dba.artfatt3.data_fattura>='20171001' and dba.artfatt3.data_fattura<'20171005'"
cursiq.execute(sql)
fatture = cursiq.fetchall()
#MI SALVO I CAMPI ESTRATTI DA SYBASE IQ SU MYSQL DI COMODO
for fattura in fatture:  
	cliente=fattura[0]
	cliente_invio=fattura[1]
	numfatt=fattura[2]
	datafatt=fattura[3]
	mail=fattura[4]
	datafatt=str(datafatt) #rendo il campo datetime una stringa
	anno=datafatt[:4]#substring per ottenere l'anno  (caratteri 1 a 4)
	#INSERISCO I DATI LETTI SU MYSQL NELLA TABELLA DI COMODO INVIO
	cursm.execute("INSERT INTO invio (fattura,data,anno,cod_cliente,cod_cliente_invio,mail) VALUES ('"+numfatt+"','"+datafatt+"','"+anno+"','"+cliente+"','"+cliente_invio+"','"+mail+"')")
cursiq.close()#SYBASE IQ NON SERVE ORA

cursm.execute("UPDATE invio SET mail='f.avino@melchioni.it' WHERE 1")