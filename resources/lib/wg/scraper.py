'''
    ftvideos.scraper
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains some functions which do the website scraping for the
    API module. You shouldn't have to use this module directly.
'''
import re
import os
from urllib import unquote
from urllib2 import urlopen
from urlparse import urljoin, urlsplit
from BeautifulSoup import BeautifulSoup as BS

BASE_URLS = ["http://www.wowporngirls.com","http://www.wowgirlsblog.com"]
XXX_URL   = "http://www.wowporn.xxx"
def _urls(path):
    '''Returns a full url for the given path'''            
    return [urljoin(i, path) for i in BASE_URLS]


def get(url):
    '''Performs a GET request for the given url and returns the response'''
    conn = urlopen(url)
    resp = conn.read()
    conn.close()
    return resp


def _html(url):
    '''Downloads the resource at the given url and parses via BeautifulSoup'''
    return BS(get(url), convertEntities=BS.HTML_ENTITIES)
    
def get_tags(url):
    '''Returns a list of tags for the website.''' 

    # subjs will contain some duplicates so we will key on url
    items = []
    urls = set()

    for u in _urls(url):
        print "Opening", u
        html = _html(u)
        
        subjs = html.find("ul",  {'class':'wp-tag-cloud'}).findAll('li')

        for subj in subjs:
            lnk = subj.a
            _url = unquote(lnk['href'])
            if _url not in urls:
                urls.add(_url)
                items.append({
                    'name': "%s (%s)" % (lnk.text, urlsplit(u).netloc),
                    'url': _url,
                })

    return items


def get_girls(url):
    '''Returns a list of girls for the website. Each girl is a dict with
    keys of 'name' and 'url'.
    '''

    # subjs will contain some duplicates so we will key on url
    items = []
    urls = set()

    # first do the usual websites
    for u in _urls(url):
        print "Opening", u
        html = _html(u)

        subjs = html.findAll('li', {'class' :"border-radius-5 box-shadow"})

        for subj in subjs:
            _runtime = subj.find('div', {'class':"time-infos"}).text
            if not ":" in _runtime:
                continue

            lnk = subj.a
            _url = unquote(lnk['href'])
            if _url not in urls:
                urls.add(_url)
                items.append({
                    'name': lnk['title'], #get_girl_name(url),
                    'url': _url,
                    'thumbnail' : subj.img['src'],
                })

    #print items

    if "movies" in url:
        # now the other URL
        print "Opening", XXX_URL
        html = _html(XXX_URL)
        subjs = html.findAll('a', {'class':"clip-link"})
        
        for subj in subjs:
            _url = unquote(subj['href'])
            if _url not in urls:
                urls.add(_url)
                items.append({
                    'name': subj['title'], #get_girl_name(url),
                    'url': _url,
                    'thumbnail' : subj.img['src'],
                })    
    
    # filter out any items that didn't parse correctly
    return [item for item in items if item['name'] and item['url']]


def get_girl_metadata(girl_url):
    '''Returns metadata for a girl parsed from the given url'''
    #html = _html(make_showall_url(girl_url))
    html = _html(girl_url)
    name = get_girl_name(html)
    videos = get_videos(html)
    desc = get_girl_description(html)
    #age,height,figure = getBioStats(html)

    _info =  {
        'name': name,
        #'age' : age,
        #'height' : height,
        #'figure' : figure,
        'description' : desc,
        'videos'      : videos,
    }
    #print _info
    return _info


def get_girl_name(html):
    try:
        return html.find('meta', {'name':"keywords"})["content"].strip()
    except:
        return "Various"

def get_girl_description(html):
    if not XXX_URL in html.text:
        return html.find('div', {'class':"video-embed"}).find("p").text.strip()
    else:
        return html.find('meta', {'property':"og:description"})["content"]

def get_videos(html):
    nodes = html.findAll('h1', {'class': "border-radius-top-5"})

    items = [{
        'name' : html.find("span").text,
        #'url':  video_ptn.findall(node.__repr__())[0],
        #'icon': node.img['src'],
    } for node in nodes]

    xxx_ptn = re.compile('m4v:"(.+?mp4)",poster:"(.+?jpg)"')

    xxxnodes = xxx_ptn.findall(html.text)
    
    items += [{
        'name' : html.find("title").text,
        #'url'  : n[0],
        'icon' : n[1],
    } for n in xxxnodes]

    return items


def get_video_metadata(url):
    print "METADATA FOR", url
    html = _html(url)
    name = html.find("title").text #get_video_name(html)
    video_url = parse_video_url(html)
    thumb_url = parse_thumb_url(html)
    return {
        'name': name,
        'video_url': video_url,
        'thumbnail' : thumb_url,
        #'cast'      : get_cast(html),
    }
    


def parse_video_url(html):
    if not XXX_URL in html.text:
        return html.find('source', {'type':"video/mp4"})['src']
    else:
        xxx_ptn = re.compile('m4v:"(.+?mp4)"')
        return xxx_ptn.findall(html.text)[0]

def parse_thumb_url(html):
    if not XXX_URL in html.text:
        return html.find('meta', {'itemprop' : "image"})['content']
    else:
        xxx_ptn = re.compile('poster:"(.+?jpg)"')
        return xxx_ptn.findall(html.text)[0]