#!/usr/bin/env python

# get_links.py

import re
import sys
import urllib
import urlparse
from bs4 import BeautifulSoup
from os.path import basename

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

def process(url):
    myopener = MyOpener()
    #page = urllib.urlopen(url)
    page = myopener.open(url)

    text = page.read()
    page.close()

    soup = BeautifulSoup(text, "html.parser")
    rk=[]
    VIDEOS={}
    for tag in soup.findAll('a', href=True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
        
##        rk.append(tag['href'])
        rk.append({'name': basename(tag['href']),
                       'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg',
                       'video': tag['href'] ,
                       'genre': '2017'})

        
        
    VIDEOS['2017']=rk
    print VIDEOS
        
        
# process(url)

def main(url):
        process(url)
# main()

if __name__ == "__main__":
    main('http://www.stocktonsda.org/Videos/2017')
