#!/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser
import json
from configparser import ConfigParser

import pandas as pd
import pymysql
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB


def parse_cfg(section, key, default_value):
    conf_parser = configparser.ConfigParser()
    conf_parser.read('./sample.cfg', encoding='utf8')
    if not conf_parser.get(section, key):
        return default_value
    else:
        return conf_parser.get(section, key)


def write_data(app_name, version_code, version_name, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3):
    data_type = parse_cfg("database", "type", "mysql")
    if data_type == "json":
        write_json(app_name, version_code, version_name, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3)
    else:
        insert_data(app_name, version_code, version_name, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3)


def write_json(app_name, version_code, version_name, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3):
    # dumps和loads是在内存中转换（python对象和json字符串之间的转换），而dump和load则是对应于文件的处理
    with open("./data.json", 'r', encoding='utf-8') as file_r:
        json_data = json.load(file_r)
        print(json_data)
        json_text = []
        index = 0
        same_value = False
        for data in json_data:
            data["id"] = index
            same_value = package_name == data["package_name"]
            json_text.append(data)
            index += 1
        if not same_value:
            json_object = {}
            json_object["id"] = len(json_data)
            json_object["app_name"] = app_name
            json_object["version_code"] = version_code
            json_object["version_name"] = version_name
            json_object["package_name"] = package_name
            json_object["app_signature_v2"] = app_signature_v2
            json_object["update_time"] = update_time
            json_object["target_sdk"] = target_sdk
            json_object["app_signature_v3"] = app_signature_v3
            json_text.append(json_object)
        print(json_text)

    with open('./data.json', 'w+', encoding='utf-8') as file_w:
        json.dump(json_text, file_w, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))


def insert_data(app_name, version_code, version_name, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3):
    db_connect, db_cursor = open_db_connect()
    # insert ignore into
    insert_sql = "REPLACE INTO antivirus_temp(app_name,version_code,version_name,package_name,app_signature_v2,update_time,target_sdk,app_signature_v3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    parser_sql = (app_name, version_name, version_code, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3)
    print('--------------------------------------------------------------')
    print("\rinsert_sql : %s , parser_sql_v : %s" % (insert_sql, parser_sql))
    print('--------------------------------------------------------------')
    write_data_mysql(db_connect, db_cursor, insert_sql, parser_sql)


def write_data_mysql(db_connect, db_cursor, sql_string, data_parser):
    try:
        db_cursor.execute(sql_string, data_parser)
        db_connect.commit()
        db_cursor.close()
        print("\rinsert data finish")
    except Exception as e:
        db_connect.rollback()
        print("\rinsert data error :", e)
    db_connect.close()


def insert_mobei(virus_name, virus_number, virus_level, virus_describe):
    db_connect, db_cursor = open_db_connect()
    insert_sql = "REPLACE INTO virus_sample(virus_name, virus_number, virus_level, virus_describe) VALUES (%s, %s, %s, %s)"
    parser_sql = (virus_name, virus_number, virus_level, virus_describe)
    print('-' * 50)
    print("\r insert_sql : %s , parser_sql_v : %s" % (insert_sql, parser_sql))
    print('-' * 50)
    try:
        db_cursor.execute(insert_sql, parser_sql)
        db_connect.commit()
        db_cursor.close()
        print("\rinsert data finish")
    except Exception as e:
        db_connect.rollback()
        print("\rinsert data error :", e)
    db_connect.close()


def insert_bazaar(first_seen_utc, sha256_hash, md5_hash, sha1_hash, reporter, file_name, file_type_guess, mime_type, signature, clamav, vtpercent, imphash, ssdeep, tlsh, t1, t2, t3):
    db_connect, db_cursor = open_db_connect()
    insert_sql = "REPLACE INTO virus_bazaar(first_seen_utc,sha256_hash,md5_hash,sha1_hash,reporter,file_name,file_type_guess,mime_type,signature,clamav,vtpercent,imphash,ssdeep,tlsh,t1,t2,t3) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    parser_sql = (first_seen_utc, sha256_hash, md5_hash, sha1_hash, reporter, file_name, file_type_guess, mime_type, signature, clamav, vtpercent, imphash, ssdeep, tlsh, t1, t2, t3)
    try:
        print('-' * 50)
        print("\r insert_sql : %s , parser_sql : %s" % (insert_sql, parser_sql))
        print('-' * 50)
        db_cursor.execute(insert_sql, parser_sql)
        db_connect.commit()
        print("\rinsert data finish")
    except Exception as e:
        # db_connect.rollback()
        print("\rinsert data error :", e)
    db_connect.close()


def update_bazaar(sql_data):
    db_poll = get_db_pool(True)
    db_connect = db_poll.connection()
    db_cursor = db_connect.cursor()
    sql_string = "UPDATE virus_bazaar SET sample_link = %s, download_link = %s, tags = %s WHERE sha256_hash = %s"
    data_parser = (sql_data[1], sql_data[3], sql_data[2], sql_data[0])
    print('-' * 50)
    print("\r sql_string : %s , data_parser : %s" % (sql_string, data_parser))
    print('-' * 50)
    try:
        db_cursor.execute(sql_string, data_parser)
        db_connect.commit()
        db_cursor.close()
    except Exception as e:
        print("update data error:", e)
        db_connect.rollback()
    db_connect.close()


def merge_data():
    db_pool = get_db_pool(True)
    db_connect = db_pool.connection()
    db_cursor = db_connect.cursor()
    select_sql = "SELECT app_name,version_code,version_name,package_name,app_signature_v2,update_time, target_sdk,app_signature_v3 FROM antivirus GROUP BY package_name"
    print('-' * 50)
    print("\rselect_sql : %s , database name : %s" % (select_sql, db_pool))
    print('-' * 50)
    try:
        db_cursor.execute(select_sql)
        for result in db_cursor.fetchall():
            insert_data(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
    except Exception as e:
        db_cursor.close()
        print("exception >> %s" % str(e))
    db_connect.close()


def create_table():
    db_pool = get_db_pool(True)
    db_connect = db_pool.connection()
    db_cursor = db_connect.cursor()
    db_cursor.execute("DROP TABLE IF EXISTS antivirus_temp")
    create_sql = """CREATE TABLE `antivirus_temp` (
                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `version_code` varchar(255) DEFAULT NULL,
                  `version_name` varchar(255) DEFAULT NULL,
                  `app_name` varchar(255) DEFAULT NULL,
                  `package_name` varchar(255) NOT NULL,
                  `app_signature_v2` varchar(255) DEFAULT NULL,
                  `update_time` bigint(50) DEFAULT NULL,
                  `app_signature_v3` varchar(255) DEFAULT NULL,
                  `target_sdk` varchar(255) DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1376 DEFAULT CHARSET=utf8mb4"""
    print("\rcreate_sql : %s" % create_sql)
    db_cursor.execute(create_sql)
    db_connect.close()


def csv_mysql(csv_file_name):
    # 用pandas读取csv
    # data = pd.read_csv(file_name,engine='python',encoding='gbk')
    data = pd.read_csv(csv_file_name, engine='python')
    print(data.head(5))  # 打印前5行
    db_pool = get_db_pool(True)
    db_connect = db_pool.connection()
    db_cursor = db_connect.cursor()
    # 数据过滤，替换 nan 值为 None
    data = data.astype(object).where(pd.notnull(data), None)

    for first_seen_utc, sha256_hash, md5_hash, sha1_hash, reporter, file_name, file_type_guess, mime_type, signature, clamav, vtpercent, imphash, ssdeep, tlsh, t1, t2, sample_link, download_link, tags in zip(
            data['first_seen_utc'], data['sha256_hash'], data['md5_hash'], data['sha1_hash'], data['reporter'], data['file_name'], data['file_type_guess'], data['mime_type'],
            data['signature'], data['clamav'], data["vtpercent"], data['imphash'], data['ssdeep'], data['tlsh'], data['t1'], data['t2'], data['sample_link'], data['download_link'], data['tags']):
        data_list = [first_seen_utc, sha256_hash, md5_hash, sha1_hash, reporter, file_name, file_type_guess, mime_type, signature, clamav, vtpercent, imphash, ssdeep, tlsh, t1, t2, sample_link, download_link, tags]
        data_list_trim = []
        for index, data in enumerate(data_list, start=0):
            if isinstance(data, str):
                data = data.replace('"', '')
                data = data.strip()
                if index == 10:
                    try:
                        data = data.replace('n/a', '0')
                        print("index : 10 => %s" % data)
                        data = float(data)
                    except Exception as e:
                        data = 0.0
                        print("error : %s" % e)
            data_list_trim.append(data)
        print("data_list_trim: %s" % data_list_trim)
        insert_sql = "REPLACE INTO virus_bazaar(first_seen_utc,sha256_hash,md5_hash,sha1_hash,reporter,file_name,file_type_guess,mime_type,signature,clamav,vtpercent,imphash,ssdeep,tlsh,t1,t2,sample_link,download_link,tags) " \
                     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            print('-' * 50)
            print('insert_sql: %s' % insert_sql)
            print('-' * 50)
            db_cursor.execute(insert_sql, data_list_trim)
            db_connect.commit()
            print("\rinsert data finish")
        except Exception as e:
            db_connect.rollback()
            print("\rinsert data error :", e)
    db_connect.close()


def insert_sql(sql_string, data_list, table_name):
    print("sql_string => %s ,data_list => %s, table_name => %s" % (sql_string, str(data_list), table_name))


def open_db_connect():
    db_poll = get_db_pool(True)
    db_connect = db_poll.connection()
    db_cursor = db_connect.cursor()
    return db_connect, db_cursor


def get_host():
    config_parser = ConfigParser()
    config_parser.read('zh_cn.config', encoding='UTF-8')
    return config_parser['database']['host']


def get_db_pool(multi_thread):
    config = {
        'host': parse_cfg('database', 'host', '127.0.0.1'),
        'user': parse_cfg("database", "user", "root"),
        'password': parse_cfg("database", "pass", "root"),
        'database': parse_cfg("database", "dbName", "test"),
        'port': 3306,
        'charset': 'utf8'
    }
    if multi_thread:
        pool_db = PooledDB(creator=pymysql, maxconnections=3, mincached=2, maxcached=5, maxshared=3, blocking=True, setsession=[], ping=0, **config)
    else:
        pool_db = PersistentDB(creator=pymysql, maxusage=1000, **config)
    return pool_db
