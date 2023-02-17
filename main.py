# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import os
import time

from utility import fileutil, dartutil, execlutil

if __name__ == '__main__':
    LOG_FILE = 'logger.log'
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    # logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    millis = int(round(time.time() * 1000))
    # 解析早版本的execl文件
    execlutil.parse_translate(os.getcwd())
    dartutil.foreach_local(os.getcwd())
    execlutil.generate_result(os.getcwd(), True)

    use_time = int(round(time.time() * 1000)) - millis
    fileutil.format_logger("任务耗时", "{:.2f}秒".format(use_time / 1000))
