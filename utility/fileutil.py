import csv
import logging
import os

# 遍历指定目录下的指定前缀和后缀文件
from utility import configs


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


# 日志打印
def format_logger(tag, message):
    logging.info('========> {0} - {1}'.format(tag, message))
