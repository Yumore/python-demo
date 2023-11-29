###########################################
# 只提供数据库的增删改查的基本操作
###########################################

import configparser
import sqlite3
from sqlite3 import OperationalError

from configs import configs
from utility import loggerx


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
        loggerx.logger('SQLite error: create_table', [sql_string, e])
    close_connect(cursor, connect)


def show_table(table_name: str):
    connect, cursor = open_connect()
    loggerx.logger('show_table', table_name)
    cursor.execute("PRAGMA table_info({}})".format(table_name))
    loggerx.logger('show_table', cursor.fetchall())
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
        loggerx.logger('SQLite error: insert_datas', [sql_string, params, counts, e])
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
        loggerx.logger('SQLite error: query_datas', [sql_string, params, e])
    close_connect(cursor, connect)
    loggerx.logger('SQLite: query_datas', [sql_string, params, results])
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
        loggerx.logger('SQLite error: update_data', [sql_string, e])
    close_connect(cursor, connect)


def replace_data(sql_string, params: None):
    connect, cursor = open_connect()
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError as e:
        # 遇到问题之后回滚此次提交
        connect.rollback()
        loggerx.logger("replace_data", [sql_string, e])
    close_connect(cursor, connect)


def parse_cfg(section, key, default_value):
    conf_parser = configparser.ConfigParser()
    conf_parser.read('configs.cfg', encoding='utf8')
    if not conf_parser.get(section, key):
        return default_value
    else:
        return conf_parser.get(section, key)
