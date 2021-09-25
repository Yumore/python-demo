#!/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser
import json
from configparser import ConfigParser

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
    db_pool = get_db_pool(True)
    db_connect = db_pool.connection()
    db_cursor = db_connect.cursor()
    # insert ignore into
    insert_sql = "REPLACE INTO antivirus_temp(app_name,version_code,version_name,package_name,app_signature_v2,update_time,target_sdk,app_signature_v3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    parser_sql = (app_name, version_name, version_code, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3)
    print('--------------------------------------------------------------')
    print("\rinsert_sql : %s , parser_sql_v : %s" % (insert_sql, parser_sql))
    print('--------------------------------------------------------------')
    try:
        db_cursor.execute(insert_sql, parser_sql)
        db_connect.commit()
        print("\rinsert data finish")
    except Exception as e:
        db_connect.rollback()
        print("\rinsert data error :", e)
    db_connect.close()


def insert_virus(virus_name, virus_number, virus_level, virus_describe):
    db_poll = get_db_pool(True)
    db_connect = db_poll.connection()
    db_cursor = db_connect.cursor()
    insert_sql = "REPLACE INTO virus_sample(virus_name, virus_number, virus_level, virus_describe) VALUES (%s, %s, %s, %s)"
    parser_sql = (virus_name, virus_number, virus_level, virus_describe)
    print('--------------------------------------------------------------')
    print("\rinsert_sql : %s , parser_sql_v : %s" % (insert_sql, parser_sql))
    print('--------------------------------------------------------------')
    try:
        db_cursor.execute(insert_sql, parser_sql)
        db_connect.commit()
        print("\rinsert data finish")
    except Exception as e:
        db_connect.rollback()
        print("\rinsert data error :", e)
    db_connect.close()


def merge_data():
    db_pool = get_db_pool(True)
    db_connect = db_pool.connection()
    db_cursor = db_connect.cursor()
    select_sql = "SELECT app_name,version_code,version_name,package_name,app_signature_v2,update_time, target_sdk,app_signature_v3 FROM antivirus GROUP BY package_name"
    print('--------------------------------------------------------------')
    print("\rselect_sql : %s , database name : %s" % (select_sql, db_pool))
    print('--------------------------------------------------------------')
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
