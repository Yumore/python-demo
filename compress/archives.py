import gzip
import os
import shutil
import tarfile
import zipfile

import py7zr


def recode(raw: str) -> str:
    try:
        return raw.encode('cp437').decode('gbk')
    except UnicodeEncodeError:
        return raw.encode('utf-8').decode('utf-8')


def decompress(file_path: str, dist_dir: str) -> str:
    # (path, filename) = os.path.split(url)
    (base_name, file_ext) = os.path.splitext(file_path)
    if dist_dir == "":
        dist_dir = base_name
    if base_name is None:
        return file_path
    if os.path.isdir(base_name):
        shutil.rmtree(base_name)
    if file_ext == ".7z":
        zip7_file = py7zr.SevenZipFile(r'{}'.format(file_path), mode='r')
        zip7_file.extractall(path=r'{}'.format(dist_dir))
        zip7_file.close()
    elif file_ext == ".zip":
        zip_file = zipfile.ZipFile(r'{}'.format(file_path))
        # output = base_name or os.path.dirname(file_path)
        zip_file.extractall(path=r'{}'.format(dist_dir))
        zip_file.close()
    # elif file_ext == ".rar":
    #     rar_file = rarfile.RarFile(r'{}'.format(file_path))
    #     rar_file.extractall(r'{}'.format(base_name))
    #     rar_file.close()
    elif file_ext == ".tar.gz":
        f_name = file_path.replace(".gz", "")
        # 获取文件的名称，去掉
        gzip_file = gzip.GzipFile(file_path)
        # 创建gzip对象
        open(f_name, "wb+").write(gzip_file.read())
        # gzip对象用read()打开后，写入open()建立的文件里。
        gzip_file.close()
        tar_file = tarfile.open(gzip_file.name)
        names = tar_file.getnames()
        if os.path.isdir(gzip_file + "_files"):
            pass
        else:
            os.mkdir(gzip_file + "_files")
        # 由于解压后是许多文件，预先建立同名文件夹
        for name in names:
            tar_file.extract(name, gzip_file + "_files/")
        tar_file.close()
    return base_name
