#!/usr/bin/python
import os
import re
import urllib2
import urllib
import csv,requests,bs4,linecache,wget,codecs,tempfile
import xmltodict
from collections import defaultdict
#from itertools import islice
#from linecache import getline
searchprint = '(CR-\d+.*?)'
rawdata = '16.8.txt'
dupdata = 'data.txt'
sortdata = 'sorted.txt'
def findallreview():
    '''
    Module to be added for downloadind data from db
    '''
def searchwrite(searchprint, rawdata):
    #open file in read mode
    rk = open(rawdata , "r")
    #read the contents of the file to variable
    s  = rk.read()
    #match the content to variable
    #matches = re.findall('(CR-\d+.*?)' , s ,re.DOTALL)
    matches = re.findall(searchprint , s ,re.DOTALL)
    #print (matches)
    #open a new file to write the output
    f = open(dupdata, "w")
    #print '\n'.join(map(str, matches))
    #write the output data
    f.write('\n'.join(map(str, matches)))
def removeDuplicate(dupdata):
    prev = None
    for line in sorted(open(dupdata)):     
          #line = line.strip()
          if prev is not None and not line.startswith(prev):
            #print prev
            fdata = open(sortdata, "a")
            fdata.write(prev)
          prev = line
    if prev is not None:
        #print prev
        fdata = open(sortdata, "a")
        fdata.write(prev)
def finddata():
     'Module for data to be fetched and parsed into csv'
     print 'started'    
     with open(sortdata, 'r') as f:
         for line in f:
               line = line.strip('\n')
               durl='http://fisheye.com/cru/'+line+'/comments.txt'
               print durl
               response = urllib2.urlopen(durl)
               op = response.read()
               #print op
               matches = re.findall('Revision Comment.*? \n.*?\n\n (.*?)\n', op ,re.DOTALL)
               #print matches
               if  matches :
                   print 'Fetching Comments for '+line
                   names = re.findall('Revision Comment by (.*?) on', op ,re.DOTALL)
                   renames = re.findall('Reply by (.*?) on', op ,re.DOTALL)
                   rematches = re.findall('Reply by .*?>(.*?)\n\n.*?', op ,re.DOTALL)
                   #print("\n".join(map(str, matches)))
                   #print matches
                   revdata = dict(zip(matches, names))
                   repdata = dict(zip(rematches, renames))
                   print revdata
                   print 
                   writer = csv.writer(open(rawdata+'.csv', 'ab'))
                   for (key, value), (key1, value1) in zip(revdata.items(), repdata.items()):
                       writer.writerow([line, key, value, key1, value1 ])
               else:
                    print 'No Comments found for '+line
           #print op
def findcomment():
     'Dummy module for crucible rest services'
     with open(sortdata, 'r') as f:
          for line in f:
           line = line.strip('\n')
           durl ='http://fisheye.com/rest-service/reviews-v1/'+line+'/comments/'
           print durl
           response = urllib2.urlopen(durl)
           op = response.read()
           print op
           matches = re.findall('<message>(.*?)</message>.*</replies>.*?</replies>' , op ,re.DOTALL)
           username = re.findall('<displayName>(.*?)</displayName>.*</replies>.*?</replies>' , op ,re.DOTALL)
           print matches
           print username

def findcsvcomment():
     with open(sortdata, 'r') as f:
         for line in f:
               line = line.strip('\n')
               #print line
               #durl ='http://fisheye.com/cru/'+line+'/reviewHistoryWrapper?content=details'
               durl ='http://fisheye.com/cru/'+line+'/reviewHistory'
               print durl
               try:
                   response = urllib2.urlopen(durl)
               except urllib2.HTTPError:
                   pass
               op = response.read()
               #print op
               #matches = re.findall('.*userorcommitter-parent.*? \n.*?\n\n (.*?)\n', op ,re.DOTALL)
               matches = re.findall('<a class="user  userorcommitter-parent".*<span class="linkText">(.*)</span></a>', op )
               if matches:
                   print(list(islice(matches, 3))[-2])
                   
               
               #comments = re.findall('<a class="user  userorcommitter-parent".*<span class="linkText.*</span></a>', op )
               print matches
def csvComment():
     'Module for data to be fetched and parsed into csv'
     print 'started'    
     with open(sortdata, 'r') as f:
         for line in f:
               line = line.strip('\n')
               durl='http://fisheyecom/cru/'+line+'/reviewHistory.csv'
               print durl
               testfile = urllib.URLopener()
               testfile.retrieve('http://fisheye.com/cru/'+line+'/reviewHistory.csv', line+'.csv')
               with open(line+'.csv') as f:
                    columns = defaultdict(list) # each value in each column is appended to a list
                    reader = csv.DictReader(f) # read rows into a dictionary format
                    for row in reader: # read a row as {column1: value1, column2: value2,...}
                        for (k,v) in row.items(): # go over each column name and value
                            columns[k].append(v) # append the value into the appropriate list

                    d = dict(zip(zip(columns['Date'],columns['User'],columns['New value']),columns['Action']))
                    print d
                    ##print rkdict
##                    for key, value in d.iteritems():
##                        if value == 'COMMENT_CHANGED' or value == 'COMMENT_ADDED':
##                            writer = csv.writer(open('final.csv', 'ab'))
##                            for (key, value)in zip(d.items()):
##                                       writer.writerow([line, key, value ])
##                        else:
##                            print 'No Comments found for '+line


def dictcsvFinalReview():
     print 'started'    
     with open(sortdata, 'r') as f:
         for line in f:
               line = line.strip('\n')
               durl='http://fisheye.cuc.com/cru/'+line+'/reviewHistory.csv'
               print durl
               testfile = urllib.URLopener()
               os.chdir(r'C:\Users\radhakrishnanr\Desktop\filescsv')
               testfile.retrieve('http://fisheye.com/cru/'+line+'/reviewHistory.csv', line+'.csv')
               columns = defaultdict(list) # each value in each column is appended to a list
               with open(line+'.csv') as f:
                    reader = csv.DictReader(f) # read rows into a dictionary format
                    for row in reader: # read a row as {column1: value1, column2: value2,...}
                        for (k,v) in row.items(): # go over each column name and value
                            columns[k].append(v) # append the value into the appropriate list
                                                 # based on column name k
                
               d = dict(zip(zip(columns['Date'],columns['User'],columns['New value']),columns['Action']))
               print d
            
##               for key, value in d.iteritems():
##                    if value == 'COMMENT_CHANGED' or value == 'COMMENT_ADDED':
##                        
##                        writer = csv.writer(open('final.csv', 'ab'))
##                        for (key, value) in zip(d,line):
##                            writer.writerow([line, key])
##                    else:
##                         print 'No Comments found for '+line

def cota():
               line='cr-4914'
               durl='http://fisheye.com/cru/cr-4/comments.txt'
               print durl
               response = urllib2.urlopen(durl)
               op = response.read()
               #print op
               matches = re.findall('Revision Comment.*? \n.*?\n\n (.*?)\n', op ,re.DOTALL)
               #print matches
               if  matches :
                   print 'Fetching Comments for '+line
                   names = re.findall('Revision Comment by (.*?) on', op ,re.DOTALL)
                   renames = re.findall('Reply by (.*?) on', op ,re.DOTALL)
                   rematches = re.findall('Reply by .*?>(.*?)\n\n.*?', op ,re.DOTALL)
                   #print("\n".join(map(str, matches)))
                   #print matches
                   revdata = dict(zip(matches, names))
                   repdata = dict(zip(rematches, renames))
##                   print revdata,repdata
                 
##                   writer = csv.writer(open(rawdata+'.csv', 'ab'))
                   for (key, value), (key1, value1) in zip(revdata.items(), repdata.items()):
                       print key +' - '+value
                       print ' Reply - '+key1 +' - '+value1
                       
##                       writer.writerow([line, key, value, key1, value1 ])
               else:
                    print 'No Comments found for '+line
def dota():
       'Dummy module for crucible rest services'
       line='cr-4914'
       durl ='http://fisheye.com/rest-service/reviews-v1/'+line+'/comments/'
       print durl
       response = urllib2.urlopen(durl)
       op = response.read()
       print op
       matches = re.findall('<message>(.*?)</message>.*</replies>.*?</replies>' , op ,re.DOTALL)
       username = re.findall('<displayName>(.*?)</displayName>.*</replies>.*?</replies>' , op ,re.DOTALL)
       print matches
       print username

def getcom():
     'Module for data to be fetched and parsed into csv'
     print 'started'
     final = open(rawdata+'-comments.txt', 'w')
     with open(sortdata, 'r') as f:
         for rid in f:
                rid = rid.strip('\n')
                cmurl='http://fisheye.com/cru/'+rid+'/comments.txt'
                rurl ='http://fisheye.com/rest-service/reviews-v1/'+rid+'/comments/'
                
                
                response = requests.get(rurl,
                                        headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                               '6.2; WOW64) AppleWebKit/'
                                                               '537.36 (KHTML, like '
                                                               'Gecko) Chrome/37.0.2062.'
                                                               '120 Safari/537.36'})
                soup = bs4.BeautifulSoup(response.content, "html.parser")
                                               
                tempfile=r'tmp/temp-'+rid+'.txt'
                wget.download(cmurl,tempfile)
                
                if soup.find_all(re.compile(r'message')):
                    print 'Fetching comments found for '+rid
                    
                    for tag in soup.find_all(re.compile(r'message')):
    ##                     tempfile='tmp/temp-'+rid+'.txt'
    ##                     wget.download(cmurl,tempfile)
                         
                         
                         with open(tempfile) as f:
                            
                             for num,line in enumerate(f, 1,):
                                 line=line.decode('utf-8')
                                 if tag.text in line:
                                     if line.startswith ('  >'):
                                         reply = linecache.getline(tempfile,num-1)
                                         final.write(rid+'|'+reply.strip()+'|'+line.strip()+'\n')
##                                         print rid+'##'+reply.strip()+'##'+line.strip()
                                         
                                         
                                     else:
                                         comment = linecache.getline(tempfile,num-3)
                                         final.write(rid+'|'+comment.strip()+'|'+line.strip()+'\n')
##                                         print rid+'##'+comment.strip()+'##'+line.strip()
                else:
                     print 'No comments found for '+rid

searchwrite(searchprint, rawdata)
removeDuplicate(dupdata)
getcom()

#dictcsvFinalReview()
'Removing logdata'
try:
    os.remove(sortdata)
    os.remove(dupdata)
    
except OSError:
    pass
