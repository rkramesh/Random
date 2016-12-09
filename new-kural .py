query ='now'
_author_ = "Rk"
_pyversion_ = "2.7 or lower"
import os,re,ast
import sys
import bs4
import requests
import logging
import ast,json,yaml,sqlite3
def search(url,i):

    #url='http://api.gokulnath.com/thirukkuralchapters/11/thirukkurals'
    return scrape(url,i)
    print (url)
def scrape(url,i):
    response = requests.get(url,
                            headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                   '6.2; WOW64) AppleWebKit/'
                                                   '537.36 (KHTML, like '
                                                   'Gecko) Chrome/37.0.2062.'
                                                   '120 Safari/537.36'})
    conn = sqlite3.connect('rk.db')
    cursor = conn.cursor()
    rk=response.content
    d = yaml.load(rk)
    
    for entry,tag in enumerate (d['Data']):
        item = [
##        tag['Index'], added in iteration
        "\n".join(tag['Tamil'].split("<br />")),
        "\n".join(tag['English'].split("<br />")),
        tag['MuVaUrai'],
        tag['KalaignarUrai'],
        tag['SolomonPaapaiyaUrai'],
        "\n".join(tag['TamilTransliteration'].split("<br />")),
        tag['EnglishMeaning'],
        ]
        query="INSERT INTO KURAL VALUES (null,"+i+",?,?,?,?,?,?,?)"
        cursor.execute(query,item)
        
    conn.commit()
    conn.close()


print "Opened database successfully"
##conn.execute('''CREATE TABLE IF NOT EXISTS KURAL
##       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
##       ADIKAR         INT      NOT NULL,
##       TAMIL          TEXT     NOT NULL,
##       ENGLISH        TEXT     NOT NULL,
##       MUVAURAI       TEXT     NOT NULL,
##       KALAURAI       TEXT     NOT NULL,
##       SOLOURAI       TEXT     NOT NULL,
##       TAMTRANS       TEXT     NOT NULL,
##       ENGMEAN        TEXT     NOT NULL);''')
##conn.commit()

for i in  range(1,134,1):
    print 'updating ADIKAR:'+str(i)
    search('http://api.gokulnath.com/thirukkuralchapters/'+str(i)+'/thirukkurals',str(i))


