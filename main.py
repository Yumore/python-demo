# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import time

from drivers import driverExam
from gits import py4git
from utility import fileUtils


def test_shell():
    py4git.list_repos()


if __name__ == '__main__':
    LOG_FILE = 'logger.log'
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    # logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    millis = int(round(time.time() * 1000))

    # test_shell()

    driverExam.getExams()

    use_time = int(round(time.time() * 1000)) - millis
    fileUtils.format_logger("任务耗时", "{:.2f}秒".format(use_time / 1000))
