import os
from urllib import request


class class_YYB:
    def __init__(self):
        self.url_list = []
        self.download_path = '/Users/nathaniel/apks'
        self.baseurl = 'https://android.myapp.com/myapp/category.htm?orgame=1&categoryId='

    def geturl(self, page_index):
        for i in range(100, page_index):
            self.url_list.append(self.baseurl + str(i))

    def spider(self):
        for i in range(len(self.url_list)):
            response = request.urlopen(self.url_list[i])
            html = response.readlines()
            link_list = []
            for i in range(len(html)):
                if 'ex_url' in html[i]:
                    tmp = html[i].split('ex_url="')[1]
                    tmp = tmp.split('"')[0]
                    link_list.append(tmp)

            for url in link_list:
                file_name = url.split('=')[1]
                file_name = file_name.split('&')[0]

                file_path = os.path.join(self.download_path, file_name)
                print('DOWNLOADING : ' + file_path)
                request.urlretrieve(url, file_path)

    def start(self):
        self.geturl(122)
        self.spider()
