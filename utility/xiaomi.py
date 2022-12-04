# coding=utf-8
import re
from urllib import request, parse

import requests
from bs4 import BeautifulSoup

from utility import data_utils


def parser_apks(self, count=0):
    _root_url = "http://app.mi.com"  # 应用市场主页网址
    res_parser = {}
    page_num = 1  # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    while count:
        # 获取排行榜页面的网页内容
        wbdata = requests.get("http://app.mi.com/topList?page=" + str(page_num)).text
        print("开始爬取第" + str(page_num) + "页")
        # 解析页面内容获取 应用下载的 界面连接
        soup = BeautifulSoup(wbdata, "html.parser")
        links = soup.body.contents[3].find_all("a", href=re.compile("/details?"), class_="", alt="")
        for link in links:
            detail_link = parse.urljoin(_root_url, str(link["href"]))
            package_name = detail_link.split("=")[1]
            # 在下载页面中获取 apk下载的地址
            download_page = requests.get(detail_link).text
            soup1 = BeautifulSoup(download_page, "html.parser")
            download_link = soup1.find(class_="download")["href"]
            download_url = parse.urljoin(_root_url, str(download_link))
            # 解析后会有重复的结果，下面通过判断去重
            if download_url not in res_parser.values():
                res_parser[package_name] = download_url
                count = count - 1
            if count == 0:
                break
        if count > 0:
            page_num = page_num + 1
    print("爬取apk数量为: " + str(len(res_parser)))
    return res_parser


def craw_apks(self, count=1, save_path=data_utils.parse_cfg('download', 'path', '../apks')):
    res_dic = parser_apks(count)
    for apk in res_dic.keys():
        print("正在下载应用: " + apk)
        request.urlretrieve(res_dic[apk], save_path + apk + ".apk")
        print("下载完成")
