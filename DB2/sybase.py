import pyodbc
cnxn = pyodbc.connect("DSN=melc6h1_dmcomm")
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM DBA.agenti")
rows = cursor.fetchall()
for row in rows:
    print (row)