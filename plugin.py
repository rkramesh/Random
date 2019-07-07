# -*- coding: utf-8 -*-
import hashlib
import hmac
import logging
import random
import re
import requests
import sys
import time
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from datetime import datetime
from urllib import quote
from urllib import urlencode
from urlparse import ParseResult
from urlparse import parse_qsl
from urlparse import urlparse

from . import kodilogging

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config(logger)

#
# Globals
#
# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

session = requests.Session()
_country_code = 'IN'


def _hotstarauth_key():
    def keygen(t):
        e = ""
        n = 0
        while len(t) > n:
            r = t[n] + t[n + 1]
            o = int(re.sub(r"[^a-f0-9]", "", r + "", re.IGNORECASE), 16)
            e += chr(o)
            n += 2

        return e

    start = int(time.time())
    expiry = start + 6000
    message = "st={}~exp={}~acl=/*".format(start, expiry)
    secret = keygen("05fc1a01cac94bc412fc53120775f9ee")
    signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
    return '{}~hmac={}'.format(message, signature)


_auth = _hotstarauth_key()

_GET_HEADERS = {
    "Origin": "https://ca.hotstar.com",
    "hotstarauth": _auth,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    "x-country-code": "IN",
    "x-client-code": "LR",
    "x-platform-code": "PCTV",
    "Accept": "*/*",
    "Referer": "https://ca.hotstar.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "x-dst-drm": "DASH/WIDEVINE",
}


def make_request(url):
    try:
        logger.info("Making request: {}, country_code: {}".format(url, _country_code))
        headers = _GET_HEADERS
        if _country_code is not None:
            headers['x-country-code'] = _country_code
        #url='https://api.hotstar.com/h/v2/play/in/contents/1000237823?desiredConfig=encryption:widevine;ladder:phone;package:dash&client=mweb&clientVersion=6.27.0&deviceId=ccc64339-0655-4b4e-952e-a7429670b84f&osName=Mac%20OS&osVersion=10.14.4'

        #response = session.get(url, headers=headers, cookies=session.cookies)
        response = session.get(url+'?desiredConfig=encryption:widevine;ladderr:phone;package:dash&client=mweb&clientVersion=6.27.0&deviceId=ccc64339-0655-4b4e-952e-a7429670b84f&osName=Mac%20OS&osVersion=10.14.4', headers=headers, cookies=session.cookies)
        data = response.json()
        logger.info("######: {}, log: {}########".format(data, url))
        if data.get('statusCodeValue') == 200:
            return data

        elif _country_code == 'IN':
            global _country_code
            _country_code = 'CA'

            logger.debug('Falling back to CA country code for getting the data for {}'.format(url))
            return make_request(url)

        else:
            raise Exception('Failed to fetch data for API!', url)

    except (urllib2.URLError, Exception) as e:
        logger.error("Failed to service request: {} -- {}".format(url, str(e)))


def _items(results):
    if 'assets' in results:
        return results['assets']['items']
    else:
        return results['items']


def _next_page(results):
    assets = results['assets'] if 'assets' in results else results
    return assets['nextOffsetURL'] if 'nextOffsetURL' in assets else None


def list_program_details(title, uri):
    if not uri:
        return

    if '?' in uri:
        base_url, param_string = uri.split('?')
        params = dict(parse_qsl(param_string))
        if 'tas' in params and int(params['tas']) < 30:
            params['tas'] = 30
        uri = '{}?{}'.format(base_url, urlencode(params))

    data = make_request(uri)
    program = data['body']['results'].get('item')

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, title)

    for item in data['body']['results']['trays']['items']:
        # {
        #   "title": "Episodes",
        #   "uri": "https://api.hotstar.com/o/v1/tray/g/1/detail?eid=1101&etid=2&tao=0&tas=20",
        #   "traySource": "CATALOG",
        #   "layoutType": "HORIZONTAL",
        #   "trayTypeId": 7002,
        #   "traySourceId": 100,
        #   "uqId": "1_2_1101"
        # },
        assets = item.get('assets')
        if not item.get('uri') or not (assets and assets.get('totalResults', 0)):
            continue

        asset_item = {}
        try:
            asset_item = assets['items'][0]
        except Exception:
            pass

        item_title = item['title']
        content_id = program['contentId'] if program else asset_item.get('contentId')
        description = program['description'] if program else asset_item.get('description')
        genre = program.get('genre') if program else asset_item.get('genre')

        asset_type = asset_item.get('assetType')
        if asset_type in ['SEASON']:
            action = 'seasons'

        elif asset_type in ['SHOW']:
            action = 'programs'

        elif asset_type in ['CHANNEL']:
            action = 'channels'

        else:
            action = 'episodes'

        _add_directory_item(
            parent_title=title,
            title=item_title,
            content_id=content_id,
            genre=genre,
            description=description,
            uri=item['uri'],
            action=action,
            image=get_thumbnail_image(asset_item) if asset_item else None
        )

    # Add Search.
    _add_search_item()

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def _get_data(url):
    data = make_request(url)
    return {
        'items': _items(data['body']['results']),
        'nextPage': _next_page(data['body']['results'])
    }


def list_seasons(title, url):
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, title)
    # Get the list of videos in the category.
    result = _get_data(url)

    # Iterate through videos.
    for season in result['items']:
        # {
        #     "title": "Chapter 23",
        #     "categoryId": 2433,
        #     "contentId": 2482,
        #     "uri": "https://api.hotstar.com/o/v1/season/detail?id=1481&avsCategoryId=2433&offset=0&size=5",
        #     "assetType": "SEASON",
        #     "episodeCnt": 86,
        #     "seasonNo": 23,
        #     "showName": "Neeya Naana",
        #     "showId": 80,
        #     "showShortTitle": "Neeya Naana"
        # },

        base_url, param_string = season['uri'].split('?')
        params = dict(parse_qsl(param_string))
        params['size'] = 30
        season_uri = '{}?{}'.format(base_url, urlencode(params))

        _add_directory_item(
            title=season['title'],
            content_id=season['contentId'],
            description=season.get('description', season['title']),
            uri=season_uri,
            action='episodes',
            parent_title=title,
            image=get_thumbnail_image(season)
        )

    _add_next_page_and_search_item(result['nextPage'], 'seasons', title)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def _add_video_item(video):
    #logger.info("######: {}, log: {}########".format('rk4', video))
    # Create a list item with a text label and a thumbnail image.
    episode_no = video.get('episodeNo')
    title = u'Episode {}: {}'.format(
        episode_no, video['title']
    ) if episode_no else video['title']
    list_item = xbmcgui.ListItem(label=title)

    # Set additional info for the list item.
    # 'mediatype' is needed for skin to display info for this ListItem correctly.
    episode_date = video.get('broadCastDate') or video.get('startDate')
    asset_type = video.get('assetType') or video.get('contentType')
    if asset_type != 'MOVIE' and episode_date:
        title = u'{} | {}'.format(datetime.fromtimestamp(episode_date).strftime('%b %d'), title)

    list_item.setInfo('video', {
        'title': title,
        'genre': video.get('genre'),
        'episode': episode_no,
        'season': video.get('seasonNo'),
        'plot': video.get('description'),
        'duration': video.get('duration'),
        'year': video.get('year', datetime.fromtimestamp(episode_date).year if episode_date else None),
        'date': datetime.fromtimestamp(episode_date).strftime('%d.%m.%Y') if episode_date else None,
        'mediatype': 'video',
    })

    # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
    # Here we use the same image for all items for simplicity's sake.
    image = get_thumbnail_image(video)
    list_item.setArt({
        'thumb': image,
        'icon': image,
        'fanart': image,
    })

    # Set 'IsPlayable' property to 'true'.
    # This is mandatory for playable items!
    list_item.setProperty('IsPlayable', 'true')

    # Create a URL for a plugin recursive call.
    # Example: plugin://plugin.video.example/?action=play&video=http:
    # //www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
    url = get_url(action='play', uri=video.get('playbackUri'))

    # Add the list item to a virtual Kodi folder.
    # is_folder = False means that this item won't open any sub-list.
    is_folder = False

    # Add our item to the Kodi virtual folder listing.
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


def list_episodes(title, uri):
    """
    Create the list of playable videos in the Kodi interface.
    """

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, title)

    # Get the list of videos in the category.
    result = _get_data(uri)
    # Iterate through videos.
    #logger.info("######: {}, log: {}########".format('rk1', result['items']))
    for video in result['items']:
        # {
        #     "title": "Sakthi returns to India",
        #     "contentId": 1000036012,
        #     "uri": "https://api.hotstar.com/o/v1/episode/detail?id=80096&contentId=
        #     1000036012&offset=0&size=20&tao=0&tas=5",
        #     "description": "Saravanana and Meenakshi's oldest son, Sakthi, returns to
        #     India 25 years after his parents had left it. He wants to search for a bride,",
        #     "duration": 1332,
        #     "contentType": "EPISODE",
        #     "contentProvider": "Global Villagers",
        #     "cpDisplayName": "Global Villagers",
        #     "assetType": "EPISODE",
        #     "genre": [
        #         "Family"
        #     ],
        #     "lang": [
        #         "Tamil"
        #     ],
        #     "channelName": "Star Vijay",
        #     "seasonNo": 1,
        #     "episodeNo": 520,
        #     "premium": false,
        #     "live": false,
        #     "hboContent": false,
        #     "encrypted": false,
        #     "startDate": 1416649260,
        #     "endDate": 4127812200,
        #     "broadCastDate": 1382367600,
        #     "showName": "Saravanan Meenatchi",
        #     "showId": 99,
        #     "showShortTitle": "Saravanan Meenatchi",
        #     "seasonName": "Chapter 1",
        #     "playbackUri": "https://api.hotstar.com/h/v1/play?contentId=1000036012",
        #     "contentDownloadable": false
        # },
        _add_video_item(video)
        #logger.info("######: {}, log: {}########".format('rk2', video))

    _add_next_page_and_search_item(result['nextPage'], 'episodes', title)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def get_image_url(content_id, images=None, hs_field='hs', image_size="web_hs_3x"):
    def get_image_url_akamai():
        if not content_id:
            return

        _image_size = "" if 'web_' not in image_size else "t_" + image_size + "/"
        _hs_field = 'hcdl' if hs_field == 'hs' else hs_field

        content_id_minified = str(content_id)[-2:]
        if len(content_id_minified) == 1:
            content_id_minified = "0{}".format(content_id_minified)

        return "https://secure-media{shard}.hotstar.com/{imageSize}r1/thumbs/PCTV/{contentIdMinified}/{contentId}/PCTV-{contentId}-{hsField}.jpg".format(
            shard=random.randint(0, 3),
            imageSize=_image_size,
            contentIdMinified=content_id_minified,
            contentId=content_id,
            hsField=_hs_field
        )

    def get_image_url_cms():
        _hs_field = {"hc1": "m", "vl": "v"}.get(hs_field, "h")
        source = images.get(_hs_field) or images.get(_hs_field.upper())
        if source is None:
            return get_image_url_akamai()

        return "https://img{shard}.hotstar.com/image/upload/f_auto,t_{imageSize}/{source}".format(
            shard=random.randint(0, 3),
            imageSize=image_size,
            source=source
        )

    if images:
        return get_image_url_cms()
    else:
        return get_image_url_akamai()


def get_thumbnail_image(item):
    return get_image_url(
        content_id=item.get('imgContentId') or item.get('contentId') or item.get('contain_id'),
        images=item.get('images'),
    )


def _add_next_page_and_search_item(uri, action, original_title):
    if uri:
        title = '| Next Page >>>'
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {
            'mediatype': 'video'
        })

        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action=action, uri=uri, title=original_title)

        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True

        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Add Search item.
    _add_search_item()


def _add_directory_item(
    title,
    description,
    content_id,
    action,
    image=None,
    genre=None,
    uri='',
    parent_title='',
    country_code=None,
):
    # Create a list item with a text label and a thumbnail image.
    list_item = xbmcgui.ListItem(label=title)

    # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
    # Here we use the same image for all items for simplicity's sake.
    # In a real-life plugin you need to set each image accordingly.
    if image:
        list_item.setArt({
            'thumb': image,
            'icon': image,
            'fanart': image
        })

    # Set additional info for the list item.
    # Here we use a category name for both properties for for simplicity's sake.
    # setInfo allows to set various information for an item.
    # For available properties see the following link:
    # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
    # 'mediatype' is needed for a skin to display info for this ListItem correctly.
    list_item.setInfo('video', {
        'count': content_id,
        'title': title,
        'genre': genre,
        'plot': description,
        'mediatype': 'video'
    })

    # Create a URL for a plugin recursive call.
    # Example: plugin://plugin.video.example/?action=listing&category=Animals
    url = get_url(
        action=action,
        uri=uri,
        title=u'{}/{}'.format(parent_title, title) if parent_title else title,
        country_code=country_code if country_code else _country_code
    )

    # is_folder = True means that this item opens a sub-list of lower level items.
    is_folder = True

    # Add our item to the Kodi virtual folder listing.
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


def list_programs(channel_name, uri):
    """
    List the programs under each channel.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, channel_name)
    # Get the list of videos in the category.
    result = _get_data(uri)
    # Iterate through videos.
    #logger.info("######: {}, log: {}########".format('rk', result['items']))
    for program in result['items']:
        # {
        #     "title": "Raja Rani",
        #     "categoryId": 14064,
        #     "contentId": 14230,
        #     "uri": "https://api.hotstar.com/o/v1/show/detail?id=
        #     1101&avsCategoryId=14064&contentId=14230&offset=0&size=20&tao=0&tas=5",
        #     "description": "Due to certain circumstances, Karthik marries the maid of his family,",
        #     "assetType": "SHOW",
        #     "genre": [
        #         "Family"
        #     ],
        #     "lang": [
        #         "Tamil"
        #     ],
        #     "channelName": "Star Vijay",
        #     "episodeCnt": 407,
        #     "premium": false
        # },
        _add_directory_item(
            parent_title=channel_name,
            title=program['title'],
            content_id=program['contentId'],
            genre=program.get('genre') or program['title'],
            description=program.get('description'),
            uri=program['uri'],
            action='programs' if program.get('assetType') == 'GENRE' else 'program_details',
            image=get_thumbnail_image(program)
        )

    _add_next_page_and_search_item(result['nextPage'], 'programs', channel_name)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_channels(title=None, uri=None):
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Channels')

    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content -- didn't use this since it's not working well
    # with the video item.
    # xbmcplugin.setContent(_handle, 'videos')

    # Get channels.
    result = _get_data(uri or 'https://api.hotstar.com/o/v1/channel/list?perPage=1000')
    # Iterate through categories

    for channel in result['items']:
        # Channel JSON structure.
        # {
        #     "title": "Star Vijay",
        #     "categoryId": 748,
        #     "contentId": 824,
        #     "uri": "https://api.hotstar.com/o/v1/channel/detail?id=12&avsCategoryId=748&contentId=824&offset=0&size=20
        #     &pageNo=1&perPage=20",
        #     "description": "A Tamil general entertainment channel with family drama, comedy and reality shows.",
        #     "assetType": "CHANNEL",
        #     "genre": [
        #         "LiveTV"
        #     ],
        #     "lang": [
        #         "Tamil"
        #     ],
        #     "showCnt": 137
        # },
        #
        _add_directory_item(
            parent_title=title,
            title=channel['title'],
            content_id=channel['contentId'],
            genre=channel.get('genre'),
            description=channel['description'],
            uri=channel['uri'],
            action='programs',
            image=get_thumbnail_image(channel)
        )

    if not uri:
        # Add Sports
        _add_directory_item(
            title='HotStar Sports',
            description='Sports',
            content_id=821,
            genre='Sports',
            uri='https://api.hotstar.com/o/v1/page/1327?tas=30',
            action='program_details',
            country_code='CA'
        )
        # Movies
        _add_directory_item(
            title='HotStar Movies',
            content_id=821,
            genre='Movies',
            description='Movies',
            uri='https://api.hotstar.com/o/v1/page/1328?tas=30',
            action='program_details',
            country_code='CA'
        )

        # TV
        _add_directory_item(
            title='HotStar TV',
            content_id=821,
            description='TV',
            genre='TV',
            uri='https://api.hotstar.com/o/v1/page/1329?tas=30',
            action='program_details',
            country_code='CA'
        )

        # Genre
        _add_directory_item(
            title='HotStar Genres',
            content_id=821,
            description='Genres',
            genre='Genre',
            uri='https://api.hotstar.com/o/v1/genre/list?perPage=1000',
            action='programs',
        )

    _add_search_item()

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    valid_kwargs = {key: value.encode('utf-8') for key, value in kwargs.iteritems() if value is not None}
    return u'{0}?{1}'.format(_url, urlencode(valid_kwargs))


def play_video(path):
    #original=https://api.hotstar.com/h/v1/play?contentId=1000238814
    path="https://api.hotstar.com/h/v2/play/in/contents/1000238814"
    """
    Play a video by the provided path.
        #logger.info("######: {}, log: {}########".format('rk2', video))

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    data = make_request(path)
    logger.info("######: {}, log: {}########".format('rk3', path))
    if not data:
        return

    def get_subtitle(url):
        #
        # https://hses.akamaized.net/videos/hotstarint/hostages/1260003409/1558430241469/
        # 265b9dab22d4e9a033e6df6f89639f17/master.m3u8?hdnea=st=1560107863~exp=1560111463~acl=
        # /*~hmac=2f6fb393159ed5fa1b12bbf12e954eb377cfa0fc852d4ff5eb24446233237620
        #
        # https://hses.akamaized.net/videos/hotstarint/hostages/1260003409/1558430241469/
        # 5d0f83c3ccbf4501cf952bdfc8c0d785/subtitle/lang_en/sub-0.vtt
        #
        _url = urlparse(url)
        values = _url._asdict()
        values['query'] = ''
        values['path'] = '{}/subtitle/lang_en/sub-0.vtt'.format("/".join(values['path'].split('/')[:-1]))

        subtitle_url = ParseResult(**values).geturl()
        # subtitle_file = kodiutils.download_url_content_to_temp(subtitle_url, '{}-{}.srt'.format(
        #     Zee5Plugin.safe_string(item['title']),
        #     subtitle_lang,
        # ))

        return subtitle_url

    logger.info("######: {}, log: {}########".format('rk6', data))
    #item = data['body']['results']['item']
    item=data['body']['results']['playBackSets'][0]
    path = item['playbackUrl']
    licenseURL = item.get('licenseUrl')
    subtitle = get_subtitle(path)

    logger.info('Playing video URL: {}, licenseURL: {}, subtitle: {}'.format(path, licenseURL, subtitle))

    play_item = xbmcgui.ListItem(path=path)
    if licenseURL:
        play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        play_item.setMimeType('application/dash+xml')
        play_item.setContentLookup(False)

    play_item.setSubtitles([get_subtitle(path)])

    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def get_user_input():
    kb = xbmc.Keyboard('', 'Search for Movies/TV Shows/Trailers/Videos in all languages')
    kb.doModal()  # Onscreen keyboard appears
    if not kb.isConfirmed():
        return

    # User input
    return kb.getText()


def _add_search_item():
    _add_directory_item(
        title='| Search', content_id=1, description='Search', action='search'
    )


def list_search():
    query = get_user_input()
    if not query:
        return []

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Search/{}'.format(query))

    url = 'https://api.hotstar.com/s/v1/scout?q={}&perPage=10'.format(quote(query))
    data = make_request(url)
    for item in data['body']['results']['items']:
        asset_type = item.get('assetType')
        if asset_type in ['CHANNEL', 'SHOW']:
            _add_directory_item(
                parent_title='Search/{}'.format(query),
                title=item['title'],
                content_id=item['contentId'],
                genre=item.get('genre'),
                description=item['description'],
                uri=item['uri'],
                action='programs' if asset_type == 'CHANNEL' else 'program_details',
                image=get_thumbnail_image(item)
            )

        elif asset_type in ['MOVIE', 'VIDEO']:
            _add_video_item(item)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    logger.info('Handling route params -- {}'.format(params))
    if params:
        title = params.get('title')
        uri = params.get('uri', None)
        action = params['action']
        country_code = params.get('country_code', None)
        global _country_code
        if country_code:
            _country_code = country_code

        if action == 'programs':
            list_programs(title, uri)

        elif action == 'program_details':
            list_program_details(title, uri)

        elif action == 'episodes':
            list_episodes(title, uri)

        elif action == 'seasons':
            list_seasons(title, uri)

        elif action == 'play':
            # Play a video from a provided URL.
            play_video(uri)

        elif action == 'search':
            list_search()

        elif action == 'channels':
            list_channels(title, uri)

        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))

    else:
        # List all the channels at the base level.
        list_channels()


def run():
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
