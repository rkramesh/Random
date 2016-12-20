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
            print ("select '{}' for '{}' ".format(count,tag.a['title']))
            optionlist[count] = tag.a['href']
 
        choice = int(raw_input("> "))
        
        if choice in optionlist:
           
            print optionlist[choice]
            
        else:
            pass
            
      
    def getScore(self):
        url='http://www.cricbuzz.com/live-cricket-scores/16872/ind-vs-eng-5th-test-england-tour-of-india-2016-17'
        response = requests.get(url,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        print soup.title.text
        print soup.find('div',{'class':re.compile('cb-mini-col')} ).text.strip()+'\n'

    def getYaml(self):
       
       url='http://push.cricbuzz.com/match-api/16872/commentary.json'
       response = requests.get(url,
                            headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                   '6.2; WOW64) AppleWebKit/'
                                                   '537.36 (KHTML, like '
                                                   'Gecko) Chrome/37.0.2062.'
                                                 '120 Safari/537.36'})
       rk=response.content
       data=json.loads(rk)
##       pprint(data)
       for tag in data['comm_lines']:
           if 'comm' in tag.keys(): print  "\n".join(tag['comm'].split("<br/>"))
               
       
        #rk = "\n".join(rk.split("<br />"))

    def scoreCard(self):
        url='http://www.cricbuzz.com/api/html/cricket-scorecard/16872'
        response = requests.get(url,
                            headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                   '6.2; WOW64) AppleWebKit/'
                                                   '537.36 (KHTML, like '
                                                   'Gecko) Chrome/37.0.2062.'
                                                 '120 Safari/537.36'})
        rk=response.content
        soup = bs4.BeautifulSoup(response.content, "html.parser")
##        print soup
        print soup.find_all('div',{'class':re.compile('cb-col-100')})
##        print soup.find('div',{'class':re.compile('.*cb-min-bat-rw')}).text.strip()+'\n'
       
##      
##        
##        for tag in soup.find_all(re.compile('.')):
##            try:
####               print tag.div.find('div',{'class':re.compile('.*cb-ovr-num')}).text+' '+tag.p.text
##                print tag.div.find('div',{'class':re.compile('ccb-mini-col')})
##            except AttributeError:
##               pass
##                
##while True:
##    cricbuzz=score()
##    cricbuzz.getScore()
##    time.sleep(15)


Score.getMatch()
    

    
