#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import simplejson as json

AUTHOR = u'Eric Peden'
SITENAME = u'I Get You More Juice'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
DEFAULT_DATE = 'fs'

RECIPE_URL = 'recipes/{slug}.json'
RECIPE_SAVE_AS = RECIPE_URL

RECIPE_DIR = 'recipes'
ARTICLE_EXCLUDES = ('pages', 'recipes',)

EXTRA_TEMPLATES_PATHS = ('templates',)

JINJA_FILTERS = {
    'tojson': json.dumps,
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('/r/ecig', '...'),
          ('Tasty Vapor', 'http://tastyvapor.us/'),
          ('Wizard Labs', ''),
          ('RTS Vapes', ''),
          ('Pelican', 'http://getpelican.com/'),
	 )

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 25

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGINS = ["getumorejuice"]