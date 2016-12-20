import os, re
import bs4,time,yaml,json
import requests
from pprint import pprint

class Score(object):

    def __init__(self):
        #will be using it for enhancements
        pass
   
    @staticmethod
    def getMatch():
        url='http://www.cricbuzz.com/api/html/matches-menu'
        response = requests.get(url,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        optionlist={}
        for count,tag in enumerate (soup.find_all('li',{'class':re.compile('cb-lst-mtch')})):
            print ("Enter '{}' for '{}' ".format(count,tag.a['title']))
            optionlist[count] = tag.a['href']
        choice = int(raw_input("\n>Enter Your Option here: "))
        if choice in optionlist:
           return Score.getScore('http://www.cricbuzz.com'+optionlist[choice])
        else:
            print'Wrong Option,Select again'
            Score.getMatch()
    @staticmethod
    def getScore(url):
        while True:
            
            response = requests.get(url,
                                    headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                           '6.2; WOW64) AppleWebKit/'
                                                           '537.36 (KHTML, like '
                                                           'Gecko) Chrome/37.0.2062.'
                                                           '120 Safari/537.36'})
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            
            print '\n'+soup.title.text+'\n'

            if soup.find('div',{'class':re.compile('cb-mini-col')}) :
                print soup.find('div',{'class':re.compile('cb-mini-col')} ).text.strip()+'\n'
                match='live'
            else:
                match='past'
            duplicate=''
            for tag in soup.find_all(re.compile('.')):
                try:
                    if match == 'live':
                        print tag.div.find('div',{'class':re.compile('.*cb-ovr-num')}).text+' '+tag.p.text
                    elif match == 'past':
                        if len(tag.p.text) == duplicate:
                            continue
                        else:
                            print tag.p.text+'\n'
                            duplicate=len(tag.p.text)
                        
                        
                except:
                    pass
                
            if match == 'past':
                break
            else:
                time.sleep(12)
                    
                    
                
            

Score.getMatch()
    

    
