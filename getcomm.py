import bs4,time
import re,requests
start_time = time.time()
class getReview(object):
    """This Class willfetch the review Comments from commenr.txt"""

    def __init__(self, filename, rid, rk):
        self.filename = filename
        self.rid = rid
        self.rk = rk
       

    def getTest(self):
        print 'Fetching comments for %s from %s'% (self.rid,self.filename)

    def getRe(self):
        rurl ='http://fisheye.cuc.com/rest-service/reviews-v1/'+self.rid+'/comments/'
                
                
        response = requests.get(rurl,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        
        
        for tag in soup.find_all(re.compile(r'versionedLineCommentData',flags=re.I)):
            print tag.message.contents
            try:
                print tag.username.contents
            except:
                print 'No reply found'
            
        
          


inst=getReview('comm.txt','cr-4914','rk')
inst.getRe()
print("--- %s seconds ---" % (time.time() - start_time))
