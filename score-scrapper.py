import os, re
import bs4,time
import requests
class score(object):

    def __init__(self):
        #will be using it for enhancements
        pass

    def getMatch(self):
        url='http://www.cricbuzz.com/cricket-match/live-scores'
        response = requests.get(url,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
##        for tag in soup.find_all('h2',{'href':re.compile('.*live-cricket-scores')}):
##            print tag['href']
        for tag in soup.find_all(re.compile('a'),{'class':re.compile('.*cb-mat-mnu')}):
            print tag
            


            
        
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
        print soup.find('div',{'class':re.compile('.*cb-min-bat-rw')}).text.strip()+'\n'
        
        for tag in soup.find_all(re.compile('.')):
            try:
               print tag.div.find('div',{'class':re.compile('.*cb-ovr-num')}).text+' '+tag.p.text
            except AttributeError:
               pass
                
##while True:
##    cricbuzz=score()
##    cricbuzz.getScore()
##    time.sleep(15)

s=score()
s.getMatch()
    

    
