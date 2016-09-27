# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import urllib
import ConfigParser
import os
import threading

# load config file
cf = ConfigParser.ConfigParser()
cf.read("config")
category = cf.get("db", "category").split(',')
save = cf.get("db", "save")
img_num = cf.getint("db", "img_num")
threads = cf.getint("db", "threads")


def crawler(obj):

    # the xpath of object element
    xpath = '//div[@id="imgid"]/ul/li/a/img'

    # launch Firefox
    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=fp)

    # maximize window, because it can only get the images in view during eatch catch
    driver.maximize_window()

    # record the img url
    img_url_dic = {}

    for x in xrange(len(obj)):
        # the aim url
        url = 'http://pic.sogou.com/pics?query='+obj[x]+'&w=05009900&p=&_asf=pic.sogou.com&_ast=1474957566&sc=index&sut=1709&sst0=1474957566200'

        # open the url using established webdriver
        driver.get(url)

        # Simulation of rolling web page to download more images
        pos = 0
        m = 0  # pic's record number
        i = 0
        while m < img_num:
            pos += i*500  # Scroll down 500
            i += 1
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            time.sleep(1)

            for element in driver.find_elements_by_xpath(xpath):
                if m > img_num - 1:
                    break
                img_url = element.get_attribute('src')

                # save pictures
                if img_url is not None and img_url not in img_url_dic:
                    img_url_dic[img_url] = ''
                    m += 1
                    filename = str(m) + '-' + obj[x] + '.png'

                    # get pictures and put them in dic
                    data = urllib.urlopen(img_url).read()
                    dic = save + '/' + obj[x] + '/'
                    if not os.path.exists(dic):
                        os.mkdir(dic)
                    f = open(dic + filename, 'wb')
                    f.write(data)
                    f.close()

    driver.close()


# assign each threads' workload
if threads > len(category):
    threads = len(category)
num = len(category) / threads
mod = len(category) % threads
thrCategory = [[]]*threads
x = 0
for i in xrange(threads):
    thrCategory[i] = category[x:x+num]
    x += num
    if i < mod:
        thrCategory[i].append(category[x:x+1])
        x += 1

# establish threads
thr = []
for i in xrange(threads):
    t = threading.Thread(target=crawler, args=(thrCategory[i],))
    thr.append(t)
    t.start()
