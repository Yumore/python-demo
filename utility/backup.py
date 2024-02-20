# !/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os

import numpy
import xlrd

def_value = '************************'
execl_ext = 'xls'


# 判断变量类型的函数
def typeof(variate):
    var_type = None
    if isinstance(variate, int):
        var_type = "int"
    elif isinstance(variate, str):
        var_type = "str"
    elif isinstance(variate, float):
        var_type = "float"
    elif isinstance(variate, list):
        var_type = "list"
    elif isinstance(variate, tuple):
        var_type = "tuple"
    elif isinstance(variate, dict):
        var_type = "dict"
    elif isinstance(variate, set):
        var_type = "set"
    return var_type


# 返回变量类型
def get_type(variate):
    type_array = {"int": "整数", "float": "浮点", "str": "字符串", "list": "列表", "tuple": "元组", "dict": "字典", "set": "集合"}
    var_type = typeof(variate)
    if not (var_type in type_array):
        return "未知类型"
    return type_array[var_type]


# 解析现有的翻译execl文件
# 并对数据进行格式化处理
# 方便后期做数据校对和匹配
def parse_execl(filename):
    execl_rows = []
    workbooks = xlrd.open_workbook(filename)
    sheet_names = workbooks.sheet_names()
    for sheet_index in range(len(workbooks.sheets())):
        sheet = workbooks.sheet_by_name(sheet_names[sheet_index])
        for row_index in range(0, sheet.nrows):
            sheet_row = sheet.row_values(row_index)
            # 剔除空数据
            if len(sheet_row) == 0:
                continue
            # 处理· ・ TODO 因为要一一对应所以要单独处理
            if '·' in str(sheet_row) or '・' in str(sheet_row):
                str_a = []
                if '·' in str(sheet_row[0]):
                    str_a = str(sheet_row[0]).split('·')
                if '・' in str(sheet_row[0]):
                    str_a = str(sheet_row[0]).split('・')
                str_b = []
                # 翻译--[校对] 的骚操作对应的列
                real_suffix = sheet_row[1]
                if len(sheet_row) > 2 and pandas.isnull(sheet_row[2]) and len(str(sheet_row[2])) > 0:
                    real_suffix = sheet_row[2]
                if '·' in str(real_suffix):
                    str_b = str(real_suffix).split('·')
                if '・' in str(real_suffix):
                    str_b = str(real_suffix).split('・')
                # 将新的键值对重新拼装
                string_array = []
                for index in range(len(str_a)):
                    string_array.clear()
                    string_array.append(str_a[index])
                    # 前后角标不对称
                    if index >= len(str_b):
                        string_array.append(def_value)
                    else:
                        string_array.append(str_b[index])

                    if string_array in execl_rows:
                        continue
                    execl_rows.append(string_array)
            else:
                if sheet_row in execl_rows:
                    continue
                execl_rows.append(sheet_row)

    return trim_data(execl_rows)


def read_xls(filename):
    """解决读取XLS文件出现警告，并且无法获取数据的问题"""
    xls_workbooks = xlrd.open_workbook(filename)
    sheet_names = xls_workbooks.sheet_names()
    data_all = {}

    for sheet_name in sheet_names:
        '''1、获取XLS表中真实行数和列数'''
        data_sheet = xls_workbooks.sheet_by_name(sheet_name)
        sheet_rows = 1
        sheet_cols = 0
        while 1:
            try:
                data_row = data_sheet.row_values(sheet_rows)
            except:
                break
            else:
                sheet_rows = sheet_rows + 1
                sheet_cols = max(sheet_cols, len(data_row))

        '''2、生成columns，定义一个data_new二维列表，存储单个sheet中所有数据'''
        data_row_0 = data_sheet.row_values(0)

        # columns 为XLS文件第一行
        columns = data_row_0 + ['Unnamed:' + str(i) for i in range(1, sheet_cols - len(data_row_0) + 1)]
        data_new = []

        '''3、遍历每行，每行的长度低于ncols时，自动并自动补充nan'''
        for row_i in range(1, sheet_rows):
            data_row_i = data_sheet.row_values(row_i)

            # 当表格中有行合并时，获取此行数据时：
            #   参与合并的单元格中最左边单元个内容 = 合并单元格中内容
            #   其他参与合并的单元个为空或者不显示，因此这些单元格填充为np.nan
            #   保证每行的长度=列数
            data_row_i = [numpy.nan if j == "" else j for j in data_row_i]
            data_row_i_supplement = data_row_i + [numpy.nan] * (sheet_cols - len(data_row_i))

            data_new.append(data_row_i_supplement)

        '''4、生成dataframe'''
        data_f = pandas.DataFrame(data_new, columns=columns)
        data_all[sheet_name] = data_f
    return data_all


# 修正数据
def trim_data(execl_rows):
    for sheet_row in execl_rows:
        # 移除 \n “ " ' 【】 []
        # for index, val in enumerate(real_data):
        for index in range(len(sheet_row)):
            if pandas.isnull(sheet_row[index]):
                sheet_row[index] = def_value
            if 'str' != typeof(sheet_row[index]):
                continue
            sheet_row[index] = sheet_row[index].strip()
            # 第一次移除逗号
            if sheet_row[index].endswith(',') or sheet_row[index].endswith('，'):
                sheet_row[index] = sheet_row[index][0: len(sheet_row[index]) - 1]
            if sheet_row[index].startswith('"') and sheet_row[index].endswith('"'):
                sheet_row[index] = sheet_row[index].replace('"', '')
            if sheet_row[index].startswith("'") and sheet_row[index].endswith("'"):
                sheet_row[index] = sheet_row[index].replace("'", '')
            # 奇奇怪怪的符号组合 TODO MLGJ
            if (sheet_row[index].startswith('“') or sheet_row[index].startswith('”')) and (sheet_row[index].endswith('”') or sheet_row[index].endswith('“')):
                sheet_row[index] = sheet_row[index][1: len(sheet_row[index]) - 1]
            # 奇奇怪怪的符号组合 TODO MLGJ
            if sheet_row[index].startswith('"') and (sheet_row[index].endswith('”') or sheet_row[index].endswith('“') or sheet_row[index].endswith('" ')):
                sheet_row[index] = sheet_row[index][1: len(sheet_row[index]) - 1]
            if sheet_row[index].startswith('"') and sheet_row[index].endswith(''):
                sheet_row[index] = sheet_row[index][1: len(sheet_row[index])]
            if sheet_row[index].startswith('“') and '” ' not in sheet_row[index]:
                sheet_row[index] = sheet_row[index][1: len(sheet_row[index])]
            # 再次移除逗号
            if sheet_row[index].endswith(',') or sheet_row[index].endswith('，'):
                sheet_row[index] = sheet_row[index][0: len(sheet_row[index]) - 1]
            if sheet_row[index].startswith('"') or sheet_row[index].startswith('“') or sheet_row[index].startswith('”'):
                print('parse_execl========>[%s]' % sheet_row[index])
                # print('parse_execl========>“    ”========>%s' % sheet_row[index])  # print(sheet_row)
    return execl_rows


# 将execl文件数据写入csv文件
# 此处采用的是追加机制
# 因为execl文件有多个sheet，要逐一写入
def write_csv(csv_name, data_rows):
    with open(csv_name, 'w', encoding='utf-8') as file:
        csv_write = csv.writer(file)
        csv_write.writerows(data_rows)


# 读dart文件的内容
def parse_dart(filename):
    file = open(filename, encoding='utf-8')
    line_list = []
    line = file.readline()
    while line:
        line_list.append(line)
        line = file.readline()
    file.close()
    return line_list


# 解析dart文件内容
# 因为要处理代码格式化导致的换行
# 所以放弃while的性能
def read_dart(filename):
    line_list = []
    file = open(filename, encoding='utf-8')
    lines = file.readlines()
    key_pre = ''
    for line in lines:
        if line.endswith(':\n'):
            key_pre = line.rstrip('\n')
            continue
        if len(key_pre):
            line = key_pre + line.strip()
            key_pre = ''
        line_list.append(line)
    file.close()
    return line_list


# 数据写入dart文件
def write_file(filename, sheet_row):
    # for line in sheet_row:
    #     print("=====write_dart=====", line, filename, end='')
    file = open(filename, 'w', encoding='utf-8')
    # lists = [line + "\n" for line in sheet_row]
    file.writelines(sheet_row)
    file.close()
    print("======write_dart======", filename + "写入完成")


# 将翻译内容和dart文件的key-value比对
def merge_trans(dart_file, trans_data):
    trans_lines = []
    result_lines = []
    dart_lines = read_dart(dart_file)
    for dart_line in dart_lines:
        if ':' in dart_line and not dart_line.startswith('//') and configs.dart_ext not in dart_line:
            real_line = parse_value(dart_line)
            # 匹配翻译内容是否有这个数据
            for trans in trans_data:
                if trans[0] == def_value and trans[1] == def_value:
                    continue
                row_origin = str(trans[0]).strip()
                if row_origin == real_line.strip():
                    row_replace = trans[1]
                    if len(trans) >= 3 and trans[2] != def_value:
                        # 有校对的那一列数据
                        row_replace = trans[2]
                    # 内容替换, 判断是否有翻译或者校对
                    if row_replace == def_value:
                        continue
                    # print("merge_dart======>", real_line, row_origin)
                    dart_line = dart_line.replace(real_line, row_origin)
                    trans_lines.append(dart_line)  # 将修改过的数据添加到源数据
            result_lines.append(dart_line)
    write_file(dart_file, result_lines)
    # write_file(dart_file + ".txt", list(set(result_lines).difference(set(trans_lines))))


def parse_value(full_line):
    dart_value = full_line.split(':')
    real_line = dart_value[1]
    if real_line.endswith(',\n'):
        real_line = real_line.rstrip('\n')
    if '//' in real_line:
        real_line = real_line.split('//')[0]
    if real_line.startswith('"') and real_line.endswith('"'):
        print("parse_value========>[%s]" % real_line)
        real_line = real_line[1, len(real_line) - 1]
    if real_line.startswith("'") and real_line.endswith("'"):
        real_line = real_line[1, len(real_line) - 1]
    if real_line.endswith(','):
        real_line = real_line.rstrip(',')
    if real_line.startswith('《') and real_line.endswith('《'):
        real_line = real_line[1, len(real_line) - 1]
    return real_line


# 遍历指定目录下的指定前缀和后缀文件
def find_files(path, pre, ext):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith(pre) and file.endswith(ext) and 'url' not in file:
                fullname = os.path.join(root, file)
                yield fullname


# 解析csv文件
def parse_csv(filename):
    csv_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spam_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spam_reader:
            csv_data.append(row)
    return csv_data


# 开始比较文件的内容
# 每一种语言对应一个execl表格
def compare_content(root_path):
    lang_china = find_files(root_path, 'zh_hans', configs.dart_ext)
    for execl in find_files(root_path, '', '.%s' % execl_ext):
        print('compare_content======>', execl)
        data_rows = parse_execl(execl)
        file_name = execl.replace(execl_ext, 'csv')
        # 判断文件存在并且有内容时先删除文件
        if os.path.exists(file_name) and not os.path.getsize(file_name):
            os.remove(file_name)
        write_csv(file_name, data_rows)
        prefix = ''
        if 'japanese' in execl.lower():
            prefix = 'ja_jp'
        elif 'korea' in execl.lower():
            prefix = 'ko_kr'
        elif 'english' in execl.lower():
            prefix = 'en_us'

        # 处理dart文件
        for dart_file in find_files(root_path, prefix, configs.dart_ext):
            compare_dart(dart_file, prefix, lang_china)
            # 合并替换翻译
            merge_trans(dart_file, data_rows)
            # 日语存在问题（非繁体存在统计错误）
            filter_trans(dart_file, prefix)


# 解析未翻译的内容, 过滤掉已经翻译的
def filter_trans(filename, prefix):
    un_trans_lines = []
    dart_lines = read_dart(filename)
    for line_tmp in dart_lines:
        if line_tmp.strip().startswith('//'):
            continue
        if configs.dart_ext in line_tmp:
            continue
        if ':' not in line_tmp:
            continue
        if '* @' in line_tmp:
            continue
        key_value = line_tmp.split(':')
        real_line = key_value[1]
        if '//' in real_line:
            real_line = real_line.split('//')[0]
        if '\n' in real_line:
            real_line = real_line.replace('\n', '')
        if '==' in real_line:
            continue
        lang = language.judge_lang(real_line)
        if ('en_us' == prefix and 'zh' in lang) or (lang == 'zh' and language.string_convert(real_line)):
            real_value = key_value[1]
            if '"' in real_value:
                real_value = real_value.replace('"', '')
            if "'" in real_value:
                real_value = real_value.replace("'", '')
            if ',' in real_value:
                real_value = real_value.replace(',', '')
            real_value = real_value.strip(' ')
            un_trans_lines.append(real_value)  # else:  # print("filter_trans======>%s, %s" % (lang, line_tmp))
    file_name = filename + ".txt"
    if os.path.exists(file_name) and not os.path.getsize(file_name):
        os.remove(file_name)
    if len(un_trans_lines):
        un_trans_lines.append("\n\n\n未翻译数量：%d" % len(un_trans_lines))
        write_file(file_name, un_trans_lines)


# 比对相同语言包下的对应文件是否有缺失
# 以中文为模板
def compare_dart(dart_file, prefix, china_langs):
    dart_lines = read_dart(dart_file)
    dart_keys = []
    for dart_line in dart_lines:
        lang_key = parse_key(dart_line)
        if len(lang_key):
            dart_keys.append(lang_key)
    china_keys = []
    china_lines = []
    for china_lang in china_langs:
        temp_suffix = china_lang.replace('zh_hans', prefix)
        if dart_file == temp_suffix:
            china_lines = read_dart(china_lang)
            for china_line in china_lines:
                china_key = parse_key(china_line)
                if len(china_key):
                    china_keys.append(china_key)
            break
    results = list(set(dart_keys) ^ set(china_keys))
    # results = list(set(dart_keys).intersection(set(china_keys)))
    print('merge_list======>', results)
    if len(results):
        if len(china_keys) - len(dart_keys):
            merge_list(china_lines, dart_lines, results, dart_file)
            # else:
            print("merge_list========", results)  # merge_list(dart_lines, china_lines, results, dart_file)
    else:
        print("merge_list======>key的个数相同")


# 合并两个列表
def merge_list(lang_list, short_list, results, dart_file):
    diff_lines = []
    for result in results:
        for china_line in lang_list:
            if result.strip() == parse_key(china_line):
                diff_lines.append(china_line)
    if len(diff_lines):
        insert_index = 0
        for index in range(len(short_list) - 1, -1, -1):
            if '};' == short_list[index].strip():
                insert_index = index
        diff_lines.append("%s// 同步存在差异的内容\n" % (' ' * 4))
        for diff_line in diff_lines:
            short_list.insert(insert_index, diff_line)
        # write_file(dart_file + '.txt', short_list)
        write_file(dart_file, short_list)


# 格式化key
def parse_key(string):
    if string.strip().startswith('//'):
        return ''
    if configs.dart_ext in string:
        return ''
    if ':' not in string:
        return ''
    if '* @' in string:
        return ''
    lang_key = string.split(':')[0]
    if '"' in lang_key:
        lang_key = lang_key.replace('"', '')
    if "'" in lang_key:
        lang_key = lang_key.replace("'", '')
    return lang_key.strip()


def find_project(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(configs.dart_ext):
                fullname = os.path.join(root, file)
                yield fullname


def find_unused(trans_file, project_dir):
    used_lines = []
    dart_lines = read_dart(trans_file)
    trans_files = find_project(project_dir)
    for trans_file in trans_files:

        file = open(trans_file, "r", encoding='utf-8')
        file_lines = file.readlines()
        for file_line in file_lines:
            for dart_line in dart_lines:
                if dart_line.strip().startswith('//'):
                    continue
                if configs.dart_ext in dart_line:
                    continue
                if ':' not in dart_line:
                    continue
                if '* @' in dart_line:
                    continue
                key_value = dart_line.split(':')
                real_value = key_value[0].strip()
                if ('%s.tr' % real_value) in file_line and dart_line not in used_lines:
                    used_lines.append(dart_line)
        print(trans_file, len(used_lines))
    write_file('../trans_used.txt', used_lines)


def compare_keys(china_file, dart_file):
    dart_lines = read_dart(dart_file)
    dart_keys = []
    for dart_line in dart_lines:
        lang_key = parse_key(dart_line)
        if len(lang_key):
            dart_keys.append(lang_key)
    china_keys = []
    china_lines = read_dart(china_file)
    for china_line in china_lines:
        china_key = parse_key(china_line)
        if len(china_key):
            china_keys.append(china_key)
    results = list(set(dart_keys).intersection(set(china_keys)))
    print('merge_list======>', results)
    final_lines = []
    if len(results):
        for dart_line in dart_lines:
            if ':' in dart_line and not dart_line.startswith('//') and configs.dart_ext not in dart_line:
                lang_key = parse_key(dart_line)
                if lang_key not in results or dart_line in final_lines:
                    continue
                final_lines.append(dart_line)
            else:
                final_lines.append(dart_line)
    else:
        print("merge_list======>key的个数相同")
    write_file(dart_file, final_lines)


if __name__ == '__main__':
    # read_dart(".\common\ja_jp.dart")
    # all_data = read_xls('japanese.xls')
    # print(all_data)
    compare_content('..')  # find_unused('zh_hans.dart', "D:/Workspace/nr_p2_global")  # compare_keys('./common/zh_hans.dart', './common/ko_kr.dart')
