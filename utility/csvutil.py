import csv

import pypinyin

from utility import dartutil, fileutil, configs, language


def convert_csv2py(root_path, full_file):
    filename = '{0}/{1}/{2}'.format(root_path, configs.execl_path, full_file)
    csv_file = open(filename, 'r', encoding='utf-8')
    line_list = []
    keys_list = []
    for row_data in csv.reader(csv_file):
        # fileutil.format_logger('parse_csv', row_data)
        for row in row_data:
            if '-' == row:
                continue
            origin_row = row
            if '：' in row:
                row = row.replace('：', '')
            if 'XXX' in origin_row:
                replace_str = '@robotName'
                if '【' not in origin_row:
                    replace_str = '【{0}】'.format(replace_str)
                origin_row = origin_row.replace('XXX', replace_str)
            if 'xx：xx' in origin_row:
                origin_row = origin_row.replace('xx：xx', '@time')
            if 'xx:xx' in origin_row:
                origin_row = origin_row.replace('xx:xx', '@time')
            key_value = 'NRMessageLocaleKeys.{0}: "{1}",\n'.format(chinese_pinyin(language.filter_string(row)), origin_row)
            line_list.append(key_value)
            real_key = 'static const {0} = \"{1}\";\n'.format(chinese_pinyin(language.filter_string(row)), chinese_pinyin(language.filter_string(row)))
            keys_list.append(real_key)
    # fileutil.format_logger('parse_csv', line_list)
    fileutil.write_file('{0}/{1}/key_values.txt'.format(root_path, configs.execl_path), line_list)
    fileutil.write_file('{0}/{1}/real_keys.txt'.format(root_path, configs.execl_path), keys_list)


def generate_keys(root_path):
    file_path = '{0}/j2/dingshi.dart'.format(root_path)
    keys_list = []
    for line in dartutil.parse_dart(file_path):
        real_key = dartutil.parse_key(line).split('.')
        keys_list.append('static const {0} = \"{1}\";\n'.format(real_key, real_key))
    fileutil.write_file('{0}/{1}/real_keys.txt'.format(root_path, configs.execl_path), keys_list)


def chinese_pinyin(chinese_string):
    result = ''.join(pypinyin.lazy_pinyin(chinese_string, style=pypinyin.Style.FIRST_LETTER))
    return result
