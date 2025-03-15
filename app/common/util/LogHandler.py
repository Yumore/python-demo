# -*- coding: utf-8 -*-
# @Time    : 2024/5/2 22:10
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : LogHandler.py
# @Software: PyCharm
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
# project_name = "movie"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "..", ".."))
LOG_PATH = os.path.join(ROOT_PATH, 'logs')

print(CURRENT_PATH, ROOT_PATH, LOG_PATH)

# LOG_PATH = "/app/logs/app/"

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


class LogHandler(logging.Logger):
    """
    LogHandler
    """

    def __init__(self, name, level=INFO, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15,
                                                encoding="utf-8")
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d %(levelname)s | [%(threadName)s] %(name)s [%(lineno)d] | %(filename)s %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d %(levelname)s | [%(threadName)s] %(name)s [%(lineno)d] | %(filename)s %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def resetName(self, name):
        """
        reset name
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()


project_name = 'app'
log = LogHandler(project_name, level=DEBUG)
if __name__ == '__main__':
    # log = LogHandler('test')
    log.info('this is a test msg')
