#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
from zipfile import Path, ZipFile, ZIP_BZIP2

from utility import langUtils, sqliteUtils, fileUtils, configs, dartUtils, execlUtils, debug


def read_csv(file_path):
    headers = []
    data_rows = []
    with open(file_path, 'r', encoding='gbk') as file:
        csv_datas = csv.reader(file)
        for index, csv_data in enumerate(csv_datas):
            if index == 0:
                headers = csv_data
            if debug.debuggable():
                break
            else:
                data_rows.append(csv_data)
    if debug.debuggable():
        execlUtils.generate_chart(headers)
    else:
        insert_issues(headers, data_rows)


def insert_issues(headers, rows):
    keys = []
    sql_string = "CREATE TABLE IF NOT EXISTS issues ("
    for index, header in enumerate(headers):
        split = ', '
        if langUtils.filter_string(header) not in keys:
            keys.append(header)
        else:
            header += str(index)
        if index == (len(headers) - 1):
            split = ''
        if index == 0:
            sql_string += "pid TEXT PRIMARY KEY{}".format(split)
        else:
            sql_string += "{} TEXT{}".format(langUtils.chinese2pinyin(header, True), split)
    sql_string += ");"
    # fileUtils.format_logger("create_table", "keys is {}".format(keys))
    sqliteUtils.create_table(sql_string)
    for row in rows:
        sql_string = "REPLACE INTO issues VALUES ("
        for posix, detail in enumerate(row):
            split = ', '
            if posix == (len(headers) - 1):
                split = ''
            if "'" in detail:
                detail = detail.replace("'", '"')
            sql_string += "'{}'{}".format(detail, split)
        sql_string += ");"
        sqliteUtils.insert_issues(sql_string)

    execlUtils.generate_chart(headers)


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
            key_value = 'NRMessageLocaleKeys.{0}: "{1}",\n'.format(langUtils.chinese2pinyin(row), origin_row)
            line_list.append(key_value)
            real_key = 'static const {0} = \"{1}\";\n'.format(langUtils.chinese2pinyin(row), langUtils.chinese2pinyin(row))
            keys_list.append(real_key)
    # fileutil.format_logger('parse_csv', line_list)
    fileUtils.write_file('{0}/{1}/key_values.txt'.format(root_path, configs.execl_path), line_list)
    fileUtils.write_file('{0}/{1}/real_keys.txt'.format(root_path, configs.execl_path), keys_list)


def generate_keys(root_path):
    file_path = '{0}/j2/dingshi.dart'.format(root_path)
    keys_list = []
    for line in dartUtils.parse_dart(file_path):
        real_key = dartUtils.parse_key(line).split('.')
        keys_list.append('static const {0} = \"{1}\";\n'.format(real_key, real_key))
    fileUtils.write_file('{0}/{1}/real_keys.txt'.format(root_path, configs.execl_path), keys_list)


from utility.generators import TYPES_TO_GENERATORS
from utility.schemas import (
    CUSTOMERS_SCHEMA,
    PEOPLE_SCHEMA,
    ORGANIZATIONS_SCHEMA,
    PRODUCTS_SCHEMA,
    OFFERS_SCHEMA,
    LEADS_SCHEMA
)

SCHEMA_TO_DICT = {
    'customers': CUSTOMERS_SCHEMA,
    'leads': LEADS_SCHEMA,
    'people': PEOPLE_SCHEMA,
    'organizations': ORGANIZATIONS_SCHEMA,
    'products': PRODUCTS_SCHEMA,
    'offers': OFFERS_SCHEMA
}


def generate_file(schema='customers', name="customers", count=1000000):
    p = Path(__file__).parent / "../files/{}".format(schema)
    p.mkdir(parents=True, exist_ok=True)

    file_name = "{}.csv".format(name)
    file_path = p / file_name

    if not file_path.exists():
        schema_dict = SCHEMA_TO_DICT[schema]

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # Headers
            headers = [elem['name'] for elem in schema_dict]
            headers.insert(0, "Index")  # Add an Index header
            writer.writerow(headers)

            # Content
            data_generators = [TYPES_TO_GENERATORS[elem['type']] for elem in schema_dict]

            rows = []
            for index in range(1, count + 1):
                row = [gen() for gen in data_generators]
                row.insert(0, index)
                rows.append(row)

                if index % 1000 == 0:
                    writer.writerows(rows)
                    rows = []

                if index % 10000 == 0:
                    print("{}/{}".format(index, count))

            writer.writerows(rows)
    else:
        print("{} already exists".format(file_path))

    # Create a zip version
    file_name_zip = "{}.zip".format(name)
    file_path_zip = p / file_name_zip
    if not file_path_zip.exists():
        with ZipFile(file_path_zip, 'w', ZIP_BZIP2) as zipObj:
            zipObj.write(filename=file_path, arcname=file_name)


if __name__ == '__main__':
    generate_file('customers', 'customers-100', 100)
    generate_file('customers', 'customers-1000', 1000)
    generate_file('customers', 'customers-10000', 10000)
    generate_file('customers', 'customers-100000', 100000)
    generate_file('customers', 'customers-500000', 500000)
    generate_file('customers', 'customers-1000000', 1000000)
    generate_file('customers', 'customers-2000000', 2000000)

    generate_file('leads', 'leads-100', 100)
    generate_file('leads', 'leads-1000', 1000)
    generate_file('leads', 'leads-10000', 10000)
    generate_file('leads', 'leads-100000', 100000)

    generate_file('people', 'people-100', 100)
    generate_file('people', 'people-1000', 1000)
    generate_file('people', 'people-10000', 10000)
    generate_file('people', 'people-100000', 100000)
    generate_file('people', 'people-500000', 500000)
    generate_file('people', 'people-1000000', 1000000)
    generate_file('people', 'people-2000000', 2000000)

    generate_file('organizations', 'organizations-100', 100)
    generate_file('organizations', 'organizations-1000', 1000)
    generate_file('organizations', 'organizations-10000', 10000)
    generate_file('organizations', 'organizations-100000', 100000)
    generate_file('organizations', 'organizations-500000', 500000)
    generate_file('organizations', 'organizations-1000000', 1000000)
    generate_file('organizations', 'organizations-2000000', 2000000)

    generate_file('products', 'products-5000', 5000)
    generate_file('offers', 'offers-5000', 5000)
