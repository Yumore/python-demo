import csv
import hashlib

import pandas
from poprogress import simple_progress

from configs import configs
from database import sqlitex
# 遍历指定目录下的指定前缀和后缀文件
from utility import langUtils


def find_files(path, prefix, extend):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith(prefix) and file.endswith(extend) and 'url' not in file and 'locale_keys' not in file and 'config' not in file:
                fullname = os.path.join(root, file)
                fullname = '/'.join(fullname.split('\\'))
                yield fullname


def find_execl(path, extend):
    file_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == extend:
            file_list.append(file)
    format_logger('find_execl', file_list)
    return file_list


# 数据写入dart文件
def write_file(filename, data_list):
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(data_list)
    file.close()
    format_logger("write_dart", filename + "写入完成")


# 将execl文件数据写入csv文件
# 此处采用的是追加机制
# 因为execl文件有多个sheet，要逐一写入
def write_csv(csv_name, data_rows):
    with open(csv_name, 'a+', encoding='utf-8') as file:
        csv_write = csv.writer(file)
        # csv_write.writerow(data_row)
        csv_write.writerows(data_rows)


def get_file_md5(file_path):
    file_name = os.path.basename(file_path)
    md5_data = hashlib.md5()
    file_size = '{:.2f}'.format(os.path.getsize(file_path) / (1024 ** 2))
    print('正在验证文件名称：%s， 文件大小：%s MB' % (file_name, file_size))
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024 * 1024 * 10)
            print('\r验证速度：%.2f MiBps' % (len(data) / (1024 ** 2)), end='')
            if not data:
                break
            md5_data.update(data)
    file_md5 = md5_data.hexdigest().upper()

    return file_md5


def gen_file_md5(file_path):
    file_name = os.path.basename(file_path)
    md5_file = '{0}.md5'.format(file_path)
    file_out = open(md5_file, "w")
    file_out.write("%s %s\n" % (get_file_md5(file_path), file_name.strip()))
    print("\rgenerate success, file_path : %s" % md5_file)
    file_out.flush()
    file_out.close()


def gen_md5_value(file_path):
    md5_data = hashlib.md5()
    file = open(file_path, 'rb')
    md5_data.update(file.read())
    file.close()
    return md5_data.hexdigest()


# 解析csv文件
def parse_csv(filename):
    csv_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spam_reader:
            csv_data.append(row)
    return csv_data


def find_project(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'common_resource' in file:
                continue
            if file.endswith(configs.dart_ext):
                fullname = os.path.join(root, file)
                fullname = '/'.join(fullname.split('\\'))
                yield fullname


def filter_filename(file_path):
    (path, filename) = os.path.split(file_path)
    return filename


def pandas_csv(filename, rows):
    datas = [["成员", "部门"]]
    for row in rows:
        datas.append([row, ""])
    csv_path = "{}/{}.csv".format(os.getcwd(), filename)
    dataframe = pandas.DataFrame(datas)
    dataframe.to_csv(csv_path, index=False, header=False, encoding='gbk')


def write_xlsx(proj_name, xls_path, dataframes):
    with pandas.ExcelWriter(xls_path, engine='openpyxl') as writer:
        for key in simple_progress(dataframes.keys(), desc="Execl文件写入进度"):
            if '?' in key:
                # key = ''.join(key.split('?'))
                key = key.replace('?', '')
            if key is None or dataframes.get(key) is None or isinstance(dataframes.get(key), list):
                format_logger("write_xlsx", "{}, exceptions: {} => {}".format(proj_name, key, dataframes.get(key)))
                continue
            dataframes.get(key).to_excel(writer, sheet_name=key, header=False, index=False)


def parse_depart(csv_path):
    arg_ele = langUtils.chinese2pinyin("指派给")
    employees = sqlitex.query_distinct(arg_ele)
    format_logger("parse_depart", "employees is {}".format(employees))
    sql_string = "CREATE TABLE IF NOT EXISTS {}(employee TEXT PRIMARY KEY, depart TEXT);".format(configs.departTable)
    sqlitex.create_table(sql_string)
    for employee in employees:
        depart = "内部未查"
        if '-' in employee:
            strings = employee.split('-')
            employee = strings[0]
            depart = "第三方"
        sql_string = "REPLACE INTO {} VALUES('{}','{}');".format(configs.departTable, employee, depart)
        sqlitex.replace_datas(sql_string)
    # 读文件更新
    with open(csv_path, 'r', encoding='gbk') as file:
        csv_reader = csv.reader(file)
        for index, row in enumerate(csv_reader):
            if index == 0:
                continue
            else:
                employee = row[0]
                depart = "第三方"
                if '-' in employee:
                    strings = employee.split('-')
                    employee = strings[0]
                if row[0] in employees:
                    depart = row[1]
                format_logger("parse_depart", "成员 ==> 部门 : {} ==> {}".format(employee, depart))
                sql_string = "REPLACE INTO {} VALUES('{}', '{}');".format(configs.departTable, employee, depart)
                sqlitex.replace_datas(sql_string)
    pandas_csv("员工信息", employees)


import os


def create_file(file_path):
    if not os.path.exists(file_path):
        file = open(file_path, "w")
        file.close()
        print(f"文件 {file_path} 创建成功")
    else:
        print(f"文件 {file_path} 已经存在")


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"目录 {dir_path} 创建成功")
    else:
        print(f"目录 {dir_path} 已经存在")


file_path = "example.txt"
dir_path = "example_dir"

create_file(file_path)
create_directory(dir_path)
