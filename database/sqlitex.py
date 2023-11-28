###########################################
# 只提供数据库的增删改查的基本操作
###########################################

import configparser
import os
import sqlite3
from sqlite3 import OperationalError

from poprogress import simple_progress

from configs import configs
from utility import fileUtils, chartUtils, langUtils


def open_connect():
    database = configs.database
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    return connect, cursor


def close_connect(cursor, connect):
    cursor.close()
    connect.close()


def create_table(sql_string: str):
    connect, cursor = open_connect()
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError as e:
        connect.rollback()
        fileUtils.format_logger('SQLite error: create_table', [sql_string, e])
    close_connect(cursor, connect)


def show_table(table_name: str):
    connect, cursor = open_connect()
    fileUtils.format_logger('show_table', table_name)
    cursor.execute("PRAGMA table_info({}})".format(table_name))
    fileUtils.format_logger('show_table', cursor.fetchall())
    close_connect(cursor, connect)


def insert_datas(sql_string: str, params=None):
    connect, cursor = open_connect()
    counts = 0
    try:
        if params is None:
            cursor.execute(sql_string)
        elif params is list:
            cursor.executemany(sql_string, params)
        else:
            cursor.execute(sql_string, params)
        counts = connect.total_changes
        connect.commit()
    except OperationalError as e:
        connect.rollback()
        fileUtils.format_logger('SQLite error: insert_datas', [sql_string, params, counts, e])
    close_connect(cursor, connect)


# 先查翻译文档中是否有这个中文的
# 再查对应的key的值
def query_datas(sql_string: str, params=None):
    connect, cursor = open_connect()
    results = []
    try:
        if params is list:
            cursor.executemany(sql_string, params)
        else:
            cursor.execute(sql_string)
        results = cursor.fetchall()
    except OperationalError as e:
        fileUtils.format_logger('SQLite error: query_datas', [sql_string, params, e])
    close_connect(cursor, connect)
    fileUtils.format_logger('SQLite: query_datas', [sql_string, params, results])
    return results


def update_data(table_name: str, select_key, select_val, changes: dict):
    connect, cursor = open_connect()
    sql_string = "UPDATE {0} SET ".format(table_name)
    # for key, value in zip(dict.keys(), dict.values()):
    for key, value in changes.items():
        if value is int or value is float:
            sql_string += "{0}={1}".format(key, value)
        else:
            sql_string += "{0}='{1}'".format(key, value)
    sql_string += "WHERE {0}='{1}';".format(select_key, select_val)
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError as e:
        connect.rollback()
        fileUtils.format_logger('SQLite error: update_data', [sql_string, e])
    close_connect(cursor, connect)


def replace_data(sql_string, params: None):
    connect, cursor = open_connect()
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError as e:
        # 遇到问题之后回滚此次提交
        connect.rollback()
        fileUtils.format_logger("replace_data", [sql_string, e])
    close_connect(cursor, connect)

def parse_cfg(section, key, default_value):
    conf_parser = configparser.ConfigParser()
    conf_parser.read('configs.cfg', encoding='utf8')
    if not conf_parser.get(section, key):
        return default_value
    else:
        return conf_parser.get(section, key)


def select_project(target):
    connect, cursor = open_connect()
    sql_string = "SELECT DISTINCT {} FROM issues;".format(target)
    projects = []
    try:
        cursor.execute(sql_string)
        results = cursor.fetchall()
        # fileUtils.format_logger("select_project", [results, results[len(results) - 1]])
        for result in results:
            if result[len(result) - 1] not in projects:
                fileUtils.format_logger("select_project", result[len(result) - 1])
                projects.append(result[len(result) - 1])
    except OperationalError as e:
        connect.rollback()
        fileUtils.format_logger('SQLite error: select_project', [sql_string, e])
    close_connect(cursor, connect)
    return projects


def select_status(target):
    connect, cursor = open_connect()
    sql_string = "SELECT DISTINCT {} FROM issues;".format(target)
    status = []
    try:
        cursor.execute(sql_string)
        results = cursor.fetchall()
        # fileUtils.format_logger("select_project", [results, results[len(results) - 1]])
        for result in results:
            if result[len(result) - 1] not in status:
                # fileUtils.format_logger("select_status", result[len(result) - 1])
                status.append(result[len(result) - 1])
    except OperationalError as e:
        connect.rollback()
        fileUtils.format_logger('SQLite error: select_status', [sql_string, e])
    close_connect(cursor, connect)
    return status


def count_status(project, target, selections, status):
    connect, cursor = open_connect()
    sql_string = "SELECT COUNT(*) FROM issues WHERE {} = '{}' AND {} = '{}';".format(target, project, selections, status)
    count = 0
    try:
        cursor.execute(sql_string)
        results = cursor.fetchall()
        fileUtils.format_logger("select_project", [sql_string, results])
        if len(results):
            result = results[len(results) - 1]
            count = result[len(result) - 1]
    except OperationalError as e:
        connect.rollback()
        fileUtils.format_logger('SQLite error: select_status', [sql_string, e])
    close_connect(cursor, connect)
    return count


def query_depart(employee):
    sql_string = "SELECT depart FROM {} WHERE employee='{}';".format(configs.departTable, employee)
    connect, cursor = open_connect()
    depart = "第三方"
    try:
        cursor.execute(sql_string)
        results = cursor.fetchone()
        if results is not None and len(results):
            depart = results[len(results) - 1]
    except OperationalError as e:
        fileUtils.format_logger("query_depart", [sql_string, e])
    close_connect(cursor, connect)
    # fileUtils.format_logger("query_depart", "{} ==> {}".format(employee, depart))
    return depart


################################
# 查询所有项目，因不确定是否有多个项目
# 项目、状态、优先级别，人员
# 这几列的数据可以去重得到
# 所以不再单独写查询语句
################################
def query_distinct(selections, table_name=configs.issueTable):
    sql_string = "SELECT DISTINCT {} FROM {};".format(selections, table_name)
    connect, cursor = open_connect()
    datas = []
    try:
        cursor.execute(sql_string)
        results = cursor.fetchall()
        # fileUtils.format_logger("query_distinct", results)
        if len(results):
            for result in results:
                data = result[len(result) - 1]
                if data not in datas:
                    datas.append(data)
    except OperationalError as e:
        fileUtils.format_logger("query_distinct", [sql_string, e])
    close_connect(cursor, connect)
    return datas


#######################################
# 根据项目的优先级、问题状态计数是同类查询语句
# 所以不再重写多余的sql
# 例如：
# 1.根据项目查询所属模块下的问题优先级
# 2.根据项目查询所属模块下问题的状态
# 3.根据项目查询每个人的问题优先级
# 4.根据项目查询每个人的问题的状态
#######################################
def query_count(selections: list, arguments: list):
    if len(selections) != len(arguments):
        fileUtils.format_logger("query_count", "selections is {}, arguments is {}".format(selections, arguments))
        return 0
    sql_string = "SELECT COUNT(*) FROM {} WHERE".format(configs.issueTable)
    for index in range(len(selections)):
        split = " AND"
        if index == (len(selections) - 1):
            split = ""
        sql_string += " {} = '{}'{}".format(selections[index], arguments[index], split)
    sql_string += ";"
    connect, cursor = open_connect()
    status_count = 0
    try:
        cursor.execute(sql_string)
        results = cursor.fetchone()
        # fileUtils.format_logger("query_count", "{} result is {}".format(arguments, results))
        if len(results):
            status_count = results[len(results) - 1]
    except OperationalError as e:
        fileUtils.format_logger("query_count", [sql_string, e])
    close_connect(cursor, connect)
    return status_count


def update_issues(headers, datas, xls_path):
    fileUtils.format_logger("update_issues", "开始创建表并插入数据")
    keys = []
    sql_string = "CREATE TABLE IF NOT EXISTS {} (".format(configs.issueTable)
    for posix, header in enumerate(headers):
        if header is None:
            break
        if posix == 0:
            sql_string += "pid TEXT PRIMARY KEY,  "
        else:
            header = langUtils.filter_string(header)
            if header not in keys:
                keys.append(header)
            else:
                header += str(posix)
            header = langUtils.chinese2pinyin(header)
            split = ', '
            if posix == (len(headers) - 1):
                split = ''
            sql_string += "{} TEXT{}".format(header, split)
    sql_string += ");"
    create_table(sql_string)
    for row in simple_progress(datas, desc='插入数据进度'):
        sql_string = "REPLACE INTO {} VALUES(".format(configs.issueTable)
        for posix, detail in enumerate(row):
            split = ', '
            if posix == (len(headers) - 1):
                split = ''
            sql_string += "'{}'{}".format(langUtils.filter_quotation(detail), split)
        sql_string += ");"
        replace_data(sql_string)
    chartUtils.parse_datas(headers, xls_path)
    fileUtils.parse_depart("{}/depart.csv".format(os.getcwd()))
    fileUtils.format_logger("update_issues", "创建表并插入数据結束")

