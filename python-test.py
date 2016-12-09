import sqlite3
conn = sqlite3.connect('rk.db')

##conn.execute('''CREATE TABLE COMPANY
##       (ID INT PRIMARY KEY     NOT NULL,
##       NAME           TEXT    NOT NULL,
##       AGE            INT     NOT NULL,
##       ADDRESS        CHAR(50),
##       SALARY         REAL);''')

##conn.execute('''CREATE TABLE IF NOT EXISTS CHAPTER
##       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
##       ADIKAR         INT    NOT NULL,
##       TAMIL          TEXT     NOT NULL,
##       ENGLISH        TEXT     NOT NULL,
##       ENGTRANS       TEXT     NOT NULL);''')
##conn.commit()       

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
##SELECT CHAPTER.Tamil AS ADIKARAM,KURAL.TAMIL as THIRUKURAL FROM 'CHAPTER' LEFT join 'KURAL' ON CHAPTER.Adikar=KURAL.ADIKAR
##alltamil
##SELECT chapter.tamil,kural.tamil,kural.muvaurai,kural.kalaurai,kural.solourai FROM 'CHAPTER' LEFT join 'KURAL' ON CHAPTER.Adikar=KURAL.ADIKAR limit 10

#SELECT chapter.tamil,kural.tamil,kural.muvaurai,kural.kalaurai,kural.solourai FROM 'CHAPTER' LEFT join 'KURAL' ON CHAPTER.Adikar=KURAL.ADIKAR order by RANDOM() limit 1
##conn.commit()
##print "Records created successfully";
##conn.close()
##cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
cursor = conn.cursor()
##cursor.execute("DELETE FROM KURAL WHERE ID > -1;")
##cursor.execute("drop table CHAPTER")
##cursor.execute("delete from KURAL  where ADIKAR='look'")
cursor.execute("SELECT chapter.tamil,kural.tamil,kural.muvaurai,kural.kalaurai,kural.solourai FROM 'CHAPTER' LEFT join 'KURAL' ON CHAPTER.Adikar=KURAL.ADIKAR limit 10")
conn.commit()
for row in cursor:
    print "\n"
    print 'ATHIKARAM : '+row[0]
    print row[1]
    print 'MuvaUrai :'
    print row[2]
    
    
    
conn.close()

##for row in cursor:
##    print row
##   print "ID = ", row[0]
##   print "NAME = ", row[1]
##   print "ADDRESS = ", row[2]
##   print "SALARY = ", row[3], "\n"


