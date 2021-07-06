# coding=utf-8
import logging
import re
import socket
import sys
import time
import urllib
from urllib import request, parse

import requests

socket.setdefaulttimeout(30)
sys.path.append("..")
from bs4 import BeautifulSoup


class apk_pure:
    '''
    ApkPure TOP下载
    '''

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename='runtime.log',
            filemode='a+'
        )
        self.logger = logging.getLogger()
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def parser_apks(self, count=1):
        '''
        apkpure
        '''
        # 伪装浏览器
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        _root_url = 'https://apkpure.com'
        res_parser = {}
        page_num = 1  # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
        while count:
            wbdata = requests.get("https://apkpure.com/cn/app?sort=download&page=" + str(page_num), headers=self.header).text
            soup = BeautifulSoup(wbdata, "html.parser")
            download_links = soup.body.contents[9].find_all('a', href=re.compile("/download?"))
            for download_link in download_links:
                download_link = download_link.get('href')
                time.sleep(3)  # 等待3s 海外网站防止连续性登录
                detail_link = parse.urljoin(_root_url, download_link)
                package_name = download_link.split('/')[3]
                s = requests.session()
                s.keep_alive = False  # 关闭多余连接
                time.sleep(3)

                def loop(detail_link=detail_link):
                    '''
                    重复5次获取网页内容，防止网络波动
                    '''
                    try:
                        detail_data = requests.get(detail_link, headers=self.header).text
                        return detail_data
                    except Exception as e:
                        count = 1
                        while count <= 5:
                            try:
                                detail_data = requests.get(detail_link, headers=self.header).text
                                return detail_data
                            except Exception as e:
                                count += 1
                        if count > 5:
                            print("网络超时" + str(e))

                detail_data = loop(detail_link)
                soup = BeautifulSoup(detail_data, "html.parser")
                download = soup.find(id="download_link")["href"]
                if download not in res_parser.values():
                    res_parser[package_name] = download
                    count = count - 1
                if count == 0:
                    break
            if count > 0:
                page_num = page_num + 1
        return res_parser

    def craw_apks(self, count=10, path="..\\"):
        '''
        爬取方法
        在获取的map里面循环下载apk
        '''
        # 在log内增加日期分割
        apk_address = 'APKPureTopAPK' + "\\"
        res_dic = self.parser_apks(count)
        for apk in res_dic.keys():
            self.auto_down(res_dic[apk], apk + ".apk")

    def auto_down(self, url, filename):
        '''
        自动尝试5次下载
        未下载的app记录在log/pure_undown_apk_info.txt文件内
        '''
        try:
            print("正在下载: " + filename.split("\\")[-1])
            self.logger.info("正在下载: " + filename.split("\\")[-1])
            request.urlretrieve(url, filename)
            # 下载完整包后才会加载下载完成log
            print("下载完成: " + filename.split("\\")[-1])
            self.logger.info("下载完成: " + filename.split("\\")[-1])
        except (socket.timeout, Exception) as e:
            # 重试5次
            count = 1
            while count <= 5:
                try:
                    request.urlretrieve(url, filename)
                except (socket.timeout, Exception) as e:
                    count += 1
            if count > 5:
                print("应用下载5次失败：" + filename)
                self.logger.info("应用下载5次失败：" + filename)


if __name__ == "__main__":
    ApkPure = apk_pure()
    ApkPure.craw_apks(count=5)
