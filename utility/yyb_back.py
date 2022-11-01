#!/usr/bin/evn python
# jojo_xia
import os
import re
import time
import urllib
import urllib.request


class yyb_back:
    def __init__(self):
        self.url_list = []
        self.c = 0
        self.baseurl = 'https://sj.qq.com/myapp/category.htm?orgame='

    def get_url(self, page):
        for i in range(1, page + 1):
            self.url_list.append(self.baseurl + str(i))

    def get_app(self):
        for j in range(len(self.url_list)):
            self.c = 0
            print(self.url_list[j])
            response = urllib.request.urlopen(self.url_list[j])
            html = response.read()
            html = html.decode('utf-8')
            link_list = re.findall(r'ex_url="(.*?)" asistanturlid', html)
            app_name_list = re.findall(r'appname="(.*?)" appicon=', html)
            package_name_list = re.findall(r'apk="(.*?)">安装', html)
            print(app_name_list)
            print("本页共计 %d 个app，将依次进行下载，详情如上：列表" % len(app_name_list))
            for u in range(len(link_list)):
                try:
                    file_path = os.path.join("E:\\yyb", app_name_list[u] + ".apk")  # 在这一行修改本地保存路径
                    print(file_path)
                    urllib.request.urlretrieve(link_list[u], file_path)
                    print("over")
                    time.sleep(3)
                    self.c = self.c + 1
                except Exception as e:
                    print(e)
                    print(link_list[u])
            print(package_name_list)
            time.sleep(10)


if __name__ == '__main__':
    a = yyb_back()
    a.get_url(20)
    a.get_app()
