#!/usr/bin/python
import os
import re
import urllib2
import csv
import xmltodict
searchprint = '(CR-\d+.*?)'
rawdata = 'changeset - Copy.csv'
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
               durl='http://fisheye.com/'+line+'/comments.txt'
               
               
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
                   writer = csv.writer(open('dict.csv', 'ab'))
                   for (key, value), (key1, value1) in zip(revdata.items(), repdata.items()):
                       writer.writerow([line, key, value, key1, value1 ])
               else:
                    print 'No Comments found for '+line
           #print op
def findcomment(sortdata):
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
           
searchwrite(searchprint, rawdata)
removeDuplicate(dupdata)
finddata()
'Removing logdata'
try:
    os.remove(sortdata)
    os.remove(dupdata)
except OSError:
    pass
