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
            # 因为<tr>标签大多数不是在同一行，所以要加 re.S和re.M多行匹配
            trs = re.findall(r"<tr>(.*?)</tr>", table, re.S | re.M)
            for tr in trs:
                # print("tr: %s" % tr)
                ths = re.findall(r"<th>(.*?)</th>", tr, re.S | re.M)
                for th in ths:
                    if "<th>" in th:
                        ths.extend(th.split('<th>'))
                    print('th: %s' % th)
                # 匹配<td></td>之间的内容
                tds = re.findall(r"<td>(.*?)</td>", tr, re.S | re.M)
                for td in tds:
                    # data_utils.insert_bazaar(tds[0], tds[1], tds[2], tds[3], tds[4], tds[5], tds[6])
                    # print("td: %s" % td)
                    if td.startswith("<a "):
                        href = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", td, re.I | re.S | re.M)
                        print("url: %s" % href)
                    elif td.startswith("<img "):
                        print("*" * 30)
                    else:
                        print("啥也没有")

    def start(self):
        self.get_url(1)
        self.get_info()
