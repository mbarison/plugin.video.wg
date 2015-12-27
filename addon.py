from xbmcswift2 import Plugin
from operator import itemgetter

from resources.lib.wg.api import WowGirls, Girl, Video

import subprocess, platform

plugin = Plugin()
api = WowGirls()

@plugin.route('/')
def main_menu():
    items = [{'label': 'Show Movies', 'path': plugin.url_for('show_galleries',url='category/movies')},
          {'label': 'Show Trailers', 'path': plugin.url_for('show_galleries',url='category/trailers')},
          {'label': 'Show Tags', 'path': plugin.url_for('show_tags',url='tags')},
          ]
    return items

@plugin.route('/tags/<url>')
def show_tags(url):
    tags = api.get_tags(url)

    print "TAGS", len(tags)

    items = [{
        'label': tag.name,
        'path': plugin.url_for('show_galleries', url=tag.url),
    } for tag in tags]
    
    print "ITEMS", len(items)
   
    print items

    sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items

@plugin.route('/<url>')
def show_galleries(url):
    girls = api.get_girls(url)

    print "GIRLS", len(girls)

    items = [{
        'label': girl.name,
        'path': plugin.url_for('show_girl_info', url=girl.url),
        'thumbnail' : girl.thumbnail,
        #'info' : {"Plot" : girl.description},
    } for girl in girls]

    #items.insert(0, {'label' : "Previous Girls",
    #               'path'  : plugin.url_for('show_girls',url=[1,pagecount-1][pagecount>1])})
    #items.insert(1, {'label' : "Next Girls",
    #               'path'  : plugin.url_for('show_girls',url=pagecount+1)})
    
    print "ITEMS", len(items)
   
    return items


@plugin.route('/girl/<url>/')
def show_girl_info(url):
    girl = Girl.from_url(url)

    videos = [{
        'label': video.name,
        'path': plugin.url_for('play_video', url=url),
        'is_playable': True,
        'thumbnail' : girl.thumbnail,
        'icon'      : girl.thumbnail,
        'info' : {"Plot" : girl.description},
    } for video in girl.videos]

    by_label = itemgetter('label')
    sorted_items = sorted(videos, key=by_label)
    return sorted_items


@plugin.route('/videos/<url>/')
def play_video(url):
    video = Video.from_url(url)
    url = video.video_url
    plugin.log.info('Playing url: %s' % url)
    plugin.set_resolved_url(url)
    if platform.machine() == 'x86_64':
        subprocess.call(["vlc",url])

if __name__ == '__main__':
    plugin.run()
