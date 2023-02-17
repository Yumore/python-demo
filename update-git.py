#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import functools
import logging
import os
import os.path
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from typing import Tuple, List


def time_me(info='耗时'):
    def _time_me(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.perf_counter()
            fn(*args, **kwargs)
            print('{} {} {}'.format(fn.__name__, info, int(time.perf_counter() - start)), ' 秒')

        return _wrapper

    return _time_me


def get_dir(path):
    file_list = os.listdir(path)
    try:
        for tmp in file_list:
            path_tmp = os.path.join(path, tmp)
            if os.path.isdir(path_tmp):
                if not path_tmp.endswith('.git'):
                    get_dir(path_tmp)
                else:
                    repo_paths.append(path_tmp)
    except PermissionError:
        pass


@time_me()
def list_dirs(root_path, level=1) -> Tuple[List[str], List[str]]:
    """
    获取指定深度以下的所有文件和目录，返回目录和文件列表
    :param root_path: 要遍历的目录
    :param level: 遍历的深度
    :return: 目录和文件列表
    """
    _dirs: List[str] = []
    _files: List[str] = []

    def inner_list_dirs(path: str, n: int):
        if n <= 0:
            return
        try:
            for df in os.listdir(path):
                abs_path = os.path.join(path, df)
                if os.path.isdir(abs_path):
                    if not os.path.isdir(os.path.join('.git', abs_path)):
                        logging.info('这个目录 {} 不是git 仓库'.format(abs_path))
                    else:
                        logging.info('本地仓库数：{}, 当前仓库地址：{}'.format(len(repo_paths), abs_path))
                        repo_paths.append(abs_path)
                    _dirs.append(abs_path)
                    n -= 1
                    inner_list_dirs(abs_path, n)
                    n += 1
                else:
                    _files.append(abs_path)
        except PermissionError:
            pass

    inner_list_dirs(root_path, level)
    return _dirs, _files


def execute_shell(root_dir: str, depth: int, suffix: str):
    command = "find {} -maxdepth {} -type d -name {} | sort".format(root_dir, depth, suffix)
    print(command)
    result = subprocess.getoutput(command)
    print(result)


def batch_pull(repo: str):
    try:
        # 切换目录
        os.chdir(repo.replace('/.git', ''))
        name = repo.split('/')[-2]
        if name not in skip_repos:
            logging.info('{} 开始拉取 [{}]'.format(threading.current_thread().name, name))
            command = 'git pull'
            # 执行pull
            file = os.popen(command)
            logging.info(file.readline())
            result = file.read()
            if 'Updating' in result:
                has_result.append(name)
                logging.info(name, '有更新内容')
            logging.info('{} 拉取 [{}] 完毕'.format(threading.current_thread().name, name))
        else:
            logging.info('{} 不需要要新'.format(name))
    except Exception as e:
        logging.error('执行异常，{}'.format(repo), e)


@time_me()
def deal_task():
    # 创建线程池
    update_tasks = []
    thread_pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='code-read-exec')
    # 获取目录
    get_dir(base_path)
    logging.info('共 {} 个项目'.format(len(repo_paths)))
    for path in repo_paths:
        time.sleep(0.05)
        update_tasks.append(thread_pool.submit(batch_pull, path))
    # 等待所有完成
    wait(update_tasks, return_when=ALL_COMPLETED)
    logging.info("\n------所有项目拉取完毕--------")


if __name__ == '__main__':
    LOG_FILE = 'logger.log'
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    # logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    # 需要跟新的目录
    logging.info('当前目录 {}'.format(os.getcwd()))
    base_path = "E:/"
    # 跳过的目录
    skip_repos = ['RxMVP', 'viponapp']
    # 所有目录
    repo_paths = []
    # 最大线程数量
    max_workers = 20
    has_result = list()
    # 执行主方法
    # deal_task()
    # logging.info('\n 更新项目列表：', has_result)
    # list_dirs(base_path, 4)
    execute_shell(base_path, 4, ".git")
