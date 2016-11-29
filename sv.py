import csv,os,urllib
import glob
from collections import defaultdict

def csvReview():
    os.chdir(r'C:\Users\yourloc\Desktop\filescsv')
    for file in glob.glob("*.csv"):
        columns = defaultdict(list) # each value in each column is appended to a list

        with open(file) as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value
                    columns[k].append(v) # append the value into the appropriate list
                                         # based on column name k
        ##            if columns['Action'] == 'COMMENT_CHANGED':
        ##                print columns['New value']
                      

        ##print(columns['Date'])
        ##print(columns['User'])
        ##print(columns['Action'])
        ##print(columns['New value'])
        ##print columns['New value']
        d = dict(zip(zip(columns['Date'],columns['User'],columns['New value']),columns['Action']))
        ##print rkdict
        for key, value in d.iteritems():
            if value == 'COMMENT_CHANGED' or value == 'COMMENT_ADDED':
                print file,key


def csvComment():
     'Module for data to be fetched and parsed into csv'
     print 'started'    
     with open('sorted.txt', 'r') as f:
         for line in f:
               line = line.strip('\n')
               durl='http://fisheye.com/cru/'+line+'/reviewHistory.csv'
               print durl
               testfile = urllib.URLopener()
               testfile.retrieve('http://fisheye.com/cru/'+line+'/reviewHistory.csv', line+'.csv')


def csvFinalReview():
     print 'started'    
     with open('sorted.txt', 'r') as f:
         for line in f:
               line = line.strip('\n')
               durl='http://fisheye.com/cru/'+line+'/reviewHistory.csv'
               print durl
               testfile = urllib.URLopener()
               testfile.retrieve('http://fisheye.com/cru/'+line+'/reviewHistory.csv', line+'.csv')
               columns = defaultdict(list) # each value in each column is appended to a list
               with open(line+'.csv') as f:
                    reader = csv.DictReader(f) # read rows into a dictionary format
                    for row in reader: # read a row as {column1: value1, column2: value2,...}
                        for (k,v) in row.items(): # go over each column name and value
                            columns[k].append(v) # append the value into the appropriate list
                                                 # based on column name k
                
               d = dict(zip(zip(columns['Date'],columns['User'],columns['New value']),columns['Action']))
               for key, value in d.iteritems():
                    if value == 'COMMENT_CHANGED' or value == 'COMMENT_ADDED':
                        print file,key
                        try:
                            os.remove(line+'.csv')
                        except IOError:
                            pass
                        
                        
    

    
               

#csvComment()
#csvReview()
csvFinalReview()
            
