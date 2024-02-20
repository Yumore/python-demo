## 使用说明

> 使用 `adb shell ps -A > logcat-pid.txt`  抓取进程信息

```shell
adb shell ps -A > logcat-pid.txt 
```

> 将车机的日志使用U盘导出

> 将 `logcat-pid.txt` 和 导出的日志放在项目 `output` 目录下, 将日志压缩包解压后重命名为 `AdayoLog`

> 运行 `index.py` 即可

### 备注

如果需要重置数据库,则需要删除 `database/mixdata.db` 后重新创建一个文本文件将名字改成 `mixdata.db` 即可