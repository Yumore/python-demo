# coding=utf-8
import re
import time
import urllib.parse
import urllib.request

import bs4
# 伪装成浏览器访问，适用于拒绝爬虫的网站
from pyparsing import unicode

headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
           'Referer': 'http://www.baidu.com/'}


def initialized():
    # 好吧，我就找到这一个免费的
    url_prefix = 'https://www.virscan.org/reportlist'

    responses = urllib.request.Request(url_prefix)
    html = urllib.request.urlopen(responses).read().decode("utf-8")

    # 解析html
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # 正则解析页面URL
    pattern = r'/reportlist/\w+'
    li_result = soup.find_all('a', href=re.compile(pattern))

    # 找到页面最大值
    max_page = 1
    for link in li_result:
        url2 = link['href']
        page = url2.split('/')[-1]
        if max_page < int(page):
            max_page = int(page)

    print("initialized-->max_page=%d" % max_page)
    # 访问查找到url
    for x in range(1, max_page + 1):
        page_url = url_prefix + '/%d' % (x)
        # print(page_url)
        get_report(page_url)
        time.sleep(1)


def get_report(page_url):
    print('get_report-->' + page_url)
    responses = urllib.request.Request(page_url)
    html = urllib.request.urlopen(responses).read().decode("utf-8")
    # 解析html
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # 查找首页所有a链接，匹配想要的URL格式（v.xxx内容）
    pattern = r'https://v.virscan.org/\w+'  # URL格式
    v_links = soup.find_all('a', href=re.compile(pattern))
    for vlink in v_links:
        url3 = urllib.parse.quote(vlink['href'])
        url3 = url3.replace('https%3A', 'https:')
        # print(url3)
        if vlink.has_attr('alt'):
            vn = vlink['alt']
        else:
            vn = ''
        # print(vn)
        # 只扫面和Android相关的病毒链接
        if 'android' in url3.lower():
            # 获取到病毒名称
            if vn == '':
                vn = url3.split('/')[-1][0:-5]
                vn = urllib.parse.unquote(vn)
            print('get antivirus name :' + vn)
            getAndroidVirusReport(url3)
            time.sleep(1)


def getAndroidVirusReport(web_url):
    responses = urllib.request.Request(web_url)
    html = urllib.request.urlopen(responses).read()
    print("getAndroidVirusReport-->html=%s", html)
    html = unicode(html, errors='ignore')
    # contents = html.decode('unicode_escape')
    # contents = html.decode("utf-8")
    # 解析html
    soup = bs4.BeautifulSoup(html, 'html.parser')

    base_page_url = urllib.parse.unquote(web_url[:-5]) + '/'

    # 获取详解界面
    pattern = 'https://v.virscan.org/'
    v_info_links = soup.find_all('a', href=re.compile(pattern))
    # 这里是找到页面最大值，然后for循环访问
    max_page_num = 1
    for link in v_info_links:
        url4 = link['href']
        num_str = url4.split('/')[-1][0:-5]
        try:
            if max_page_num < int(num_str):
                max_page_num = int(num_str)

        except Exception as e:
            print(e)
            continue
    print('found max page:' + str(max_page_num))

    for i in range(1, max_page_num + 1):
        url5 = urllib.parse.quote(base_page_url + str(i) + '.html')
        url5 = url5.replace('https%3A', 'https:')
        getAndroidVirusPage(url5)
        time.sleep(1)


# 获取病毒md5值
def getAndroidVirusPage(web_url):
    print("getAndroidVirusPage-->web_url=" + web_url)
    responses = urllib.request.Request(web_url)
    html = urllib.request.urlopen(responses).read().decode("utf-8")
    # 解析html
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # 拿到md5值
    pattern = r'https://md5.virscan.org/\w+'  # URL格式
    md5_links = soup.find_all('a', href=re.compile(pattern))
    for link in md5_links:
        url6 = link['href']
        md5str = url6.split('/')[-1][0:-5]
        print("get file md5 :" + md5str)
