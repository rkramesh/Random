import wget
import requests,bs4,re
from credentials import *

##headers={'User-agent': 'Mozilla/5.0 (Windows NT '
##                                 '6.2; WOW64) AppleWebKit/'
##                                 '537.36 (KHTML, like '
##                                 'Gecko) Chrome/37.0.2062.'
##                                 '120 Safari/537.36'}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "text/html;charset=utf-8"
}
response = requests.get(ciresturl+'/builds/id:147694/statistics',headers)
#print response.content

def getCoverage():
    
    response = requests.get(ciresturl+'/builds/id:147694/statistics',headers)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    for tag in soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
        print tag['name']+':'+tag['value']
    
                   
    
getCoverage()
    

