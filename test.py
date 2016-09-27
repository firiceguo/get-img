# -*- coding: utf-8 -*-
import ConfigParser

# load config file
cf = ConfigParser.ConfigParser()
cf.read("config")
category = cf.get("db", "category").split(',')
save = cf.get("db", "save")
img_num = cf.getint("db", "img_num")
threads = cf.get("db", "threads")

print category[1]
