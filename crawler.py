# -*- coding: utf-8 -*-

import ConfigParser
import os
import urllib2
import requests
import hashlib
import urllib
import lxml.html as HTML

# config the objects you want to get
category = ["book", "bird"]

# read the config file
cf = ConfigParser.ConfigParser()
cf.read("config")

category = ["book"]
img_num = cf.getint("db", "img_num")
threads = cf.getint("db", "threads")
save = cf.get("db", "save")

# get the url
session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
for item in category:
    url = "http://rvc.ust.hk/mgmt/media.aspx?path=16FA_CSIT5210-L1_160922_44793"
    req = session.get(url, headers=headers)
    print req.text
