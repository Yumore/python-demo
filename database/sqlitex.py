###########################################
# 只提供数据库的增删改查的基本操作
###########################################

import configparser
import os.path
import sqlite3
from sqlite3 import OperationalError

from utility import loggerx, configs


def open_connect():
    database = configs.database
    if not os.path.exists(database):
        datafile = open(database, "w")
        datafile.close()
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    return connect, cursor


def close_connect(cursor, connect):
    cursor.close()
    connect.close()


def create_tables(table_name: str, fields: list):
    sql_string = f"CREATE TABLE IF NOT EXISTS {table_name}("
    for field in fields:
        sql_string += f"{field['name']} {field['type']},"
    sql_string = sql_string.rstrip(',') + ")"
    create_table(sql_string)


def create_table(sql_string: str):
    connect, cursor = open_connect()
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError as e:
        connect.rollback()
        loggerx.logger('SQLite error: create_table', sql_string, e)
    close_connect(cursor, connect)


def show_table(table_name: str):
    connect, cursor = open_connect()
    loggerx.logger('show_table', table_name)
    sql_string = f"PRAGMA table_info({table_name})"
    cursor.execute(sql_string)
    loggerx.logger('show_table', cursor.fetchall())
    close_connect(cursor, connect)


def insert_datas(sql_string: str, params=None):
    connect, cursor = open_connect()
    # 关闭日志和同步
    # cursor.execute('''PRAGMA synchronous = OFF;''')
    # cursor.execute('''PRAGMA journal_mode = OFF;''')
    counts = 0
    try:
        if isinstance(params, tuple):
            cursor.execute(sql_string, params)
        elif isinstance(params, list):
            cursor.executemany(sql_string, params)
        else:
            cursor.execute(sql_string)
        counts = connect.total_changes
        connect.commit()
    except OperationalError as e:
        connect.rollback()
        loggerx.logger('SQLite error: insert_datas', sql_string, params, counts, e)
    close_connect(cursor, connect)


def insert_values(table_name: str, fields: list, values: list):
    connect, cursor = open_connect()
    sql_string = f"INSERT INTO {table_name} ({','.join(fields)}) VALUES ({','.join(['?'] * len(values))})"
    connect.execute(sql_string, values)
    close_connect(cursor, connect)


def query_values(sql_string: str, params=None):
    connect, cursor = open_connect()
    results = []
    try:
        if params is list:
            cursor.executemany(sql_string, params)
        else:
            cursor.execute(sql_string)
        results = cursor.fetchall()
    except OperationalError as e:
        loggerx.logger('SQLite error: query_datas', sql_string, params, e)
    close_connect(cursor, connect)
    return results


def select_values(self, table_name, fields, condition=None, limit=None):
    connect, cursor = open_connect()
    sql_string = f"SELECT {','.join(fields)} FROM {table_name}"
    if condition:
        sql_string += f" WHERE {condition}"
    if limit:
        sql_string += f" LIMIT {limit}"
    results = connect.execute(sql_string).fetchall()
    close_connect(cursor, connect)
    return results


def update_datas(table_name: str, select_key, select_val, changes: dict):
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
        loggerx.logger('SQLite error: update_data', sql_string, e)
    close_connect(cursor, connect)


def replace_datas(sql_string, params: None):
    connect, cursor = open_connect()
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError as e:
        # 遇到问题之后回滚此次提交
        connect.rollback()
        loggerx.logger("replace_data", sql_string, e)
    close_connect(cursor, connect)


def update_values(table_name: str, newer_value, condition):
    connect, cursor = open_connect()
    sql_string = f"UPDATE {table_name} SET {newer_value} WHERE {condition}"
    connect.execute(sql_string)
    close_connect(cursor, connect)


def delete_values(table_name: str, condition):
    connect, cursor = open_connect()
    sql_string = f"DELETE FROM {table_name} WHERE {condition}"
    connect.execute(sql_string)
    close_connect(cursor, connect)


def parse_cfg(section, key, default_value):
    conf_parser = configparser.ConfigParser()
    conf_parser.read('configs.cfg', encoding='utf8')
    if not conf_parser.get(section, key):
        return default_value
    else:
        return conf_parser.get(section, key)
