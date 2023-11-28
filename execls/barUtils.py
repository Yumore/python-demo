import matplotlib.pyplot as plt
import numpy
import pandas
import pandas as pd
import xlrd
import xlsxwriter


def create_bar():
    xlsxFile = "D:\\data-process\\项目7003A过滤器的数据.xlsx"
    df = pd.read_excel(xlsxFile, sheet_name='模块紧急问题数')
    df.sort_values(by='问题数', ascending=False, inplace=True)
    # df.plot(kind='bar')
    df.plot.bar(x='模块', y='问题数')
    print(df.plot)
    # plt.rcParams['font.family'] = 'SimHei'
    # 解决标签乱码
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()
    # writer = pd.ExcelWriter(xlsxFile, engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='模块紧急问题数', startrow=5, startcol=5)
    # writer._save()


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


def parse_position(headers, target):
    posix = -1
    for index, header in enumerate(headers):
        if header == target:
            posix = index
            break
    return posix


def generate_line(filepath, datas):
    workbook = xlsxwriter.Workbook(filepath)
    # 创建一个sheet
    worksheet = workbook.add_worksheet()
    # worksheet = workbook.add_worksheet("bug_analysis")
    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})
    for index, data in enumerate(datas):
        if index == 0:
            # 写入表头
            worksheet.write_row('A1', data, bold)
        else:
            # 写入数据
            worksheet.write_column('A{}'.format(index + 1), data)
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
