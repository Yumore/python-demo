#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket
import threading
from urllib import request

import apk_info
import data_utils
import file_utils

socket.setdefaulttimeout(30)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
category = [-10, 122, 102, 110, 103, 108, 115, 106, 101, 119, 104, 114, 117, 107, 112, 118, 111, 109, 105, 100, 113,
            116]
category_names = ['腾讯软件', '阅读', '新闻', '视频', '旅游', '工具', '社交', '音乐', '美化', '摄影', '理财', '系统',
                  '生活', '出行', '安全', '教育', '健康', '娱乐', '健康', '儿童', '办公', '通讯']
thread_count = len(category)
lock = threading.Lock()


class yyb:
    def __init__(self):
        self.download_path = data_utils.parse_cfg('download', 'path', '../apks')
        print(self.download_path)
        self.url_list = []
        self.baseurl = 'https://android.myapp.com/myapp/category.htm?orgame=1&categoryId='

    def geturl(self, page_index):
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        for page in range(100, page_index):
            self.url_list.append(self.baseurl + str(page))
        self.url_list.append(self.baseurl + str(-10))

    def download(self, url, index):
        print('\rdownload url is : %s' % url)
        file_name = url.split('=')[1]
        file_name = file_name.split('&')[0]
        file_path = os.path.join(self.download_path, file_name)
        if not os.path.isfile(file_path):
            count = 1
            while count <= 5:
                try:
                    print('\rtry to download %s with %d times' % (file_path, count))

                    # os.chmod(self.download_path, stat.S_IRWXO + stat.S_IRWXG | stat.S_IRWXU)

                    def reporthook(block_num, block_size, block_total):
                        print('\rdownload progress: %.2f%%' % (block_num * block_size * 100.0 / block_total), end="")

                    self.down_real(url=url, file_path=file_path, reporthook=reporthook, category=category_names[index])
                    break
                except socket.timeout:
                    err_info = '\nReloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                    print("\rerror info : %s" % err_info)
                    count += 1
            if count > 5:
                print('\ndownload failed!')
        else:
            print('\nfile already exists! file path is : %s' % file_path)
            apk_info.get_apk_info(file_path, category_names[index])

    def spider(self):
        for index in range(len(self.url_list)):
            try:
                response = request.urlopen(self.url_list[index], timeout=15)
                html = response.readlines()
                link_list = []
                for task in range(len(html)):
                    str_tmp = str(html[task], encoding="utf8")
                    if 'ex_url' in str_tmp:
                        tmp = str_tmp.split('ex_url="')[1]
                        tmp = tmp.split('"')[0]
                        link_list.append(tmp)

                self.single_thread(link_list, index)

            except Exception as e:
                print("exception : %s" % str(e))

    def single_thread(self, link_list, index):
        for url in link_list:
            self.download(url, index)

    def multi_threads(self):
        print('thread %s is running ... ' % threading.currentThread().getName())
        while True:
            try:
                with lock:
                    for url in self.url_list:
                        self.download(url)
                        item = next(self.url_list)
                        print(item)
            except Exception as e:
                print('exception %s' % str(e))
            print('thread %s is ending ... ' % threading.currentThread().getName())

    def down_real(self, url, file_path, reporthook, category):
        request.urlretrieve(url, file_path, reporthook)
        apk_info.get_apk_info(file_path, category)
        print('\ndownload finished!')
        request.urlcleanup()
        file_size = os.path.getsize(file_path)
        print('\rfile size = %.2f MB' % (file_size / 1024 / 1024))
        file_utils.gen_file_md5(file_path)

    def start(self):
        self.geturl(123)
        self.spider()
