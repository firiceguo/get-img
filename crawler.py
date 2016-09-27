# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import urllib
import ConfigParser
import os

# load config file
cf = ConfigParser.ConfigParser()
cf.read("config")
category = cf.get("db", "category").split(',')
save = cf.get("db", "save")
img_num = cf.getint("db", "img_num")
threads = cf.getint("db", "threads")

# 目标元素的xpath
xpath = '//div[@id="imgid"]/ul/li/a/img'

# 启动Firefox浏览器
fp = webdriver.FirefoxProfile()
driver = webdriver.Firefox(firefox_profile=fp)

# 最大化窗口，因为每一次爬取只能看到视窗内的图片
driver.maximize_window()

# 记录下载过的图片地址，避免重复下载
img_url_dic = {}

for x in xrange(len(category)):
    # 爬取页面地址
    url = 'http://pic.sogou.com/pics?query='+category[x]+'&w=05009900&p=&_asf=pic.sogou.com&_ast=1474957566&sc=index&sut=1709&sst0=1474957566200'

    # 浏览器打开爬取页面
    driver.get(url)

    # 模拟滚动窗口以浏览下载更多图片
    pos = 0
    m = 0  # 图片编号
    i = 0
    while m < img_num:
        pos += i*500  # 每次下滚500
        i += 1
        js = "document.documentElement.scrollTop=%d" % pos
        driver.execute_script(js)
        time.sleep(1)

        for element in driver.find_elements_by_xpath(xpath):
            if m > img_num - 1:
                break
            img_url = element.get_attribute('src')
            print img_url
            # 保存图片到指定路径
            if img_url is not None and img_url not in img_url_dic:
                img_url_dic[img_url] = ''
                m += 1
                # ext = img_url.split('/')[-1]
                filename = str(m) + '-' + category[x] + '.png'
                # 保存图片数据
                data = urllib.urlopen(img_url).read()
                dic = save + '/' + category[x] + '/'
                if not os.path.exists(dic):
                    os.mkdir(dic)
                f = open(dic + filename, 'wb')
                f.write(data)
                f.close()
driver.close()
