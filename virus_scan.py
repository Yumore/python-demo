import re
from urllib import request


class virus_scan:
    def __init__(self):
        self.base_url = "https://www.virscan.org/reportlist/"

    def get_url(self, page_size):
        for page in range(page_size):
            print("current url = " + (self.base_url + str(page)))
            response = request.urlopen(self.base_url + str(page))
            html = response.read()
            html = html.decode('utf-8')
            self.parse_html(html)

    def parse_html(self, html):
        tables = re.findall(r"<table.*?>.*?</table>", html, re.M | re.S)
        for index, table in enumerate(tables, start=0):
            if index == 1:
                print("分页的table: %s" % table)
                continue
            else:
                # 匹配<th></th>之间的内容
                # 因为<tr>标签大多数不是在同一行，所以要加 re.S和re.M多行匹配
                trs = re.findall(r"<tr.*?>(.*?)</tr>", table, re.S | re.M)
                data_list = []
                for indicate, tr in enumerate(trs, start=0):
                    # tr = tr.replace('&nbsp;', '').replace('/> ', '/>').replace('> <', '><')
                    # 匹配<td></td>之间的内容
                    # tds = re.findall(r"<td>(.*?)</td>", tr, re.S | re.M)
                    if indicate >= 1:
                        tds = re.findall(r"<td>(.*?)</td>", tr, re.S | re.M)
                        sql_data = []
                        for position, td in enumerate(tds, start=0):
                            print('position=>td : %s=>%s' % (position, td))
                            if position == 1 and "Found" in tr:
                                print("X" * 30, "没有找到病毒", "X" * 30)
                                continue
                            values = re.findall(r'<a .*?>(.*?)</a>', td, re.S | re.M)
                            hrefs = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", td, re.I | re.S | re.M)
                            print("values: %s --- hrefs: %s" % (values, hrefs))
                            sql_data.extend(values)
                            sql_data.extend(hrefs)
                        print("sql_data: %s" % sql_data)
                        data_list.append(sql_data)
                    else:
                        ths = re.findall(r"<th[^>]*>(.*?)</th>", tr, re.S | re.M)
                        print("ths: %s" % ths)
                        continue
                print("data_list: %s" % data_list)

    def start(self):
        # data_utils.csv_mysql("./full-back.csv")
        self.get_url(1)
