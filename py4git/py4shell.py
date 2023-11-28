import os
import subprocess


def py_os_shell():
    result = os.system("python3 -V")
    print(result)


def py_popen_shell():
    str = os.popen("ls").read()
    a = str.split("\n")
    for b in a:
        print(b)
    file = os.popen("python3 demo.py")
    file.read()
    file.close()

    fw = os.popen("python3 demo.py", mode="w")
    fw.write("你好")
    fw.close()


def py_subprocess_shell():
    result = subprocess.run("ls")
    print(result)
    subprocess.run(["python3", "-m", "pip", "list"])
    subprocess.run("pwd", cwd="/Users")


def py_test():
    p = subprocess.Popen(["java", "-version"])
    p.wait()
    print(p.returncode)
