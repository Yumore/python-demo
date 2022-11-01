import json

import pandas as pd
import requests
from bs4 import BeautifulSoup


def getUrlText(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    '''
    爬取网页的通用代码框架
    '''
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # 如果status_code不等于200,就抛出异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("产生异常")


'''
切换为手机模式爬的结果，有点问题
'''


# def getPageApp(pageConfigVersion):
#     '''
#     获取指定pageConfigVersion的app信息
#     '''
#     result = [] # 存放结果
#     url_left = r"https://app.market.xiaomi.com/apm/featured?stamp=0&os=1.1.1&model=unknown&ro=unknown&marketVersion=1914102&imei=cfcd208495d565ef66e7dff9f98764da&miuiBigVersionName=unknown&resolution=1080*1920&webResVersion=0&clientId=cfcd208495d565ef66e7dff9f98764da&densityScaleFactor=3&co=CN&pageConfigVersion=0&session=cfcd208495d565ef66e7dff9f98764da&deviceType=0&la=zh&sdk=19&mobileWeb=1&newUser=true&page="
#     url_right = r"&combine=1&h5=1&supportSlide=4&refs=index"

#     url = url_left+str(pageConfigVersion)+url_right
#     first_text = getUrlText(url)
#     first_data = json.loads(first_text)

#     for i in range(1,len(first_data['list'])):
#         detail_first = first_data['list'][i]
#         try:
#             listApps = detail_first['data']['listApp']
#         except:
#             continue
#         for j in range(len(listApps)):
#             detail_data =listApps[j]
#             app_name = detail_data['displayName']
#             app_first_level = detail_data['level1CategoryName']
#             app_second_level = detail_data['level2CategoryName']
#             result.append([app_first_level,app_second_level,app_name])
#     return result

# results = []
# for p in range(5):
#     r = getPageApp(p)
#     print(len(r))
#     results.extend(r)
# results = pd.DataFrame(results)
# results.drop_duplicates()

def getCategoryID():
    '''
    返回值，列表：去除【游戏】的分类id列表
    '''
    origin_url = "http://app.mi.com/category/0"
    origin_url_text = getUrlText(origin_url)
    origin_soup = BeautifulSoup(origin_url_text, 'lxml')
    category_list = origin_soup.find_all('ul', class_="category-list")[0]
    categorys = category_list.find_all('a')
    category_id = []  # 存放id结果
    for cate in categorys:
        category_id.append(cate.attrs['href'].split('/')[-1])

    return category_id


def getPageAppMessage():
    '''
    获取指定app信息
    '''
    url_left = r"http://app.mi.com/categotyAllListApi?page="
    url_center = r"&categoryId="
    url_right = r"&pageSize=30"

    count = 0  # app计数
    result = []  # 存储结果
    categoryId = getCategoryID()
    for cid in categoryId:
        pageNum = 0  # 初值
        flag = True  # 页面循环标记，当无数据时标记为 False
        while flag:
            url = url_left + str(pageNum) + url_center + cid + url_right
            url_text = getUrlText(url)
            url_data = json.loads(url_text)
            data = url_data['data']
            if data:
                for i in range(len(data)):
                    app_name = data[i]["displayName"]
                    app_first_level = data[i]['level1CategoryName']
                    result.append([app_first_level, app_name])
                    count += 1
                    print([app_first_level, app_name], count)
                pageNum += 1  # 页面加1
            else:
                flag = False
                print('一级标签：', app_first_level)
                print('页面个数有：', pageNum)
        print(cid)
    return result


if __name__ == "__main__":
    result = getPageAppMessage()
    result = pd.DataFrame(result)
    result = result.drop_duplicates()
    result.columns = ['一级标签', 'app名称']
    result.to_excel('xiaomiApp.xls', index=False, encoding='utf-8')
