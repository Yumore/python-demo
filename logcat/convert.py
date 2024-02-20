import os
import re
import shutil

import chardet
from tqdm import tqdm

from compress import archives
from database import sqlitex
from utility import loggerx


def batch_decompress(root_path: str):
    # file_names = os.listdir(root_path)
    file_names = os.scandir(root_path)
    for index, file_name in enumerate(file_names):
        if file_name == ".DS_Store":
            continue
        file_path = os.path.join(r'{}'.format(root_path), file_name)
        if os.path.isdir(file_path):
            logcat_path = r'{}/logcat'.format(file_path)
            loggerx.logger("batch_decompress", logcat_path)
            decompress_logcat(logcat_path, index)
        else:
            (base_name, file_ext) = os.path.splitext(file_path)
            loggerx.logger("batch_decompress", base_name, "\t\t\t\t\t\t\t", file_ext)
            archive_dir = archives.decompress(file_path, root_path)
            logcat_path = r'{}/logcat'.format(archive_dir)
            decompress_logcat(logcat_path, index)


def parse_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def decompress_logcat(logcat_path: str, index=0):
    logcat_zips = os.scandir(logcat_path)
    for logcat_zip in tqdm(logcat_zips, desc='write data to sqlite', position=0, leave=True):
        zip_path = os.path.join(r'{}'.format(logcat_path), logcat_zip)
        (base_name, file_ext) = os.path.splitext(zip_path)
        if base_name == "aRecorder":
            # loggerx.logger("decompress_logcat", base_name, '\t\t\t\t\t\t\t', file_ext)
            continue
        if os.path.isdir(zip_path):
            # loggerx.logger("decompress_logcat", zip_path)
            shutil.rmtree(zip_path)
        create_logcat_table(index)
        log_dir = archives.decompress(zip_path, "")
        # loggerx.logger("decompress_logcat", logcat_path, zip_path, log_dir)
        for txt_file in tqdm(os.scandir(log_dir)):
            decode_file_encode(log_dir, txt_file, logcat_zip, index)


def decode_file_encode(log_dir: str, txt_file, logcat_zip, index):
    try:
        log_file = open(os.path.join(r'{}'.format(log_dir), txt_file), 'r', encoding="utf-8")
        log_lines = log_file.readlines()
        batch_write_logcat(log_lines, index, logcat_zip.name)
    except UnicodeDecodeError:
        file_path = os.path.join(r'{}'.format(log_dir), txt_file)
        encoding = parse_file_encoding(file_path)
        loggerx.logger("decode_file_encode", file_path, encoding)
        log_file = open(file_path, 'r', encoding=encoding)
        log_lines = log_file.readlines()
        batch_write_logcat(log_lines, index, logcat_zip.name)


# with tqdm(log_lines, total=len(log_lines), position=0, leave=True) as progress:
# logics--------------
# time.sleep(.1)
# progress.update()
def batch_write_logcat(log_lines: list, posix: int, file_name: str):
    logcat_datas = []
    system_datas = []
    count = 0
    for log_line in tqdm(log_lines, desc="analyze {0}".format(file_name), position=0, leave=True):
        if "beginning of" in log_line:
            continue
        if "Booting Linux" in log_line:
            posix += 1
            create_logcat_table(posix)
        count += 1
        data_params = parse_logcat_data(log_line, count)
        if len(data_params) > 2:
            logcat_datas.append(data_params)
        else:
            system_datas.append(data_params)
    if len(system_datas):
        create_system_table(posix)
    write_logcat_database(logcat_datas, system_datas, posix)


def create_logcat_table(posix: int):
    sql_string = "CREATE TABLE IF NOT EXISTS LOGCAT{0} (datetime TEXT, timestamp TEXT NOT NULL, pid TEXT NOT NULL, tid TEXT, level TEXT, tag TEXT, message TEXT);".format(posix)
    sqlitex.create_table(sql_string)


def parse_logcat_data(line: str, index: int) -> tuple:
    # tuple->list tuple(list_x)
    # date time pid tid level tag:message
    pattern = r'^(\d{2}\-\d{2})\s(\d\d:\d\d:\d\d\.\d+)\s+(\d+)\s+(\d+)\s+([VDIWEAF])\s+(.*[:]*):\s+(.*)?$'
    splits = re.split(pattern, line)
    if len(splits) > 1:
        data_params = [x.strip() for x in splits if x.strip() != '']
        if len(data_params) < 7:
            data_params.append("NULL")
        return tuple(data_params)
    else:
        return index, line


def create_system_table(posix: int):
    sql_string = "CREATE TABLE IF NOT EXISTS SYSTEM{0} (id TEXT, content TEXT);".format(posix)
    sqlitex.create_table(sql_string)


def write_logcat_database(logcat_params: list, system_params: list, posix: int):
    logcat_string = "REPLACE INTO LOGCAT{0} VALUES (?, ?, ?, ?, ?, ?, ?)".format(posix)
    sqlitex.insert_datas(logcat_string, logcat_params)
    system_string = "REPLACE INTO SYSTEM{0} VALUES (?, ?)".format(posix)
    sqlitex.insert_datas(system_string, system_params)


def test_logcat():
    # logcat_test = "12-12 11:21:42.039   470   512 D fgemcucomm: send Uart data : 6AA60210420002920018"
    logcat_test = "02-01 16:11:08.903   812   812 I HwBinder:812_1: type=1400 audit(0.0:33206): avc: denied { call } for scontext=u:r:mcucomm:s0 tcontext=u:r:system_app:s0 tclass=binder permissive=1"
    patten = r'^(\d{2}\-\d{2})\s(\d\d:\d\d:\d\d\.\d+)\s+(\d+)\s+(\d+)\s+([VDIWEAF])\s+(.*[:]*):\s(.*)?$'
    splits = re.split(patten, logcat_test)
    results = [x.strip() for x in splits if x.strip() != '']
    loggerx.logger("test_logcat", len(results), results)
