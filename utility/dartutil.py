import os

from zhconv import zhconv

from utility import configs, fileutil, sqliteutil, language


def foreach_local(root_path):
    sql_string = "CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY AUTOINCREMENT, local_key TEXT UNIQUE, local_value TEXT NOT NULL, module TEXT);".format('tradition_local')
    sqliteutil.create_table(sql_string)
    for prefix in configs.languages:
        table_name = '{0}_local'.format(configs.convert_lang(prefix))
        sql_string = "CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY AUTOINCREMENT, local_key TEXT UNIQUE, local_value TEXT NOT NULL, module TEXT);".format(table_name)
        sqliteutil.create_table(sql_string)
        for dart_file in fileutil.find_files(root_path, prefix, configs.dart_ext):
            merge_sentence(dart_file, prefix, table_name)
    # sqliteutil.merge_table()


# 将翻译内容和dart文件的key-value比对
# 如果新的翻译表中有这一条数据则使用新的翻译表
# 否则使用旧中文相同则替换对应的翻译
def merge_sentence(dart_file, prefix, table_name):
    if prefix != configs.def_prefix:
        compare_dart(dart_file, prefix)
    result_lines = []
    hant_lines = []
    dart_lines = parse_dart(dart_file)
    for dart_line in dart_lines:
        if key_included(dart_line):
            local_value = parse_value(dart_line)
            local_key = parse_key(dart_line)
            # 匹配翻译内容是否有这个数据
            result_data = sqliteutil.query_data(prefix, local_key, local_value)
            if len(result_data):
                # 内容替换, 判断是否有翻译或者校对
                fileutil.format_logger("merge_sentence", [local_value, result_data, language.judge_lang(local_value)])
                dart_line = dart_line.replace(local_value, "{0}".format(result_data))
            else:
                result_data = sqliteutil.convert_wifi(local_value)
            # 将本地的内容更新到数据库
            if prefix == configs.def_prefix:
                # 中文的时候要将简体转换成繁体
                sqliteutil.insert_local('tradition_local', local_key, zhconv.convert(result_data, configs.def_zhTW), generate_clazz(dart_file))
            sqliteutil.insert_local(table_name, local_key, result_data, generate_clazz(dart_file))
        # 将修改过的数据 或者源数据 添加到源数据集合
        result_lines.append(dart_line)
        # 如果是中文则需要转换成繁体
        if prefix == configs.def_prefix:
            hant_file = dart_file.replace(prefix, 'zh_hant')
            if 'const Map<String, String>' in dart_line:
                dart_line = dart_line.replace(generate_clazz(dart_file), generate_clazz(hant_file))
            hant_lines.append(zhconv.convert(dart_line, configs.def_zhTW))
    # 将最终的数据写入到源文件
    fileutil.write_file(dart_file, result_lines)
    # 将繁体写入文件
    if len(hant_lines):
        hant_file = dart_file.replace(prefix, 'zh_hant')
        fileutil.write_file(hant_file, hant_lines)


# 解析未翻译的内容, 过滤掉已经翻译的
def filter_sentence(root_path, prefix):
    for dart_file in fileutil.find_files(root_path, prefix, configs.dart_ext):
        origin_lines = []
        for dart_line in parse_dart(dart_file):
            if key_included(dart_line):
                real_value = parse_value(dart_line)
                lang = language.judge_lang(real_value)
                if 'zh' in lang or (prefix == 'ja_jp' and language.string_convert(real_value) and 'zh' == lang):
                    origin_lines.append(real_value)

        file_name = dart_file + ".txt"
        if os.path.exists(file_name) and not os.path.getsize(file_name):
            os.remove(file_name)
        if len(origin_lines):
            origin_lines.append("\n\n\n未翻译数量：%d" % len(origin_lines))
            fileutil.write_file(file_name, origin_lines)


#   以简体中文为模板
#   在处理翻译之前先找出其他语言包的差异词条
#   并将漏掉的词条写入
def compare_dart(dart_file, prefix):
    fileutil.format_logger('compare_dart', [dart_file, prefix])
    dart_lines = parse_dart(dart_file)
    dart_keys = []
    for dart_line in dart_lines:
        if key_included(dart_line):
            dart_keys.append(parse_key(dart_line))
    china_keys = []
    china_file = dart_file.replace(prefix, 'zh_hans')
    if os.path.exists(china_file):
        china_lines = parse_dart(china_file)
        for china_line in china_lines:
            if key_included(china_line):
                china_keys.append(parse_key(china_line))
        diff_keys = list(set(china_keys) ^ set(dart_keys))
        fileutil.format_logger('compare_dart', diff_keys)
        if len(china_keys) - len(dart_keys):
            merge_list(china_lines, dart_lines, diff_keys, dart_file)
        elif len(dart_keys) - len(china_keys):
            merge_list(dart_lines, china_lines, diff_keys, china_file)
        else:
            fileutil.format_logger("compare_dart", "{0}:::{1} 和 {2} key的个数相同".format(prefix, dart_file, china_file))
    else:
        fileutil.format_logger('compare_dart', '{0} 不存在'.format(china_file))


# 合并两个列表
# TODO 此处没有去重
def merge_list(long_list, short_list, diff_keys, dart_file):
    diff_lines = []
    for long_line in long_list:
        if parse_key(long_line) in diff_keys:
            diff_lines.append(long_line)
    for short_line in long_list:
        if parse_key(short_line) in diff_keys:
            diff_lines.append(short_line)
    if len(diff_lines):
        insert_index = 0
        for index in range(len(short_list) - 1, -1, -1):
            if '};' == short_list[index].strip():
                insert_index = index
        diff_lines.append("%s////%s \n" % (' ' * 4, '*' * 12))
        diff_lines.append("%s//// 同步存在差异的内容\n" % (' ' * 4))
        diff_lines.append("%s////%s \n" % (' ' * 4, '*' * 12))
        for diff_line in diff_lines:
            if diff_line in short_list:
                continue
            short_list.insert(insert_index, diff_line)
        fileutil.write_file(dart_file, short_list)


# 此处逻辑已经废弃
def compare_keys(china_file, dart_file):
    dart_lines = parse_dart(dart_file)
    dart_keys = []
    for dart_line in dart_lines:
        if key_included(dart_line):
            dart_keys.append(dart_line.split(': '))
    china_keys = []
    china_lines = parse_dart(china_file)
    for china_line in china_lines:
        if key_included(china_line):
            china_keys.append(china_line.split(': '))
    results = list(set(dart_keys).intersection(set(china_keys)))
    fileutil.format_logger('compare_keys', results)
    final_lines = []
    if len(results):
        for dart_line in dart_lines:
            if key_included(dart_line):
                lang_key = dart_line.split(': ')
                if lang_key not in results or dart_line in final_lines:
                    continue
                final_lines.append(dart_line)
            else:
                final_lines.append(dart_line)
        fileutil.write_file('%s.bak' % dart_file, final_lines)


# 解析dart文件内容
# 因为要处理代码格式化导致的换行
# 所以放弃while的性能
def parse_dart(filename):
    line_list = []
    file = open(filename, encoding='utf-8')
    lines = file.readlines()
    key_pre = ''
    append_times = 0
    for line in lines:
        line_temp = line.rstrip()
        # 不是以 // 开头并且是 : 结尾的
        if not line_temp.strip().startswith('//') and (line_temp.endswith(':') or line_temp.endswith('Keys')):
            key_pre += (line_temp.strip(' ') if append_times > 0 else line_temp)
            append_times += 1
            continue
        if len(key_pre):
            fileutil.format_logger('parse_dart', [key_pre, line_temp])
            line = key_pre.rstrip('\n') + ' ' + line.strip(' ')
            key_pre = ''
            append_times = 0
        line_list.append(line)
    file.close()
    # 将文件格式化之后输出
    fileutil.write_file(filename, line_list)
    return line_list


def parse_value(full_line):
    real_line = full_line.lstrip('')
    # 存在多个 【:】的只按照第一次的分割
    if real_line.count(': ') >= 2:
        index = real_line.find(': ')
        real_line = real_line[index + 1:]
        # fileutil.format_logger('parse_value', [index, real_line])
    else:
        real_line = real_line.split(': ')[1]
    real_line = real_line.strip('')
    if real_line.endswith(',\n'):
        real_line = real_line.rstrip(',\n')
    if '//' in real_line:
        if real_line.strip().startswith('//'):
            index = real_line.find('//')
            real_line = real_line[index:len(real_line)]
        else:
            real_line = real_line.split('//')[0]
    real_line = real_line.strip()
    if real_line.startswith('"') and real_line.endswith('"'):
        # fileutil.format_logger('parse_value', real_line)
        real_line = real_line.lstrip('"').rstrip('"')
    if real_line.startswith("'") and real_line.endswith("'"):
        real_line = real_line.lstrip("'").rstrip("'")
    if real_line.endswith(','):
        real_line = real_line.rstrip(',')
    if real_line.startswith('《') and real_line.endswith('《'):
        real_line = real_line.lstrip('《').rstrip('》')
    if "'" in real_line:
        real_line = real_line.replace("'", '’')
    # 再次格式化内容
    real_line = real_line.strip()
    return real_line


def parse_key(full_line):
    local_key = full_line.split(': ')[0].lstrip()
    return local_key


# 格式化key
# 因为已经全部迁移到key-value方式
# 所以不需要其他处理
def key_included(full_line):
    line_strip = full_line.lstrip()
    # // 注释的行 /**/注释中有@方式注解的行
    if line_strip.startswith('//'):
        return False
    if configs.dart_ext in line_strip:
        return False
    if line_strip.startswith('* @'):
        return False
    if line_strip.startswith('/*'):
        return False
    return ': ' in line_strip


def convert_normalize(string, convert):
    if convert:
        return string[0].upper() + string[1:].lower()
    else:
        return string.lower()


def generate_clazz(dart_file):
    clazz_name = fileutil.filter_filename(dart_file)
    clazz_names = clazz_name.replace(configs.dart_ext, '').split('_')
    real_name = ''
    for index, name in enumerate(clazz_names):
        real_name += convert_normalize(name, index >= 1)
    # fileutil.format_logger('generate_clazz', [dart_file, real_name])
    return real_name


# 错误满和异常码简繁转换
def convert_json(root_path):
    prefix = 'zh_hans'
    for json_file in fileutil.find_files(root_path, prefix, configs.json_ext):
        fileutil.format_logger('convert_json', json_file)
        result_file = json_file.replace(prefix, 'zh_hant')
        result_lines = []
        file = open(json_file, encoding='utf-8')
        for dart_line in file.readlines():
            result_lines.append(zhconv.convert(dart_line, configs.def_zhTW))
        fileutil.write_file(result_file, result_lines)
