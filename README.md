# 免责声明

该项目仅做学习交流使用，请勿用做商务用途

若用在商务用途上引起的任何纠纷由使用者自行承担

若本项目有损害您的相关利益，请及时告知，以便沟通交流

## 项目说明

使用Python批量下载apk文件并获取包名和应用签名

## 环境

Python3.6+ MySQL 可选

> 安装Python环境
>
> Windows 从官网下载Python安装包，并配置环境变量，最好是3.6以上版本
>
> 在命令行输入 `python -V` 和 `pip -V` 查看配置的环境变量是否正确
>
> Linux和MacOS需要安装Python3.6以上版本
>
> MacOS：`brew install python3`
>
> Linux：`apt install python3`

以上如有问题请自行百度或者 <a herf="mailto:nathanwriting@126.com">联系我</a>

## 目录结构

    ├── antivirus.sql 已有mysql, 但没有去重
    ├── apk_info.py 解析apk文件信息
    ├── class_360.py 360 测试脚本
    ├── class_YYB.py 应用宝测试脚本
    ├── data.json 本地保存json
    ├── data_utils.py 数据存储工具类
    ├── file_utils.py 文件工具类
    ├── get_apk.py  下载文件测试工具类
    ├── get_apk_info.py 获取本地文件信息工具类
    ├── main.py 主入口文件
    ├── qihu.py 360下载类
    ├── requirements.txt 依赖库
    ├── sample.cfg 配置文件
    └── yyb.py 应用宝下载类

## 配置下载目录

> 修改[sample.cfg](./sample.cfg)文件即可
>
>如果没有安装MySQL 建议不要修改相关配置
>
> 所生成数据会存在[data.json](./data.json)中

## 如何使用

> 1. 安装依赖
>
>1.1 Windows 在cmd中输入`pip install -r requirements.txt`
>
>1.2 MacOS和Linux在Terminal输入 `pip install -r requirements.txt`
>
>2. 执行 `python3 main.py`
