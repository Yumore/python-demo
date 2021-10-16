import re
from urllib import request


class bazaar:
    def __init__(self):
        self.url_list = []
        self.base_url = "https://bazaar.abuse.ch/browse/"
        self.index = 0

    def get_url(self, page):
        for i in range(1, page + 1):
            self.url_list.append(self.base_url)

    def get_info(self):
        for url in range(len(self.url_list)):
            print(self.url_list[url])
            response = request.urlopen(self.url_list[url])
            html = response.read()
            html = html.decode('utf-8')
            self.parse_html(html)

    def parse_html(self, html):
        tables = re.findall(r"<table.*?>.*?</table>", html, re.M | re.S)
        for table in tables:
            # print(table)
            # 匹配<th></th>之间的内容
            ths = re.findall(r"<th>(.*?)</th>", table, re.S | re.M)
            for th in ths:
                print('th : %s' % th)
            # 因为<tr>标签大多数不是在同一行，所以要加 re.S和re.M多行匹配
            trs = re.findall(r"<tr>(.*?)</tr>", table, re.S | re.M)
            for row in trs:
                print("row: %s" % row)
                # 匹配<td></td>之间的内容
                tds = re.findall(r"<td>(.*?)</td>", row, re.S | re.M)
                for td in tds:
                    print("-----------------------------------------------------------------------------------")
                    print('td : %s' % td)
                    print("-----------------------------------------------------------------------------------")
            #     data_utils.insert_bazaar(tds[0], tds[1], tds[2], tds[3], tds[4], tds[5], tds[6])

    def start(self):
        self.get_url(1)
        self.get_info()
