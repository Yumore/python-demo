# 判断变量类型的函数
def typeof(variate):
    var_type = None
    if isinstance(variate, int):
        var_type = "int"
    elif isinstance(variate, str):
        var_type = "str"
    elif isinstance(variate, float):
        var_type = "float"
    elif isinstance(variate, list):
        var_type = "list"
    elif isinstance(variate, tuple):
        var_type = "tuple"
    elif isinstance(variate, dict):
        var_type = "dict"
    elif isinstance(variate, set):
        var_type = "set"
    else:
        var_type = "None"
    return var_type
