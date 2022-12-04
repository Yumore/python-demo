#!/usr/bin/evn python
# jojo_xia
import os
import re
import socket
from urllib import request
from urllib.error import ContentTooShortError

from utility import file_utils, data_utils, apk_info

socket.setdefaulttimeout(30)


class qihu:
    def __init__(self):
        self.url_list = []
        self.apk_list = []
        self.index = 0
        self.download_path = data_utils.parse_cfg('download', 'path', '../apks')
        self.baseurl = 'http://zhushou.360.cn/list/index/cid/1?page='

    def get_url(self, page):
        for i in range(1, page + 1):
            self.url_list.append(self.baseurl + str(i))

    def get_app(self):
        print('download root dir is : %s' % self.download_path)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        for index in range(len(self.url_list)):
            self.index = 0
            self.apk_list = []
            response = request.urlopen(self.url_list[index], timeout=15)
            html = response.read()
            html = html.decode('utf-8')
            # print('url list is : ', re.findall(r"(?<=&url=).*?apk", html))
            link_list = re.findall(r"(?<=&url=).*?%26v%3D%26f%3Dz.apk", html)
            patten = re.compile(r'thirdlink&name=(.*?)&icon=')
            app_name_list = patten.findall(html)
            print("当前分类: %d, 本页共计%d个app，将依次进行下载，详情如下:" % (index, len(app_name_list)), app_name_list)
            for url in link_list:
                try:
                    app_name = '{0}.apk'.format(app_name_list[self.index])
                    if " " in app_name:
                        print("app name constrains  ")
                        app_name = app_name.replace(" ", '')
                    # http://s.shouji.qihucdn.com/210615/88e3d6ad97f17836fc2be9c7f10f8ee8/com.doumi.jianzhi_134.apk
                    # ?en=curpage%3D%26exp%3D1626254620%26from%3DAppList_json%26m2%3D%26ts%3D1625649820%26tok%3Dbb89589c22a22c76bc917767b8083660%26v%3D%26f%3Dz.apk
                    file_path = os.path.join(self.download_path, app_name)
                    if not os.path.isfile(file_path):
                        count = 1
                        while count <= 5:
                            try:
                                print('\rtry to download %s with %d times' % (file_path, count))
                                self.real_down(url=url, file_path=file_path)
                                break
                            except socket.timeout:
                                error_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                                print("\rerror info : %s" % error_info)
                                count += 1
                            except ContentTooShortError:
                                print('Network conditions is not good. Reloading...')
                                self.real_down(url=url, file_path=file_path)
                        if count > 5:
                            print('\ndownload failed!')
                    else:
                        print('\nfile already exists! file path is : %s' % file_path)
                        md5_file = '{0}.md5'.format(file_path)
                        if not os.path.isfile(md5_file):
                            os.remove(file_path)
                        else:
                            file_out = open(md5_file, "r")
                            if file_out.read() == file_utils.gen_file_md5(file_path):
                                apk_info.get_apk_info(file_path)
                            else:
                                os.remove(file_path)
                                os.remove(md5_file)

                    self.index = self.index + 1
                except Exception as e:
                    print('\rexception >> %s --> %s' % (url, str(e)))

    def real_down(self, url, file_path):
        def reporthook(block_num, block_size, block_total):
            print('\rdownload progress: %.2f%%' % (block_num * block_size * 100.0 / block_total), end="")

        request.urlretrieve(url, file_path, reporthook=reporthook)
        apk_info.get_apk_info(file_path)
        request.urlcleanup()
        file_size = os.path.getsize(file_path)
        print('\rdownload finished, file size : %.2f MB' % (file_size / 1024 / 1024))
        file_utils.gen_file_md5(file_path)
        # time.sleep(3)

    def start(self):
        self.get_url(50)
        self.get_app()
