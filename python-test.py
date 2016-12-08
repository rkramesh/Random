import sqlite3
conn = sqlite3.connect('rk.db')
print "Opened database successfully"
##conn.execute('''CREATE TABLE COMPANY
##       (ID INT PRIMARY KEY     NOT NULL,
##       NAME           TEXT    NOT NULL,
##       AGE            INT     NOT NULL,
##       ADDRESS        CHAR(50),
##       SALARY         REAL);''')

conn.execute('''CREATE TABLE IF NOT EXISTS KURAL
       (ID INT PRIMARY KEY,
       ADIKAR         INT    NOT NULL,
       TAMIL          TEXT     NOT NULL,
       ENGLISH        TEXT     NOT NULL,
       MUVAURAI       TEXT     NOT NULL,
       KALAURAI       TEXT     NOT NULL,
       SOLOURAI       TEXT     NOT NULL,
       TAMTRANS       TEXT     NOT NULL);''')
conn.commit()       

#create database for tku


##conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
##      VALUES (1, 'Paul', 32, 'California', 20000.00 )");
##
##conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
##      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");
##
##conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
##      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");
##
##conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
##      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
##
##conn.commit()
##print "Records created successfully";
##conn.close()
##cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
cursor = conn.cursor()
##cursor.execute("DELETE FROM KURAL WHERE ID > -1;")
##cursor.execute("drop table KURAL")
##cursor.execute("delete from KURAL  where ADIKAR='look'")
cursor.execute("select * from KURAL")
conn.commit()
for row in cursor:
    print row
conn.close()

##for row in cursor:
##    print row
##   print "ID = ", row[0]
##   print "NAME = ", row[1]
##   print "ADDRESS = ", row[2]
##   print "SALARY = ", row[3], "\n"


