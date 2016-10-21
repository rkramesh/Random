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
response = requests.get(ciresturl+'/builds/',headers,stream=False)

def getCoverage(id):
    
    response = requests.get(ciresturl+'/builds/id:'+id+'/statistics',headers,stream=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    if soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
        print '===='+job+'===='
        for cov_tag in soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
            print cov_tag['name']+':'+tag['value']
    
def getBuildtype():
    response = requests.get(ciresturl+'/builds/',headers,stream=False)       
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    if soup.find_all('build', attrs={'status':"SUCCESS","buildtypeid": re.compile(".")}):
       for build_tag in soup.find_all('build', attrs={'status':"SUCCESS","buildtypeid": re.compile(".")}):
            print build_tag['buildtypeid']
##            getCoverage(tag['id'])



def getProject():
    response = requests.get(ciresturl+'/projects/',headers,stream=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    for proj_tag in soup.find_all('project', attrs={"href": re.compile(r'169')}):
##        print proj_tag['id']
        proid=proj_tag['id']
        
        getBuildtypeFromproject(proid)


def getBuildtypeFromproject(proid):
    response = requests.get(ciresturl+'/projects/id:'+proid,headers,stream=False)       
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    
    for build_tag in soup.find_all('buildtype', attrs={"href": re.compile(r'Coverage')}):
            print build_tag['id']
##            getCoverage(tag['id'])
        
getProject()
##print '=============================='
##getBuildtype()
##        
##    if soup.find_all('buildtype', attrs={"id": re.compile("debugtestcoverage")}):    
    

    
                   
    

    

