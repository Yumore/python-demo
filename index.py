# !/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from logcat import convert, analyzer, process
from py4git import py4git
from utility import loggerx, configs

if __name__ == '__main__':
    millis = int(round(time.time() * 1000))
    selected = int(input("please input: \n 0: update repo \n 1: analyzer logcat \n"))
    match selected:
        case 1:
            # 第几次开机的日志
            table_index = 0
            # 输出结果的前20个
            table_limit = 20
            process.parse_process(configs.outputs)
            convert.decompress_logcat(configs.logcats)
            analyzer.analyzer_logcat(table_index, table_limit)
        case 0:
            py4git.update_repos()

    use_time = int(round(time.time() * 1000)) - millis
    loggerx.logger("任务耗时", "{:.2f}秒".format(use_time / 1000))
