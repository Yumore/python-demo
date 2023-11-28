import os
import time
from sqlite3 import OperationalError

import numpy
import pandas
import xlrd
import xlsxwriter as xlsxwriter
import xlwt

from utility import fileUtils, configs, dartUtils, typeutil, sqliteUtils, langUtils


# 开始比较文件的内容
# 每一种语言对应一个execl表格
def parse_translate(root_path):
    for execl_file in fileUtils.find_execl(root_path, configs.execl_ext):
        fileUtils.format_logger('compare_content', execl_file)
        table_name = "chinese"
        if 'japanese' in execl_file.lower():
            table_name = 'japanese'
        elif 'korea' in execl_file.lower():
            table_name = 'korea'
        elif 'english' in execl_file.lower():
            table_name = 'english'
        sql_string = "CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY, chinese TEXT NOT NULL, translated TEXT NOT NULL, proofread TEXT, sheetname TEXT, timenow INTEGER DEFAULT 0);".format(
            table_name)
        sqliteUtils.create_table(sql_string)
        parse_execl(execl_file, table_name)
    merge_translate(root_path)


# 解析现有的翻译execl文件
# 并对数据进行格式化处理
# 方便后期做数据校对和匹配
def parse_execl(file_name, table_name):
    data_index = 0
    workbooks = xlrd.open_workbook(file_name)
    sheet_names = workbooks.sheet_names()
    for sheet_index in range(len(workbooks.sheets())):
        # important = 1 if 'p2' in sheet_names[sheet_index] or 'P2' in sheet_names[sheet_index] else 0
        # sheet_rows =  workbooks.sheet_by_name(sheet_names[sheet_index]).get_rows()
        # fileUtils.format_logger('parse_execl', [sheet_names[sheet_index], important])
        sheet = workbooks.sheet_by_name(sheet_names[sheet_index])
        for row_index in range(0, sheet.nrows):
            # 处理· ・ TODO 因为要一一对应所以要单独处理
            # sheet_row = [sheet_object.row_values(row) for row in range(sheet_object.nrows)]
            sheet_row = sheet.row_values(row_index)
            if not len(sheet_row[0]) or not len(sheet_row[0].strip()):
                continue
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
                        string_array.append(configs.def_value)
                    else:
                        string_array.append(str_b[index])
                    trim_data(string_array, table_name, data_index, sheet_names[sheet_index])
                    data_index += 1
            else:
                trim_data(sheet_row, table_name, data_index, sheet_names[sheet_index])
                data_index += 1
    fileUtils.format_logger('parse_execl', '%s, 数组总数：%d, 表格sheet数量：%d' % (file_name, data_index, len(sheet_names)))


def read_xls(file_name):
    # """解决读取XLS文件出现警告，并且无法获取数据的问题"""
    workbooks = xlrd.open_workbook(file_name)
    sheet_names = workbooks.sheet_names()
    all_datas = {}
    for sheet_name in sheet_names:
        data_sheet = workbooks.sheet_by_name(sheet_name)
        sheet_rows = 1
        sheet_cols = 0
        while 1:
            try:
                data_row = data_sheet.row_values(sheet_rows)
            except IOError:
                break
            else:
                sheet_rows = sheet_rows + 1
                sheet_cols = max(sheet_cols, len(data_row))

        # columns 为XLS文件第一行
        columns = data_sheet.row_values(0) + ['Unnamed:' + str(i) for i in range(1, sheet_cols - len(data_sheet.row_values(0)) + 1)]
        data_newer = []
        for row_index in range(1, sheet_rows):
            value_index = data_sheet.row_values(row_index)
            # 当表格中有行合并时，获取此行数据时：
            #   参与合并的单元格中最左边单元个内容 = 合并单元格中内容
            #   其他参与合并的单元个为空或者不显示，因此这些单元格填充为np.nan
            #   保证每行的长度=列数
            value_index = [numpy.nan if j == "" else j for j in value_index]
            row_supplement = value_index + [numpy.nan] * (sheet_cols - len(value_index))
            data_newer.append(row_supplement)

        data_frame = pandas.DataFrame(data_newer, columns=columns)
        all_datas[sheet_name] = data_frame
    return all_datas


# 修正数据
def trim_data(execl_row, table_name, data_index, sheet_name):
    # 移除 \n “ " ' 【】 []
    for index in range(len(execl_row)):
        if pandas.isnull(execl_row[index]):
            execl_row[index] = configs.def_value
        execl_row[index] = execl_row[index].strip('')
        if dartUtils.key_included(execl_row[index]):
            execl_row[index] = dartUtils.parse_value(execl_row[index])
        # 第一次移除逗号
        if execl_row[index].endswith(',') or execl_row[index].endswith('，'):
            execl_row[index] = execl_row[index][0: len(execl_row[index]) - 1]
        if execl_row[index].startswith('"') and execl_row[index].endswith('"'):
            execl_row[index] = execl_row[index].lstrip('"').rstrip('"')
        if execl_row[index].startswith("'") and execl_row[index].endswith("'"):
            execl_row[index] = execl_row[index].lstrip("'").rstrip("'")
        # TODO 奇奇怪怪的符号组合
        if (execl_row[index].startswith('“') or execl_row[index].startswith('”')) and (execl_row[index].endswith('”') or execl_row[index].endswith('“')):
            execl_row[index] = execl_row[index].lstrip('“').lstrip('”').rstrip('”').rstrip('“')
        # TODO 奇奇怪怪的符号组合
        execl_row[index] = execl_row[index].strip('')
        if execl_row[index].startswith('"') and (execl_row[index].endswith('”') or execl_row[index].endswith('“')):
            execl_row[index] = execl_row[index].lstrip('"').rstrip('”').rstrip('“')
        if execl_row[index].startswith('"') and execl_row[index].endswith(''):
            execl_row[index] = execl_row[index].lstrip('"').rstrip('')
        if execl_row[index].startswith('“') and '” ' not in execl_row[index]:
            execl_row[index] = execl_row[index].lstrip('“')
        # 再次移除逗号
        if execl_row[index].endswith(','):
            execl_row[index] = execl_row[index].rstrip(',')
        if execl_row[index].endswith('，'):
            execl_row[index] = execl_row[index].rstrip('，')
        if execl_row[index].startswith('"') or execl_row[index].startswith('“') or execl_row[index].startswith('”'):
            fileUtils.format_logger('trim_data', execl_row[index])
        if "'" in execl_row[index]:
            execl_row[index] = execl_row[index].replace("'", '’')
        if execl_row[index].startswith('：'):
            execl_row[index] = execl_row[index].lstrip('：')
        if execl_row[index].startswith('【') and execl_row[index].endswith('】'):
            execl_row[index] = execl_row[index].lstrip('【').rstrip('】')
        if execl_row[index].startswith('[') and execl_row[index].endswith(']'):
            execl_row[index] = execl_row[index].lstrip('[').rstrip(']')
        if execl_row[index].startswith('「') and execl_row[index].endswith('」'):
            execl_row[index] = execl_row[index].lstrip('「').rstrip('」')
        execl_row[index] = execl_row[index].lstrip()
    proofread = configs.def_value
    if len(execl_row) > 2:
        proofread = execl_row[len(execl_row) - 1]
        proofread = proofread if len(proofread) else configs.def_value
        # fileUtils.format_logger('trim_data', proofread)
    if configs.def_value != execl_row[0]:
        timestamp = int(time.time() * 1000 * 1000)
        sqliteUtils.insert_data(table_name, data_index, execl_row[0], execl_row[1], proofread, sheet_name, timestamp)


def update_translate(root_path, prefix):
    table_name = '{0}_new'.format(prefix)
    filename = "{0}/{1}/{1}.xls".format(root_path, table_name, configs.execl_path)
    connect, cursor = sqliteUtils.open_connect()
    # 在查询之前先创建表
    sql_string = "CREATE TABLE IF NOT EXISTS {0} (local_key PRIMARY KEY, module TEXT, chinese TEXT, {1} TEXT);".format(table_name, prefix)
    fileUtils.format_logger('update_translate', sql_string)
    cursor.execute(sql_string)
    connect.commit()
    if os.path.exists(filename):
        execle_sheets = pandas.read_excel(filename, sheet_name=None, header=None).values()
        for execl_sheet in execle_sheets:
            for sheet_row in execl_sheet.values:
                data_list = sheet_row.tolist()
                if data_list[0] == 'key':
                    continue
                if len(data_list) > 4:
                    fileUtils.format_logger('update_translate====', data_list)
                if len(data_list) > 4 and not pandas.isnull(data_list[len(data_list) - 1]):
                    data_list[3] = data_list[len(data_list) - 1]
                # insert_sql = "UPDATE {0} SET chinese='{1}', english='{2}', japanese='{3}', korea='{4}' WHERE local_key='{5}';" \
                #     .format(table_name, table_value[1], table_value[2], table_value[3], table_value[4], table_value[0])
                insert_sql = "REPLACE INTO {0} (local_key, module, chinese, {1}) values ('{2}', '{3}','{4}', '{5}');".format(table_name, prefix, data_list[0], data_list[1], data_list[2], data_list[3])
                update_sql = "UPDATE translate SET module='{1}', {2}='{3}' WHERE local_key='{4}';".format(table_name, prefix, data_list[1], data_list[3], data_list[0])
                try:
                    cursor.execute(insert_sql)
                    # cursor.execute(update_sql)
                    connect.commit()
                except OperationalError:
                    fileUtils.format_logger('SQLite error: update_translate', insert_sql)
        sqliteUtils.close_connect(cursor, connect)
    else:
        fileUtils.format_logger('update_translate', '{0} 文件不存在'.format(filename))


def merge_translate(root_path):
    table_name = 'translate'
    sql_string = "CREATE TABLE IF NOT EXISTS {0} (local_key TEXT PRIMARY KEY, module TEXT, chinese TEXT, english TEXT, japanese TEXT, korea TEXT, tradition TEXT);".format(table_name)
    sqliteUtils.create_table(sql_string)
    filename = "{0}/{1}/{2}.xls".format(root_path, configs.execl_path, table_name)
    connect, cursor = sqliteUtils.open_connect()
    execle_sheets = pandas.read_excel(filename, sheet_name=None, header=None).values()
    for execl_sheet in execle_sheets:
        for sheet_row in execl_sheet.values:
            data_list = format_data(sheet_row.tolist())
            if data_list[0] == 'key':
                continue
            insert_sql = "REPLACE INTO {0} (local_key, module, chinese, english, japanese, korea) values ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}');".format(table_name, data_list[0], data_list[1],
                                                                                                                                                             data_list[2], data_list[3], data_list[4],
                                                                                                                                                             data_list[5])
            update_sql = "UPDATE {0} SET module='{1}', chinese='{2}', english='{3}', japanese='{4}', korea='{5}' WHERE local_key='{6}';".format(table_name, data_list[1], data_list[2], data_list[3],
                                                                                                                                                data_list[4], data_list[5], data_list[0])
            try:
                cursor.execute(insert_sql)
                connect.commit()
            except OperationalError as e:
                connect.rollback()
                fileUtils.format_logger('SQLite error: merge_translate', [insert_sql, e])
    sqliteUtils.close_connect(cursor, connect)


def format_data(data_list):
    real_data = []
    for data in data_list:
        if typeutil.typeof(data) != 'str':
            real_data.append('')
        elif "'" in data:
            real_data.append(data.replace("'", "’"))
        else:
            real_data.append(data)
    return real_data


def update_history(root_path, table_name):
    connect, cursor = sqliteUtils.open_connect()
    filename = "{0}/{1}/{2}.xls".format(root_path, configs.execl_path, 'results0812')
    execle_sheets = pandas.read_excel(filename, sheet_name=None, header=None).values()
    for execl_sheet in execle_sheets:
        for sheet_row in execl_sheet.values:
            data_list = sheet_row.tolist()
            update_sql = "UPDATE {0} SET optation='已校对', module='{1}' WHERE local_key='{2}';".format(table_name, data_list[0], data_list[1])
            try:
                cursor.execute(update_sql)
                connect.commit()
            except OperationalError as e:
                connect.rollback()
                fileUtils.format_logger('SQLite error: update_translate', [update_sql, e])
    sqliteUtils.close_connect(cursor, connect)


def update_tradition():
    connect, cursor = sqliteUtils.open_connect()
    tradition_sql = "SELECT local_key, local_value FROM tradition_local;"
    cursor.execute(tradition_sql)
    results = cursor.fetchall()
    for result in results:
        translate_sql = "UPDATE translate SET tradition='{0}' WHERE local_key='{1}';".format(result[1], result[0])
        cursor.execute(translate_sql)
        connect.commit()
    sqliteUtils.close_connect(cursor, connect)


def generate_result(root_path, tradition):
    if tradition:
        update_tradition()
    table_name = 'translate'
    connect, cursor = sqliteUtils.open_connect()
    query_sql = "SELECT * FROM {0}".format(table_name)
    cursor.execute(query_sql)
    table_values = cursor.fetchall()
    sqliteUtils.close_connect(cursor, connect)
    index = len(table_values)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('翻译总表')
    for i in range(0, index):
        for j in range(0, len(table_values[i])):
            sheet.write(i, j, table_values[i][j])
    file_path = "{0}/{1}/results.xls".format(root_path, configs.execl_path)
    workbook.save(file_path)
    fileUtils.format_logger('generate_result', '从翻译结果表导出数据成功：{0}'.format(file_path))


def generate_result(root_path, tradition):
    if tradition:
        update_tradition()
    table_name = 'translate'
    connect, cursor = sqliteUtils.open_connect()
    query_sql = "SELECT * FROM {0}".format(table_name)
    cursor.execute(query_sql)
    table_values = cursor.fetchall()
    sqliteUtils.close_connect(cursor, connect)
    index = len(table_values)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('翻译总表')
    for i in range(0, index):
        for j in range(0, len(table_values[i])):
            sheet.write(i, j, table_values[i][j])
    file_path = "{0}/{1}/results.xls".format(root_path, configs.execl_path)
    workbook.save(file_path)
    fileUtils.format_logger('generate_result', '从翻译结果表导出数据成功：{0}'.format(file_path))


def parse_position(headers, target):
    posix = -1
    for index, header in enumerate(headers):
        if header == target:
            posix = index
            break
    return posix


def generate_chart(headers):
    target = langUtils.chinese2pinyin("项目")
    projects = sqliteUtils.select_project(target)
    for project in projects:
        project_chart(project, target, headers)


def project_chart(project, target, headers):
    if configs.debuggable:
        fileUtils.format_logger("project_chart", headers)
    selections = langUtils.chinese2pinyin("状态")
    states = sqliteUtils.select_status(selections)
    status_datas = [["状态", project]]
    for state in states:
        count = sqliteUtils.count_status(project, target, selections, state)
        status_datas.append([state, count])
    fileUtils.format_logger("project_chart", status_datas)
    write_sheet("项目问题概览", status_datas)
    # status_groups = itertools.groupby(status_datas, key=lambda x: (x[position]))
    # for key, group in status_groups:
    #     fileUtils.format_logger("project_chart", [key, group])


def write_sheet(sheet_name, datas):
    execl_file = "{}/files/result.xlsx".format(os.getcwd())
    dataframe = pandas.DataFrame(data=datas)
    # writer = pandas.ExcelWriter(execl_file, engin='openpyxl')
    writer = pandas.ExcelWriter(execl_file)
    # book = openpyxl.reader.excel.load_workbook(writer.path)
    # writer.book = book
    dataframe.to_excel(writer, sheet_name, index=False, header=False)
    writer.close()
    fileUtils.format_logger("write_sheet", "{} has been wrote {}".format(execl_file, sheet_name))

    # generate_line(execl_file)
    # generate_bar(execl_file)
    generate_pie(execl_file)


def generate_line(filepath):
    workbook = xlsxwriter.Workbook(filepath)
    # 创建一个sheet
    worksheet = workbook.add_worksheet()
    # worksheet = workbook.add_worksheet("bug_analysis")
    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})
    headings = ['Number', 'testA', 'testB']
    headings = ['Number', 'testA', 'testB']
    data = [
        ['2017-9-1', '2017-9-2', '2017-9-3', '2017-9-4', '2017-9-5', '2017-9-6'],
        [10, 40, 50, 20, 10, 50],
        [30, 60, 70, 50, 40, 30],
    ]

    # 写入表头
    worksheet.write_row('A1', headings, bold)

    # 写入数据
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])
    # --------2、生成图表并插入到excel---------------
    # 创建一个柱状图(line chart)
    chart_col = workbook.add_chart({'type': 'line'})
    # 配置第一个系列数据
    chart_col.add_series({
        # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
        # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$7',
        'values': '=Sheet1!$B$2:$B$7',
        'line': {'color': 'red'},
    })
    # 配置第二个系列数据
    chart_col.add_series({
        'name': '=Sheet1!$C$1',
        'categories': '=Sheet1!$A$2:$A$7',
        'values': '=Sheet1!$C$2:$C$7',
        'line': {'color': 'yellow'},
    })
    # 配置第二个系列数据(用了另一种语法)
    # chart_col.add_series({
    #     'name': ['Sheet1', 0, 2],
    #     'categories': ['Sheet1', 1, 0, 6, 0],
    #     'values': ['Sheet1', 1, 2, 6, 2],
    #     'line': {'color': 'yellow'},
    # })
    # 设置图表的title 和 x，y轴信息
    chart_col.set_title({'name': 'The xxx site Bug Analysis'})
    chart_col.set_x_axis({'name': 'Test number'})
    chart_col.set_y_axis({'name': 'Sample length (mm)'})
    # 设置图表的风格
    chart_col.set_style(1)
    # 把图表插入到worksheet并设置偏移
    worksheet.insert_chart('A10', chart_col, {'x_offset': 25, 'y_offset': 10})
    workbook.close()


def generate_bar(filepath):
    # 创建一个excel
    workbook = xlsxwriter.Workbook(filepath)
    # 创建一个sheet
    worksheet = workbook.add_worksheet()
    # worksheet = workbook.add_worksheet("bug_analysis")

    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})

    # --------1、准备数据并写入excel---------------
    # 向excel中写入数据，建立图标时要用到
    headings = ['Number', 'testA', 'testB']
    data = [
        ['2017-9-1', '2017-9-2', '2017-9-3', '2017-9-4', '2017-9-5', '2017-9-6'],
        [10, 40, 50, 20, 10, 50],
        [30, 60, 70, 50, 40, 30],
    ]

    # 写入表头
    worksheet.write_row('A1', headings, bold)

    # 写入数据
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])

    # --------2、生成图表并插入到excel---------------
    # 创建一个柱状图(column chart)
    chart_col = workbook.add_chart({'type': 'column'})

    # 配置第一个系列数据
    chart_col.add_series({
        # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
        # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$7',
        'values': '=Sheet1!$B$2:$B$7',
        'line': {'color': 'red'},
    })

    # 配置第二个系列数据(用了另一种语法)
    chart_col.add_series({
        'name': '=Sheet1!$C$1',
        'categories': '=Sheet1!$A$2:$A$7',
        'values': '=Sheet1!$C$2:$C$7',
        'line': {'color': 'yellow'},
    })

    # 配置第二个系列数据(用了另一种语法)
    # chart_col.add_series({
    #     'name': ['Sheet1', 0, 2],
    #     'categories': ['Sheet1', 1, 0, 6, 0],
    #     'values': ['Sheet1', 1, 2, 6, 2],
    #     'line': {'color': 'yellow'},
    # })

    # 设置图表的title 和 x，y轴信息
    chart_col.set_title({'name': 'The xxx site Bug Analysis'})
    chart_col.set_x_axis({'name': 'Test number'})
    chart_col.set_y_axis({'name': 'Sample length (mm)'})

    # 设置图表的风格
    chart_col.set_style(1)

    # 把图表插入到worksheet以及偏移
    worksheet.insert_chart('A10', chart_col, {'x_offset': 25, 'y_offset': 10})
    workbook.close()


def generate_pie(filepath):
    # 创建一个excel
    workbook = xlsxwriter.Workbook(filepath)
    # 创建一个sheet
    worksheet = workbook.add_worksheet()

    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})

    # --------1、准备数据并写入excel---------------
    # 向excel中写入数据，建立图标时要用到
    data = [
        ['closed', 'active', 'reopen', 'NT'],
        [1012, 109, 123, 131],
    ]

    # 写入数据
    worksheet.write_row('A1', data[0], bold)
    worksheet.write_row('A2', data[1])

    # --------2、生成图表并插入到excel---------------
    # 创建一个柱状图(pie chart)
    chart_col = workbook.add_chart({'type': 'pie'})

    # 配置第一个系列数据
    chart_col.add_series({
        'name': 'Bug Analysis',
        'categories': '=Sheet1!$A$1:$D$1',
        'values': '=Sheet1!$A$2:$D$2',
        'points': [
            {'fill': {'color': '#00CD00'}},
            {'fill': {'color': 'red'}},
            {'fill': {'color': 'yellow'}},
            {'fill': {'color': 'gray'}},
        ],

    })

    # 设置图表的title 和 x，y轴信息
    chart_col.set_title({'name': 'Bug Analysis'})

    # 设置图表的风格
    chart_col.set_style(10)

    # 把图表插入到worksheet以及偏移
    worksheet.insert_chart('B10', chart_col, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
