import logging
import os
from datetime import datetime

import colorlog

colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}
logger_filename = "{0}/logger/{1}.log".format(os.getcwd(), datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))


#########################
# *args
# **kwargs
#########################
def logger(tag: str, *args):
    color_logger = logging.getLogger('logger_name')
    # 输出到控制台
    console_handler = logging.StreamHandler()
    # 输出到文件
    filename_handler = logging.FileHandler(filename=logger_filename, mode='a', encoding='utf8')
    # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
    color_logger.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)
    filename_handler.setLevel(logging.INFO)

    # 日志输出格式
    filename_formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S'
    )
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=colors_config
    )
    console_handler.setFormatter(console_formatter)
    filename_handler.setFormatter(filename_formatter)

    # 重复日志问题：
    # 1、防止多次addHandler；
    # 2、logger_name 保证每次添加的时候不一样；
    # 3、显示完log之后调用removeHandler
    if not color_logger.handlers:
        color_logger.addHandler(console_handler)
        color_logger.addHandler(filename_handler)

    console_handler.close()
    filename_handler.close()
    color_logger.info(f'{tag} ========> {args}')


def default_logger(tag: str, *args):
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%m/%d/%Y %H:%M:%S %p"
    # logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    logging.info(f'{tag} ========> {args}')
