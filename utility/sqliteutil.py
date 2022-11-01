import configparser
import os
import sqlite3
from sqlite3 import OperationalError

from utility import configs, fileutil


def open_connect():
    database = '{0}/translated.db'.format(os.getcwd())
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    return connect, cursor


def create_table(sql_string):
    connect, cursor = open_connect()
    fileutil.format_logger('create_table', sql_string)
    cursor.execute(sql_string)
    connect.commit()
    close_connect(cursor, connect)


def create_tab(sql_string):
    connect, cursor = open_connect()
    fileutil.format_logger('create_tab', sql_string)
    cursor.execute(sql_string)
    connect.commit()
    close_connect(cursor, connect)


def insert_data(table_name, tid, chinese, translated, proofread, sheet_name, timestamp):
    connect, cursor = open_connect()
    sql_string = "REPLACE INTO {0} VALUES({1}, '{2}', '{3}', '{4}', '{5}', {6});".format(table_name, tid, chinese, translated, proofread, sheet_name, timestamp)
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError:
        connect.rollback()
        fileutil.format_logger('SQLite error: insert_data', sql_string)
    close_connect(cursor, connect)


# 先查翻译文档中是否有这个中文的
# 再查对应的key的值
def query_data(prefix, local_key, chinese):
    table_name = 'translate'
    connect, cursor = open_connect()
    real_translate = ''
    sql_string = "SELECT {0} FROM {1} WHERE local_key = '{2}'".format(configs.convert_lang(prefix), table_name, local_key)
    cursor.execute(sql_string)
    results = cursor.fetchall()
    if len(results):
        result = results[len(results) - 1]
        real_translate = result[len(result) - 1]
    # 如果不是中文，并且新的翻译表不存在则去翻译表获取
    else:
        sql_string = "SELECT chinese FROM {0} WHERE local_key = '{1}'".format(table_name, local_key)
        cursor.execute(sql_string)
        results = cursor.fetchall()
        if len(results):
            result = results[len(results) - 1]
            real_translate = result[len(result) - 1]
        elif prefix != configs.def_prefix:
            # 最后的兜底
            sql_string = "SELECT translated, proofread FROM {0} WHERE chinese='{1}';".format(configs.convert_lang(prefix), chinese)
            cursor.execute(sql_string)
            results = cursor.fetchall()
            if len(results):
                result = results[len(results) - 1]
                real_translate = result[0] if result[len(result) - 1] == configs.def_value else result[len(result) - 1]
    close_connect(cursor, connect)
    return convert_wifi(real_translate)


def convert_wifi(value):
    real_value = value
    # 统一配网中的 wifi wi-fi 大小写的问题
    for wifi in configs.def_wifi:
        real_value = real_value.replace(wifi, 'Wi-Fi')
    return real_value


def update_data(table_name, exchanged, chinese):
    connect, cursor = open_connect()
    sql_string = "UPDATE {0} SET exchanged={1} WHERE chinese='{2}';".format(table_name, exchanged, chinese)
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError:
        connect.rollback()
        fileutil.format_logger('SQLite error: update_data', sql_string)
    close_connect(cursor, connect)


def insert_local(table_name, local_key, local_value, module):
    connect, cursor = open_connect()
    sql_string = "REPLACE INTO {0} (local_key, local_value, module) VALUES('{1}', '{2}', '{3}');".format(table_name, local_key, local_value, module)
    try:
        cursor.execute(sql_string)
        connect.commit()
    except OperationalError:
        connect.rollback()
        fileutil.format_logger('SQLite error: insert_local', sql_string)
    close_connect(cursor, connect)


def merge_table():
    # tabel_A, tabel_B, tabel_C, tabel_D 四张表查询方法：
    """
    select D.device_uuid,D.track_switch from tabel_A A
    INNER JOIN tabel_B B
    ON A.device_uuid=B.device_uuid
    INNER JOIN tabel_C C
    ON A.device_uuid=C.device_uuid
    INNER JOIN tabel_D D
    ON A.device_uuid=D.device_uuid;
    """
    connect, cursor = open_connect()
    sql_string = '''
    select A.local_key, A.local_value, B.local_value, C.local_value, D.local_value, E.local_value from chinese_local A
    INNER JOIN english_local B ON A.local_key=B.local_key
    INNER JOIN japanese_local C ON A.local_key=C.local_key
    INNER JOIN korea_local D ON A.local_key=D.local_key 
    INNER JOIN tradition_local E ON A.local_key=E.local_key 
    group by A.local_value;
    '''
    try:
        cursor.execute(sql_string)
        results = cursor.fetchall()
        for data_list in results:
            # exists_sql = "SELECT COUNT(*) FROM {0}  WHERE local_key='{1}';".format(table_name, data_list[0])
            sql_string = "REPLACE INTO translate (local_key, chinese, english, japanese, korea, tradition) VALUES(?, ?, ?, ?, ?, ?);"
            cursor.execute(sql_string, data_list)
            connect.commit()
    except OperationalError as e:
        fileutil.format_logger('SQLite error: merge_translate', [sql_string, e])
        connect.rollback()
    close_connect(cursor, connect)


def close_connect(cursor, connect):
    cursor.close()
    connect.close()


def parse_cfg(section, key, default_value):
    conf_parser = configparser.ConfigParser()
    conf_parser.read('configs.cfg', encoding='utf8')
    if not conf_parser.get(section, key):
        return default_value
    else:
        return conf_parser.get(section, key)
