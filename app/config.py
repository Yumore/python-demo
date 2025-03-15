# -*- coding: utf-8 -*-
# @Time    : 2024/5/2 12:04
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : config.py
# @Software: PyCharm
import os

from app.common.util.MySQLUtil import DBUtil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

url_path_prefix = '/api'

db_util = DBUtil('192.168.102.20', 'root', '123456', 'develo')  # auto_dev_hub
KEYWORDS = ['1003626', '1003609']
Ding_URl = "https://oapi.dingtalk.com/robot/send?access_token=xxxx"
Ding_SCRET = "xxxx"


# base configuration
class Config:
    SECRET_KEY = os.environ.get('KEY') or '123456'

    # 数据库规则
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


# 开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.102.20:3306/auto_dev_hub'


# 测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/test-database'


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/product-database'


# config dict
# 生成一个字典，用来根据字符串找到对应的配置类
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
