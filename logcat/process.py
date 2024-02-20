from database import sqlitex


def parse_process(logger_path: str):
    log_file = open(logger_path, 'r')
    log_lines = log_file.readlines()
    process_list = []
    for index, log_line in enumerate(log_lines):
        splits = log_line.split()
        if index == 0:
            print(index, splits)
            create_process_maps(splits)
        else:
            sql_string = f"REPLACE INTO LOGPID VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            sqlitex.insert_datas(sql_string, splits)


def create_process_maps(datas):
    sql_string = "CREATE TABLE IF NOT EXISTS LOGPID ("
    for posix, key in enumerate(datas):
        splits = ", "
        if posix == len(datas) - 1:
            splits = ""
        sql_string += "{0} TEXT{1}".format(key, splits)
    sql_string += ");"
    print(sql_string)
    sqlitex.create_table(sql_string)
