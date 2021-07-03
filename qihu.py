#!/usr/bin/evn python
# jojo_xia
import os
import re
import socket
from urllib import request

import apk_info
import data_utils
import file_utils

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
            link_list = re.findall(r"(?<=&url=).*?%26v%3D%26f%3Dz.apk", html)
            patten = re.compile(r'thirdlink&name=(.*?)&icon=')
            app_name_list = patten.findall(html)
            print("本页共计 %d 个app，将依次进行下载，详情如下:", app_name_list)
            for url in link_list:
                try:
                    app_name = '{0}.apk'.format(app_name_list[self.index])
                    if "\xa0" in app_name:
                        print("app name constrains \xa0")
                        app_name = app_name.replace("\xa0", '')
                    if "\x20" in app_name:
                        print("app name constrains \x20")
                        app_name = app_name.replace("\x20", '')
                    if " " in app_name:
                        print("app name constrains  ")
                        app_name = app_name.replace(" ", '')
                    if "com" in url:
                        if re.search(r"(?<=/com)(.*?)_\d*?.apk", url).group(1):
                            package_name = re.search(r"(?<=/com)(.*?)_\d*?.apk", url).group(1)
                            package_name = "com" + package_name + ".apk"
                            self.apk_list.append(package_name)
                    elif "tv" in url:
                        if re.search(r"(?<=/tv)(.*?)_\d*?.apk", url).group(1):
                            package_name = re.search(r"(?<=/tv)(.*?)_\d*?.apk", url).group(1)
                            package_name = "tv" + package_name + ".apk"
                            self.apk_list.append(package_name)
                    else:
                        print('url is : %s' % url)
                    file_path = os.path.join(self.download_path, app_name)
                    if not os.path.isfile(file_path):
                        count = 1
                        while count <= 5:
                            try:
                                print('\rtry to download %s with %d times' % (file_path, count))

                                def reporthook(block_num, block_size, block_total):
                                    print('\rdownload progress: %.2f%%' % (block_num * block_size * 100.0 / block_total), end="")

                                request.urlretrieve(url, file_path, reporthook=reporthook)
                                apk_info.get_apk_info(file_path)
                                print('\ndownload finished!')
                                request.urlcleanup()
                                file_size = os.path.getsize(file_path)
                                print('\rfile size = %.2f MB' % (file_size / 1024 / 1024))
                                file_utils.gen_file_md5(file_path)
                                # time.sleep(3)
                                break
                            except socket.timeout:
                                error_info = '\nReloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                                print("\rerror info : %s" % error_info)
                                count += 1
                        if count > 5:
                            print('\ndownload failed!')
                    else:
                        print('\nfile already exists! file path is : %s' % file_path)
                        md5_file = "%s.md5" % file_path
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
                    print('exception >> %s --> %s' % (url, str(e)))
            print(self.apk_list)
            print(len(self.apk_list))

    def start(self):
        self.get_url(50)
        self.get_app()
