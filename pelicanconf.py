#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Matt Hamilton'
SITENAME = u'Quernus'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/hammertoe'),
          ('linkedin', 'https://www.linkedin.com/in/matthamilton77'),
          ('slideshare', 'https://www.slideshare.net/hammertoe'),
          ('github', 'https://github.com/hammertoe'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PROFILE_IMG_URL = '/theme/matt_head_bucharest.jpg'
#COVER_IMG_URL = '/theme/oak_tree_medium.png'

TAGLINE = 'Matt Hamilton. An Internet technologist, interested in Python web development, iOS deployment and testing, wearables, networking and operating systems.'

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
MENUITEMS = (('Home', '/'),
             ('Talks', '/category/talks.html'),
             ('Archives', '/archives.html'),
             ('Tags', '/tags.html'),
)
THEME = 'pure-single'

FAVICON_URL = '/theme/favicon.ico'

GOOGLE_ANALYTICS = 'UA-65654046-1'
DISQUS_SITENAME = 'quernus'

DEFAULT_CATEGORY = 'blog'

STATIC_PATHS = ['public']
