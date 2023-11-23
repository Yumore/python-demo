# mysql数据库服务器，端口：3306，而且服务器是处于启动状态
# 安装pymysql：pip install pymysql
import threading

import pymysql
from settings import MYSQL_HOST, MYSQL_DB, MYSQL_PWD, MYSQL_USER


class DataManager():
    # 单例模式，确保每次实例化都调用一个对象。
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataManager, "_instance"):
            with DataManager._instance_lock:
                DataManager._instance = object.__new__(cls)
                return DataManager._instance

        return DataManager._instance

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PWD, database=MYSQL_DB, charset='utf8')

        # 建立游标
        self.cursor = self.conn.cursor()

    def save_data(self, data):
        # 数据库操作
        # (1)定义一个格式化的sql语句
        sql = "insert into question(`type`,`title`,`option`,`answer`) values(%s,%s,%s,%s)"
        # (2)准备数据
        # data = ('nancy','30','100','太好笑了')
        # (3)操作
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print('插入数据失败', e)
            self.conn.rollback()  # 回滚

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
