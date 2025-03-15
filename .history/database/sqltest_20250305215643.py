from database import sqlitex


def test_create_table():
    # 使用参数化查询防止 SQL 注入
    placeholders = ', '.join(['?'] * len(values))
    columns = ', '.join(fields)
    sql = f"INSERT INTO user ({columns}) VALUES ({placeholders})"
    fields_list = [
        {'name': 'id', 'type': 'INTEGER PRIMARY KEY'},
        {'name': 'name', 'type': 'VARCHAR(20)'},
        {'name': 'gender', 'type': 'VARCHAR(4)'},
        {'name': 'age', 'type': 'INTEGER'}
    ]
    table_name = 'user'
    sqlitex.create_tables(table_name, fields_list)


def test_insert_values():
    fields = ['name', 'gender', 'age']
    values = ['Tom', '男', 20]
    sqlitex.insert_values('user', fields, values)
