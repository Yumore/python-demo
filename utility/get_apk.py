#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import time
from urllib import request

import data_utils


class get_apk:
    def __init__(self):
        self.url_list = []
        self.index = 0
        self.download_path = data_utils.parse_cfg('download', 'path', '../apks')
        self.baseurl = 'https://sj.qq.com/myapp/category.htm?orgame='

    def get_url(self, page):
        for i in range(1, page + 1):
            self.url_list.append(self.baseurl + str(i))

    def get_app(self):
        for url in range(len(self.url_list)):
            self.index = 0
            print(self.url_list[url])
            response = request.urlopen(self.url_list[url])
            html = response.read()
            html = html.decode('utf-8')
            link_list = re.findall(r'ex_url="(.*?)" asistanturlid', html)
            app_name_list = re.findall(r'appname="(.*?)" appicon=', html)
            package_name_list = re.findall(r'apk="(.*?)">安装', html)
            print(app_name_list)
            print("本页共计 %d 个app，将依次进行下载，详情如上：列表" % len(app_name_list))
            for link in range(len(link_list)):
                try:
                    file_path = os.path.join(self.download_path, app_name_list[link] + ".apk")
                    print(file_path)
                    request.urlretrieve(link_list[link], file_path)
                    print("over")
                    time.sleep(3)
                    self.index = self.index + 1
                except Exception as e:
                    print(e)
                    print(link_list[link])
            print(package_name_list)
            time.sleep(10)


if __name__ == '__main__':
    a = get_apk()
    a.get_url(20)
    a.get_app()
