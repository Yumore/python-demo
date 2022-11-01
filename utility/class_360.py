# -*- coding: utf-8 -*-

import os
import re
from urllib import request


class class_360:
    def __init__(self):
        self.url_list = []
        self.download_path = '/Users/nathaniel/apks'
        self.baseurl = 'http://zhushou.360.cn/list/index/cid/1?page='

    def geturl(self, page_index):
        for i in range(35, page_index):
            self.url_list.append(self.baseurl + str(i))

    def spider(self):
        for i in range(len(self.url_list)):
            response = request.urlopen(self.url_list[i])
            html = response.read()
            link_list = re.findall(r"(?<=&url=).*?apk", html)
            for url in link_list:
                file_name = url.split('/')[-1]

                file_path = os.path.join(self.download_path, file_name)
                print('DOWNLOADING : ' + file_path)
                request.urlretrieve(url, file_path)

    def start(self):
        self.geturl(40)
        self.spider()
