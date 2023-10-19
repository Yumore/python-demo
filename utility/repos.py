# 在子 shell 中执行命令（字符串）。该函数是调用标准 C 函数 system() 来实现的，
# 因此限制条件与该函数相同。对 sys.stdin 等的更改不会反映在执行命令的环境中。
# command 产生的任何输出将被发送到解释器标准输出流。
# 返回一个 int 类型的 code，一般返回 0 表示执行成功。
import os

command = ""
os.system(command)

result = os.system("python3 -V")
print(result)

# 打开一个管道执行 cmd 命令, 返回值是连接到管道的 文件对象。
# 只能和管道单向通讯, 返回值只能是 写入 或 读取 对象。
# mode 为 'r', 表示返回的的是 读取对象, 可以对管道 read()、 readlines()
# mode 为 'w', 表示返回的的是 写入对象, 可以对管道 write()、writelines()
# 返回的文件对象只能读写字符串, 不能是字节类型。
os.popen(command, mode='r', buffering=-1)

file = os.popen("python3 demo.py")
file.read()
file.close()

fw = os.popen("python3 demo.py", mode="w")
fw.write("你好")
fw.close()

# subprocess.run(args, 
#                *,
#                stdin=None, input=None, stdout=None, stderr=None,
#                capture_output=False, shell=False, cwd=None, timeout=None,
#                check=False, encoding=None, errors=None, text=None, env=None,
#                universal_newlines=None, **other_popen_kwargs)
# 部分参数说明:
#
# args:
#    需要执行的命令, str 或 list/tuple 类型, 如果携带参数需要使用 list/tuple 类型,
#    将命令以及每个参数组成 list/tuple, 例如: ["python3", "-m", "pip", "list"]
#
# stdin, stdout, stderr:
#    子进程的标准 输入、输出、错误输出
#
# cwd:
#    执行命令时的工作目录
#
# timeout:
#    超时时间, 超过该时间子进程还没有结束, 则杀掉子进程并抛出异常
#
# env:
#    为子进程设置环境变量, 字典类型, 默认继承自父进程
#
# 等待命令执行完成后, 返回一个 subprocess.CompletedProcess 实例,
# 可以通过 CompletedProcess.returncode 属性判断子进程的返回 Code。
