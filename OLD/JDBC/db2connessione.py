import jaydebeapi
import jpype

jar = 'C:\IBM\db2jcc4.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)

conn=jaydebeapi.connect('com.ibm.db2.jcc.DB2Driver', 'jdbc:db2://10.1.12.71:50000/s71mk0pu',['db2inst1','db2inst1']) #connessione al db2

curs=conn.cursor()

with conn.cursor() as cursor:
	curs.execute("SELECT DG_INDIRIZZO_EMAIL FROM DIGI.AZ_FRANCO WHERE MK_TIPO_CONTROPART='CLIENT' AND MK_UNITA_ORGANIZ='CNTFOR' AND FATT_MAIL!='0'")
	for row in cursor:
		
	
curs.close()
conn.close()
