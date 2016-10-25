
class getReview(object):
    """This Class willfetch the review Comments from commenr.txt"""

    def __init__(self, filename, rid):
        self.filename = filename
        self.rid = rid

    def getTest(self):
        print 'Fetching comments for %s from %s'% (self.rid,self.filename)

    def getRe(self):
        with open(self.filename, 'r') as f:
              for line in f:
                 if 'File: ' in line:
                     print line
                 elif 'Revision Comment' in line:
                     print line
             
                 elif 'Reply by' in line:
                     print line
                 elif line.startswith('  > '):
                     print line
                                       


inst=getReview('comm.txt','cr-1567')
inst.getRe()
