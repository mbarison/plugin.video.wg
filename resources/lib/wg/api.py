'''

    wowgirls.api
    ~~~~~~~~~~~~~~~~~

    This module contains the API classes and method to parse information from
    the WowGirls and WowPorn websites.

'''
from scraper import (get_girls, get_videos, get_girl_metadata,
                     get_video_metadata)
from datetime import datetime
import re


class WowGirls(object):
    '''The main API object. Useful as a starting point to get available
    girls.
    '''

    def __init__(self):
        pass

    def get_girls(self,url):
        '''Returns a list of girls available on the website.'''

        return [Girl(**info) for info in get_girls(url)]


class Girl(object):
    '''Object representing a FTV model.'''

    def __init__(self, url, name=None, thumbnail=None):
        self.url = url
        self._name = name
        self._videos = None
        self._loaded = False
        self._thumbnail = thumbnail
        self._description = None
        self._date = None

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Girl '%s'>" % self.name

    def _load_metadata(self):
        resp = get_girl_metadata(self.url)
        if not self._name:
            self._name = resp['name']
        self._videos = [Video(self.url, **info) for info in resp['videos']]
        self._description = resp['description']
        self._loaded = True

        #ptn = re.compile("wp-content/uploads/([0-9]{4}/[0-9]{2})/")
        #_dt = ptn.findall(self._thumbnail)[0]
        #self._date = datetime.strptime(_dt, "%Y/%m")

    @property
    def name(self):
        '''Girl name'''
        if not self._name:
            self._load_metadata()
        return self._name
        
    @property
    def videos(self):
        '''List of videos available for this girl'''
        if not self._loaded:
            self._load_metadata()
        return self._videos

    @property
    def thumbnail(self):
        return self._thumbnail

    @property
    def date(self):
        return self._date

    @property
    def description(self):
        if not self._loaded:
            self._load_metadata()
        return self._description



class Video(object):

    def __init__(self, url, name=None, **kwargs):
        self.url = url
        self._name = name
        self._loaded = False
        self._video_url = None
        self._thumbnail = None
        self._cast      = []

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Video '%s'>" % self.name

    def _load_metadata(self):
        resp = get_video_metadata(self.url)
        if not self._name:
            self._name = resp['name']
        self._video_url = resp['video_url']
        self._thumbnail = resp['thumbnail']
        #self._cast      = resp['cast']
        self._loaded = True

    @property
    def name(self):
        if not self._name:
            self._load_metadata()
        return self._name

    @property
    def video_url(self):
        if not self._loaded:
            self._load_metadata()
        return self._video_url

    @property
    def thumbnail(self):
        if not self._loaded:
            self._load_metadata()
        return self._thumbnail

    @property
    def cast(self):
        if not self._loaded:
            self._load_metadata()
        return self._cast
