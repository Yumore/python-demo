# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 09:36:17 2020

@author: Administrator
"""
import json
import time

import pandas as pd
import requests
from xlrd import open_workbook
from xlutils.copy import copy


# 写入excel，xlutils可以写入到已存在的excel中,xlwt只能每次都重写
def write_xls(filename, row, first_level, second_level, app_name):
    rb = open_workbook(filename)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row, 0, first_level)
    ws.write(row, 1, second_level)
    ws.write(row, 2, app_name)
    wb.save(filename)


def getUrlText(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

    '''
    爬取网页的通用代码框架
    '''
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # 如果status_code不等于200,就抛出异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


def getAppLabels():
    time_start = time.time()  # 500个结果开始计时

    flag_second = True
    flag_third = True

    url = "https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&serviceType=13&reqPageNum=1&uri=34789c86f4654624ba9e63cf1353c860&maxResults=25&locale=zh_CN"
    com_left_url = r"https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri="
    com_center_url = r"&maxResults=25&reqPageNum="
    com_right_url = r"&locale=zh_CN"

    first_url_text = getUrlText(url)
    first_data = json.loads(first_url_text)
    first_levels = first_data['layoutData'][1]['dataList']

    #     row = 0  # 用来记录存取数据的行数
    global row

    #    result = pd.DataFrame(columns=['一级标签','二级标签','app名称']) # 用来存放结果
    result = []
    for i in range(len(first_levels)):
        first_level = first_levels[i]['name']  # 一级标签
        # 游戏单独处理
        if first_level != "游戏":
            first_detailId = first_levels[i]['detailId']

            # 获取二级标签对应的多页数据
            second_page_num = 1  # 页面初值设为1
            while flag_second:
                second_url = com_left_url + first_detailId + com_center_url + str(second_page_num) + com_right_url
                second_url_text = getUrlText(second_url)
                second_data = json.loads(second_url_text)
                second_levels = second_data['layoutData']

                if second_levels == []:  # 无数据
                    flag_second = False  # 结束循环
                else:
                    second_page_num += 1  # 二级页面自加1
                    for j in range(len(second_levels)):
                        second_level = second_levels[j]['name']  # 二级标签
                        second_detailId = second_levels[j]['detailId']

                        # 获取三级对应的多页app信息
                        third_page_num = 1  # 页面初值设为1
                        while flag_third:
                            third_url = com_left_url + second_detailId + com_center_url + str(third_page_num) + com_right_url
                            third_url_text = getUrlText(third_url)
                            third_data = json.loads(third_url_text)
                            third_levels = third_data['layoutData']
                            if third_levels == []:  # 无数据
                                flag_third = False
                            else:
                                third_page_num += 1  # 三级页面自加1
                                third_levels = third_levels[0]['dataList']

                                for k in range(len(third_levels)):
                                    app_name = third_levels[k]['name']  # 对应的app

                                    #                                    write_xls('test.xlsx',row,first_level, second_level, app_name)
                                    result.append([first_level, second_level, app_name])
                                    #                                    result = result.append(pd.DataFrame({'一级标签':[first_level],'二级标签':[second_level],'app名称':[app_name]}))
                                    row += 1
                                    if row % 500 == 1:
                                        time_end = time.time()  # 500个结果结束计时
                                        print('time cost：%.3f' % (time_end - time_start), 's')
                                        time_start = time.time()
                                        print(row)
                                        print(first_level, "： ", second_level)
                        flag_third = True  # 恢复初值
            flag_second = True  # 恢复初值

    return result


# 主程序
if __name__ == "__main__":
    row = 0  # 用来记录存取数据的行数
    result = getAppLabels()
    result = pd.DataFrame(result, columns=['一级标签', '二级标签', 'app名称'])
    result.to_excel('result2.xlsx', sheet_name='应用', encoding='utf-8', index=False)
