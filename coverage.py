import wget
import requests,bs4,re,csv
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


def getCoverage(id,bid):
    
    response = requests.get(ciresturl+'/builds/id:'+id+'/statistics',headers,stream=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    if soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
##        print '===='+job+'===='
        
        for cov_tag in soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
##            print cov_tag['name']+','+cov_tag['value']
            row=cov_tag['name']+','+cov_tag['value']
            print row
            with open('large.csv','a') as f1:
                writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
##                writer.writerow(row.split()+[',']+[bid])
                writer.writerow(row.split()+[',',bid])
    else:
        print 'No Coverage Details found for'+bid
    
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
    for proj_tag in soup.find_all('project', attrs={"href": re.compile(r'16')}):
##        print proj_tag['id']
        proid=proj_tag['id']
##        print proid
        
        getBuildtypeFromproject(proid)


def getBuildtypeFromproject(proid):
    response = requests.get(ciresturl+'/projects/id:'+proid,headers,stream=False)       
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    
    for build_tag in soup.find_all('buildtype', attrs={"href": re.compile(r'Coverage')}):
            bid=build_tag["id"]
            print bid
            
            response = requests.get(ciresturl+'/builds/?locator=buildType:('+build_tag["id"]+')&count=1',headers,stream=False)
            rsoup = bs4.BeautifulSoup(response.content, "html.parser")
##            
            if rsoup.find(True,{'status':"SUCCESS","id":True}):
                buildid=rsoup.find(True,{'status':"SUCCESS","id":True})
                getCoverage(buildid['id'],bid)
            else:
                print 'No Coverage Details found for'+bid
            
        
getProject()

def getbCoverage(id):
    
    response = requests.get(ciresturl+'/builds/id:'+id+'/statistics',headers,stream=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    if soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
##        print '===='+job+'===='
        
        for cov_tag in soup.find_all('property', attrs={"name": re.compile(r"Code*")}):
            row=[cov_tag['name']+','+cov_tag['value']]
            print row
            with open('large.csv','a') as f1:
                writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
                writer.writerow(row+[',berry'])
    else:
        print 'No Coverage Details found for'+bid

##getbCoverage(id='147729')

##print '=============================='
##getBuildtype()
##        
##    if soup.find_all('buildtype', attrs={"id": re.compile("debugtestcoverage")}):    
    

