import jaydebeapi
import jpype

jar = 'C:\IBM\jdbcmysql.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
con1=jaydebeapi.connect('com.mysql.jdbc.Driver', 'jdbc:mysql://localhost:3306/billtomail',['billtomail','billtomail']) #connessione al db2
cursm=con1.cursor()
cursm.execute("SELECT * FROM date")


	
curs.close()
conn.close()
