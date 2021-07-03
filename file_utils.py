import hashlib
import os


def get_file_md5(file_path):
    file_name = os.path.basename(file_path)
    md5_data = hashlib.md5()
    file_size = '{:.2f}'.format(os.path.getsize(file_path) / (1024 ** 2))
    print('正在验证文件名称：%s， 文件大小：%s MB' % (file_name, file_size))
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(99999999)
            print('验证速度：%.2f Mb/s' % (len(data) / (1024 ** 2)), end='\r')
            if not data:
                break
            md5_data.update(data)
    file_md5 = md5_data.hexdigest().upper()

    return file_md5


def gen_file_md5(file_path):
    file_name = os.path.basename(file_path)
    md5_file = "%s.md5" % file_path
    file_out = open(md5_file, "w")
    file_out.write("%s %s\n" % (get_file_md5(file_path), file_name.strip()))
    print("generate success, file_path:%s" % md5_file)
    file_out.flush()
    file_out.close()


def gen_md5_value(file_path):
    md5_data = hashlib.md5()
    file = open(file_path, 'rb')
    md5_data.update(file.read())
    file.close()
    return md5_data.hexdigest()
