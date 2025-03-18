import os

# 数据库配置信息
database = "{0}/database/mixdata.db".format(os.getcwd())
issueTable = "issues"
departTable = "employees"
debuggable = True
# status
issueDoing = ["New", "InProgress", "Reopen", "Reviewed"]
issueFinish = ["Resolved", "Cancel1", "Cancel2", "Reject", "Closed"]

reposPath = "~/workspace"

mysqlHost = "127.0.0.1"
mysqlPort = 3306
mysqlPwd = "Nathan@126.com"
mysqlDb = "user_test"
mysqlCharset = "utf8mb4"
mysqlTimeout = 10 * 60 * 60
mysqlReadTime = 10 * 60
mysqlWriteTime = 10 * 60
mysqlUser = "root"

import os

from common.util.MySQLUtil import DBUtil


def create_Mysql_uri(username, password, host, port, database):
    db_url = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(username, password, host, port, database)
    return db_url


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'zheshimiyao')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    WTF_I18n_ENABLED = False
    # 全文搜索
    WHOOSHEE_MIN_STRING_LEN = 0


class DevConfig(BaseConfig):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    # 数据库链接 URI
    DB_URI = create_Mysql_uri('root', 'wistbean', '127.0.0.1', 3306, 'my_system_dev')
    SQLALCHEMY_DATABASE_URI = DB_URI


class ProConfig(BaseConfig):
    # 数据库链接 URI
    DB_URI = create_Mysql_uri('root', 'root', '127.0.0.1', 3306, 'my_system_pro')
    SQLALCHEMY_DATABASE_URI = DB_URI


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


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
# config = {
#     "development": DevConfig,
#     "testing": TestConfig,
#     "production": ProConfig,
#     "default": DevConfig,
# }
