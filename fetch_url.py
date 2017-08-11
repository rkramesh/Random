__author__  = "Rk"
__license__ = "GPL"
__version__ = "1.0.1"
import bs4,time,re
import requests
import Request, urlopen, urlretrieve
class ParseHttp(object):

    def __init__(self):
        #will be using it for future enhancements
        pass
    @staticmethod
    def getLink():
        url = "http://fs.evonetbd.com/Media/Movies/English%20Movies/2017/"
        response = requests.get(url,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        for i in soup.find_all('tr'):
            if  i.img['alt'] != '[   ]':
                print i.a['href']
            else:
                print 'Directory'



    def read_url(url):
        url = url.replace(" ","%20")
        req = Request(url)
        a = urlopen(req).read()
        soup = BeautifulSoup(a, 'html.parser')
        x = (soup.find_all('a'))
        for i in x:
            file_name = i.extract().get_text()
            url_new = url + file_name
            url_new = url_new.replace(" ","%20")
            if(file_name[-1]=='/' and file_name[0]!='.'):
                read_url(url_new)
            print(url_new)

       

ParseHttp.read_url("http://fs.evonetbd.com/Media/Movies/English%20Movies/2017/")
