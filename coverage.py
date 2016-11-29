import wget
import requests,bs4,re,csv
from credentials import *

#ciresturl='http://username:password@url/app/rest'
release='.'

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "text/html;charset=utf-8"
}


def getCoverage(id,build_tag,proj_tag):
    
    response = requests.get(ciresturl+'/builds/id:'+id+'/statistics',headers,stream=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    if soup.find_all('property', attrs={"name": re.compile(r"Code*")}):

        
        for cov_tag in soup.find_all('property', attrs={"name": re.compile(r"Code*")}):

            row=cov_tag['name']+','+cov_tag['value']+','+build_tag["id"]

            with open(release+'.csv','a') as f1:
                writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
                print 'Fetching coverage results for '+proj_tag["name"]
                try:
                    writer.writerow(row.split()+[',', proj_tag["name"]])
                except(UnicodeEncodeError):
                    writer.writerow(row.split()+[',', proj_tag["name"].encode('utf-8')])
                    
                    
    else:
        print 'No Coverage Details found for '+proj_tag["name"]
    
##def getBuildtype():
##    response = requests.get(ciresturl+'/builds/',headers,stream=False)       
##    soup = bs4.BeautifulSoup(response.content, "html.parser")
##    if soup.find_all('build', attrs={'status':"SUCCESS","buildtypeid": re.compile(".")}):
##       for build_tag in soup.find_all('build', attrs={'status':"SUCCESS","buildtypeid": re.compile(release)}):
##            print build_tag['buildtypeid']
####            getCoverage(tag['id'])



def getProject():
    response = requests.get(ciresturl+'/projects/',headers,stream=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    
    for proj_tag in soup.find_all('project', attrs={"href": re.compile(release)}):
       
       
        getBuildtypeFromproject(proj_tag)


def getBuildtypeFromproject(proj_tag):
    
    response = requests.get(ciresturl+'/projects/id:'+proj_tag['id'],headers,stream=False)       
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    
    for build_tag in soup.find_all('buildtype', attrs={"href": re.compile(r'Coverage')}):

            
            response = requests.get(ciresturl+'/builds/?locator=buildType:('+build_tag["id"]+')&count=1',headers,stream=False)
            rsoup = bs4.BeautifulSoup(response.content, "html.parser")
          
            if rsoup.find(True,{'status':"SUCCESS","id":True}):
                buildid=rsoup.find(True,{'status':"SUCCESS","id":True})
                getCoverage(buildid['id'],build_tag,proj_tag)
               
            else:
                print 'No Coverage Details found for '+proj_tag["name"]
            
getProject()




