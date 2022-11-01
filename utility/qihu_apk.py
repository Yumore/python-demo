#!/usr/bin/evn python
# jojo_xia
import os
import re
import urllib
import urllib.request


class qihu_apk:
    def __init__(self):
        self.urllist = []
        self.ap_list = []
        self.k = r"com"
        self.c = 0
        self.baseurl = 'http://zhushou.360.cn/list/index/cid/1?page='

    def get_url(self, page):
        for i in range(1, page + 1):
            self.urllist.append(self.baseurl + str(i))

    def get_app(self):
        for j in range(len(self.urllist)):
            self.c = 0
            self.ap_list = []
            response = urllib.request.urlopen(self.urllist[j])
            html = response.read()
            html = html.decode('utf-8')
            link_list = re.findall(r"(?<=&url=).*?%26v%3D%26f%3Dz.apk", html)
            patten = re.compile(r'thirdlink&name=(.*?)&icon=')
            app_name_list = patten.findall(html)
            print(app_name_list)
            print("本页共计 %d 个app，将依次进行下载，详情如上：列表" % len(app_name_list))
            for url in link_list:
                try:
                    app_name = app_name_list[self.c] + '.apk'
                    if re.search(r"(?<=/com)(.*?)_\d*?.apk", url).group(1):
                        package_name = re.search(r"(?<=/com)(.*?)_\d*?.apk", url).group(1)
                        package_name = "com" + package_name + ".apk"
                        self.ap_list.append(package_name)
                    if re.search(r"(?<=/tv)(.*?)_\d*?.apk", url).group(1):
                        package_name = re.search(r"(?<=/tv)(.*?)_\d*?.apk", url).group(1)
                        package_name = "tv" + package_name + ".apk"
                        self.ap_list.append(package_name)
                    file_path = os.path.join("E:\\apk100", app_name)
                    print(file_path)
                    urllib.request.urlretrieve(url, file_path)
                    print("over")
                    self.c = self.c + 1
                except Exception as e:
                    print(e)
                    print(url)
            print(self.ap_list)
            print(len(self.ap_list))

    def start(self):
        self.get_url(51)
        self.get_app()
