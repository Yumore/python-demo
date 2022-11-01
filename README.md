# language-tools

多语言脚本处理工具

# 食用方式

## 1. 导入语言包

将 `nr_common_resource` 工程中 `lib/language` 下的文件目录考入本工程的根目录

## 2.安装依赖

执行`pip install -r requirements.txt` 安装所需要的依赖

## 导入产品翻译源

访问[产品翻译石墨文档](https://shimo.narwal.com/sheets/3yJ3vwX6UAIHJtO5/BZ5yB)

将需要比对的数据复制到 `execls/translate.xls` 各个sheet中

执行脚本 `python main.py`

# 文件目录

- execls -- execl 文件路径
- main.py -- 脚本主入口
- utility -- 需要用到的工具类
- utility/configs.py 配置信息

# 实现想法

- 解析 excel 文件翻译文件数据 key-value 格式
    - 一个 key 对应不同的语音
- 解析 dart 文件生成 key-value 的词条
    - 通过 dart 文件的 key 查询翻译文档的校对数据
    - 文件中所有的 key 对应的 value 校对之后写入文件
- 通过比对工具合并到工程中,防止出错

# 遇到的问题

1. 's 't 'll 've 会导致写入 dart 文件之后报错

- 解决方案 将这些特殊的数据转义后写入 dart
- 在解析翻译文件的时候先转义

2. 翻译文档中 key-values 直接写如内存,导致脚本操作很慢

- 使用结构化数据且能独立操作的数据--sqlite
- 可单独存储每一种语言和翻译总表
- 可实现一对一 和 一对多的数据关系
- 能将结果保存并方便后续增量更新

    