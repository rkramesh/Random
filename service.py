#ifdef VERSION1
# -*- coding: utf-8 -*-
import json
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import logging
from youtube_dl import YoutubeDL


class replacement_stderr(sys.stderr.__class__):
    def isatty(self): return False


sys.stderr.__class__ = replacement_stderr



def debug(content):
    log(content, xbmc.LOGDEBUG)


def notice(content):
    log(content, xbmc.LOGNOTICE)


def log(msg, level=xbmc.LOGNOTICE):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)


def showInfoNotification(message):
    xbmcgui.Dialog().notification("SendToKodi", message, xbmcgui.NOTIFICATION_INFO, 5000)


def showErrorNotification(message):
    xbmcgui.Dialog().notification("SendToKodi", message,
                                  xbmcgui.NOTIFICATION_ERROR, 5000)


# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])


def getParams():
    result = {}
    paramstring = sys.argv[2]
    additionalParamsIndex = paramstring.find(' ')
    if additionalParamsIndex == -1:
        result['url'] = paramstring[1:]
        result['ydlOpts'] = {}
    else:
        result['url'] = paramstring[1:additionalParamsIndex]
        additionalParamsString = paramstring[additionalParamsIndex:]
        additionalParams = json.loads(additionalParamsString)
        result['ydlOpts'] = additionalParams['ydlOpts']
    return result


def createListItemFromVideo(video):
    debug(video)
    url = video['url']
    thumbnail = video.get('thumbnail')
    title = video['title']
    list_item = xbmcgui.ListItem(title, path=url)
    list_item.setInfo(type='Video', infoLabels={'Title': title})

    if thumbnail is not None:
        list_item.setArt({'thumb': thumbnail})

    return list_item
   

ydl_opts = {
    'format': 'best'
}

params = getParams()
url = str(params['url'])
ydl_opts.update(params['ydlOpts'])
ydl = YoutubeDL(ydl_opts)
ydl.add_default_info_extractors()

with ydl:
    showInfoNotification("resolving stream(s) for " + url)
    result = ydl.extract_info(url, download=False)

if 'entries' in result:
    # Playlist
    pl = xbmc.PlayList(1)
    pl.clear()
    for video in result['entries']:
        list_item = createListItemFromVideo(video);
        xbmc.PlayList(1).add(list_item.getPath(), list_item)
    xbmc.Player().play(pl)
    showInfoNotification("playing playlist " + result['title'])
else:
    # Just a video, pass the item to the Kodi player.
    showInfoNotification("playing title " + result['title'])
    xbmcplugin.setResolvedUrl(__handle__, True, listitem=createListItemFromVideo(result))
#    xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.super.favourites/1mod_menuUtils.py,addfolder,{0},{1},{2}".format('addfolder',result['title'],result['url']))
#    xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.super.favourites/1mod_menuUtils.py,addfolder,{0},{1}".format(result['title'],result['url']))
#    xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.super.favourites/1mod_menuUtils.py,addfolder,'mahabalipuram','http.rockywinsnow')") 
#    xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.super.favourites/1mod_menuUtils.py,addfolder,"+result['title']+","+result['url']+")") 
    logging.warning("{0} {1} {2} {0}".format ('??'*15, 'result-url',url))
    try:
        if 'ww.xvi' in str(url):
            xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.super.favourites/1mod_menuUtils.py,addfolder,corrupt,"+result['title'].encode('ascii', 'ignore').decode('ascii')+","+result['url']+")") 
        else:
            xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.super.favourites/1mod_menuUtils.py,addfolder,MISC,"+result['title'].encode('ascii', 'ignore').decode('ascii')+","+result['url']+")") 
    except Exception, e:
        pass

#endif /* VERSION1 */
