import time

from bs4 import BeautifulSoup
from python爬题库.dataManager import DataManager
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import ActionChains

# 实例化数据库类对象
db = DataManager()


def to_string(s):
    string = s.strip().split("\t")
    string_list = []
    for i in range(len(string)):
        if string[i] != "":
            string_list.append(string[i].strip())
    return string_list


def have_alert(driver):
    try:
        alert = driver.switch_to.alert
        return alert
    except NoAlertPresentException:
        return False


def get(type_work):
    """
    获取试题
    :param type_work: 工种名称
    :return: [[题型, 题干, 选项, 答案], [], ...]
    """

    # 设置最大等待时长为 10秒
    driver = webdriver.Chrome()  # 测试
    driver.implicitly_wait(10)
    driver.get("http://www.tf110.cn")  # 进入界面
    # http://www.tf110.cn/tf/computer/sjlogin_index.do
    driver.maximize_window()  # 最大化窗口

    # 用户名
    user_name = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[2]/form/input[2]')
    user_name.send_keys("19914724023")
    # 密码
    user_passwd = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[2]/form/input[3]')
    user_passwd.send_keys("1234567890")

    print("等待10秒，请尽快输入验证码")
    time.sleep(10)

    # 代替回车
    # driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[2]/form/input[4]').click()  # 登录

    # /html/body/div[1]/div[1]/div/div[2]/div[2]/ul/li[2]/a/span[1]  G1工业锅炉司炉
    mouse = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]')
    ActionChains(driver).move_to_element(mouse).perform()
    # 点击更换工种类型
    # print(driver.find_elements_by_xpath("//*[contains(text(), "+type_work+")]"))
    # //span[contains(text(), '低压电工作业')]
    driver.find_elements_by_xpath("//span[contains(text(), '" + type_work + "')]")[0].click()
    if have_alert(driver):
        driver.switch_to.alert.accept()

    # 全真题库
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/ul/li[2]/a').click()

    # 点击弹出警告
    if have_alert(driver):
        driver.switch_to.alert.accept()

    # 获取题目数量
    cnt = driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/div[1]/div[2]/h1/span[2]').text
    print("题目数量有" + cnt)
    # 现在的题号
    cnt_c = int(driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/div[1]/div[2]/h1/span[1]').text)
    time.sleep(2)

    for i in range(cnt_c, int(cnt)):
        print('第' + str(i) + "/" + str(cnt) + '题', end=": ")

        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # 判断试题类型
        ques_type = driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/div[1]/div[1]').text.split(" ")[0]
        print("试题类型", ques_type)

        # 填入题型
        if ques_type == "判断题":
            ques_type = 0
        elif ques_type == "单选题":
            ques_type = 1
        elif ques_type == "多选题":
            ques_type = 2
        # 获取题干
        ques_text = driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/div[1]/div[2]/h1/span[3]').text
        print("题干", ques_text)

        # 选项
        op_list = soup.find('div', class_='text_list').find_all('li')
        op_len = len(op_list)
        print("选项长度", op_len)

        # 获取所有选项
        op_s = ''
        for lens in range(op_len):
            op = to_string(op_list[lens].text)
            print(op)
            op_s += chr(ord('A') + lens) + op[1]
        op_s += ''
        print(op_s)

        # 获取答案
        if ques_type == 0:
            time.sleep(0.4)
            driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/div[1]/div[2]/div/ul/li[1]/a/span').click()
            # driver.find_element_by_xpath('').click()

            ans_s = driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/div[2]/div[1]/div[1]/a').text
            ans_s = ans_s.split("参考答案")[1].strip()
            if ans_s[-1] == '对':
                ans_s = 'A'
            elif ans_s[-1] == '错':
                ans_s = 'B'
            print('答案:', ans_s)
        elif ques_type == 1:
            for lens in range(1, op_len + 1):
                driver.find_element_by_xpath(
                    '/html/body/div[4]/div/div/form/div/div[1]/div[2]/div/ul/li[' + str(lens) + ']/a/span').click()
            ans_s = \
                driver.find_element_by_xpath(
                    '/html/body/div[4]/div/div/form/div/div[2]/div[1]/div[1]/a').text.strip().split(" ")[-1].strip()
            print(ans_s)

        elif ques_type == 2:
            for lens in range(1, op_len + 1):
                driver.find_element_by_xpath(
                    '/html/body/div[4]/div/div/form/div/div[1]/div[2]/div[1]/ul/li[' + str(lens) + ']/label/a').click()

            driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/form/div/div[1]/div[2]/div[2]/a').click()
            ans_s = \
                driver.find_element_by_xpath(
                    '/html/body/div[4]/div/div/form/div/div[2]/div[1]/div[1]/a').text.strip().split(" ")[-1].strip()
            print(ans_s)
        # 下一题
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/ul/li[3]').click()
        data = (ques_type, ques_text, op_s, ans_s)
        db.save_data(data)


if __name__ == '__main__':
    get("A特种设备相关管理（限电梯安全管理）")
