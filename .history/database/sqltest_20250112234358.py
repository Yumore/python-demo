from database import sqlitex


def test_create_table():
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
