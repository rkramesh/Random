#!/usr/bin/python
import base64
import hashlib
import time
jctBase = "cutibeau2ic"
ssoToken = "AQIC5wM2LY4SfczEZE2fGevb0t17TAm-G9kAMvxhtxL4oGU.*AAJTSQACMDIAAlNLABQtMTkwNjA5MTA1OTI5NDc0NTI1MgACUzEAAjQ4*"

sample='http://mumsite.cdnsrv.jio.com/jiotv.live.cdn.jio.com/Zee_Salaam/Zee_Salaam_1200.m3u8?jct=ZgUCpa78weI1Mud0F480NQ&pxe=1560770528&st=2rABpyTLSDzkoYSlKcWJhg|user-agent="AppleWebKit/JioTV/537.36"'

sample='http://gdcsite.cdnsrv.jio.com/jiotv.live.cdn.jio.com/Sahana_Music/Sahana_Music_1200.m3u8?jct=fGkvWUrs1dQJsUtRSg3bDg&pxe=1563559536&st=nsV2-53QXSLtevfjGhkkYQ|user-agent="Mozilla/5.0 (Mobile; LYF/F90M/LYF-F90M-000-02-17-270917; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.0"'

cdn="http://gdcsite.cdnsrv.jio.com/jiotv.live.cdn.jio.com"

jct="fGkvWUrs1dQJsUtRSg3bDg&pxe=1563559536&st=nsV2-53QXSLtevfjGhkkYQ"

UA="Mozilla/5.0 (Mobile; LYF/F90M/LYF-F90M-000-02-17-270917; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.0"



#raw_data='All_channels_2'
raw_data='tamil_list'
#raw_data='all_list'

def tokenFormat(ssoToken):
    return base64.b64encode(hashlib.md5(ssoToken).digest()).replace('+', '-').replace('/', '_').replace('=', '').replace("\n", "").replace("\r", "")
    


def generateSt():
    return tokenFormat(ssoToken)


def generatePxe():
    return  int(time.time())+ int(60000)

def generateJct(st,pxe):    
    return tokenFormat('{}{}{}'.format(jctBase,st,pxe))
    
  
def generateToken():
    st  = generateSt()
    pxe = generatePxe()
    jct = generateJct(st, pxe)
    return '%s&pxe=%s&st=%s'%(jct,pxe,st)

def write_m3u():
    with open(raw_data) as fp:
        line = fp.readline()
        cnt = 1
        #print("Line {}: {}".format(cnt, line.strip))
        #f = open(raw_data+'.m3u',"wb")
        #f.write('#EXTM3U' + '\n')
        while line:
            if line.startswith('#EXT'):
                #f.write(line + '\n')
                 pass
            elif line.find('.m3u8'):
                    print("Line:{} {}/{}?jct={}|user-agent='{}'".format(cnt, cdn, '/'.join(line.split('?')[0].split('/')[-2:]).strip(), generateToken().strip(), UA ))
                    #f.write("{}/{}?jct={}|user-agent='{}'".format(cdn, '/'.join(line.split('?')[0].split('/')[-2:]), jct, UA ) + '\n')
            line = fp.readline()
            cnt += 1


def write_file_m3u():
    with open(raw_data) as fp:
        line = fp.readline()
        cnt = 1
        #print("Line {}: {}".format(cnt, line.strip))
        f = open(raw_data+'.m3u',"wb")
        f.write('#EXTM3U' + '\n')
        while line:
            if line.startswith('#EXT'):
                pass
                #f.write(line + '\n')
            elif line.find('.m3u8'):
                f.write('#EXTINF:-1, group-title="All", '+line+'\n')
                #print("Line:{} {}/{}?jct={}|user-agent='{}'".format(cnt, cdn, line.strip(), jct, UA ))
                f.write("{}/{}?jct={}|user-agent='{}'".format(cdn, line.strip(), jct, UA ) + '\n')
                    #f.write("{}/{}?jct={}|user-agent='{}'".format(cdn, '/'.join(line.split('?')[0].split('/')[-2:]), jct, UA ) + '\n')
            line = fp.readline()
            cnt += 1

write_m3u()
#write_file_m3u()



