def my_mysql_test(operate_tablename: str, my_sqldb_config_param: dict):
    print("-------------my_mysql_test：注意下面传入数据的格式---------------")

    # 创建自己的mysql连接对象，operate_tablename是要进行操作的表名，my_sqldb_config_param是pymysql连接本机MySQL所需的配置参数
    mysql = MySql(operate_tablename=operate_tablename, my_sqldb_config_param=my_sqldb_config_param)
    print(mysql.operate_tablename)
    mysql.operate_tablename = "tb_user"  # 修改要操作的表
    print(mysql.operate_tablename)

    print("----------------insert-----------------")
    # 自定义sql语句，插入多条数据，这里我们在创建表时，设置了id自动增加，所以这里不需要设置id字段
    mysql.insert_by_sql('insert into tb_user(name,age,gender) values ("111", 12, "男"), ("222", 22, "女"),("333", 32, "女")')
    mysql.insert(("444", 42, "男"))  # 插入一条数据
    mysql.insert(("555", 52, "男"), ("666", 62, "女"))  # 插入多条数据
    # mysql.insert("777",72,"男") # 异常
    # mysql.insert(["888",82,"女"]) # 异常
    mysql.insert(("999", 92, "男"), ("000", '28', "女", "xxx"))  # 异常

    print("----------------select-----------------")
    result = mysql.select_by_sql("select * from tb_user where gender='男'")  # 自定义sql语句查询数据
    print("查询：自定义sql查询数据：\n", result)
    result = mysql.select_all()  # 查询表中所有数据，返回表中所有数据
    print("查询：表中所有数据：\n", result)
    result = mysql.select_by_id(1)  # 通过id查询，返回一条数据
    print("\n查询：通过id：", result)
    result = mysql.select_many(1, {"gender": "女"})  # 指定查询返回多少条数数据,可根据简单条件查询（where 字段=”“）
    print('查询：指定查询多少条数数据,可根据简单条件查询（where 字段=”“）：', result)

    print("----------------delete-----------------")
    mysql.delete_by_sql('delete from tb_user where gender="男"')  # 自定义sql语句删除数据
    mysql.delete_by_id(4)  # 通过id删除数据
    result = mysql.select_all()
    print("删除数据后查询表中所有数据：\n", result)

    print("----------------update-----------------")
    mysql.update_by_sql("update tb_user set name='update_name',gender='男' where id = 6")  # 自定义sql语句更新数据
    mysql.update_by_id(3, {"age": "180"})  # 通过id更新数据
    mysql.update_by_id(2, {"name": "update_name", "age": "999"})
    mysql.update_by_id(6, {"xxx": "updateName", "yyy": "18"})  # 异常
    # mysql.update_by_id(1, ("age","180"))  # 异常
    result = mysql.select_all()
    print("更新数据后查询表中所有数据：\n", result)


if __name__ == '__main__':
    my_sqldb_config_param = {
        "host": "127.0.0.1",  # 连接主机的ip
        "port": 3306,  # 连接主机的端口
        "user": "root",  # 本地数据库的用户名
        "password": "***",  # 本地数据库的密码
        "database": "pythondemo",  # 连接的数据库
        "charset": "utf8"  # 设置编码格式
    }
    operate_tablename = "tb_test"  # 设置该数据库准备操作的表名
    my_mysql_test(operate_tablename, my_sqldb_config_param)
