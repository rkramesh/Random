query ='now'
_author_ = "Rk"
_pyversion_ = "2.7 or lower"
import os,re,ast
import sys
import bs4
import requests
import logging
import ast,json,yaml
def search(query):

    url='http://api.gokulnath.com/thirukkuralchapters/5/thirukkurals'
##    url = 'http://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias' \
##          '%3Daps&field-ke#ywords={}'.format(query.replace(' ', '+'))
    
    return scrape(url)
    print (url)
def scrape(url):
    response = requests.get(url,
                            headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                   '6.2; WOW64) AppleWebKit/'
                                                   '537.36 (KHTML, like '
                                                   'Gecko) Chrome/37.0.2062.'
                                                   '120 Safari/537.36'})
    rk=response.content
    #rk = "\n".join(rk.split("<br />"))
    
    d = yaml.load(rk)
    
    for tag in d['Data']:
        print "\n".join(tag['Tamil'].split("<br />"))# replacing break statement with new line statement
        print "\n".join(tag['English'].split("<br />"))
        print "\n".join(tag['KalaignarUrai'].split("<br />"))
        
##['Index', 'Tamil', 'EnglishMeaning', 'MuVaUrai', 'English', 'KalaignarUrai', 'SolomonPaapaiyaUrai', 'TamilTransliteration']          
     
      
        
search('now')


