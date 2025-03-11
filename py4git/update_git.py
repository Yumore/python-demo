import datetime
import fnmatch
import glob
import os
import re
import shutil
import sqlite3
import subprocess

# 创建或连接到 SQLite 数据库
conn = sqlite3.connect('git_repos.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS repos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_path TEXT NOT NULL,
    remote_url TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    branch_name TEXT,
    local_hash TEXT,
    remote_hash TEXT,
    status TEXT
)
''')
conn.commit()

ROOT_PATH = os.path.expanduser('~/workspace')
LOG_FILE = os.path.join(ROOT_PATH, 'update-git.log')

with open(LOG_FILE, 'w') as log_file:
    log_file.write(f"{datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')} updated git repos on {subprocess.check_output(['uname', '-a']).decode().strip()}\n")

start_time = datetime.datetime.now().timestamp()

# 查找所有git仓库(包含.git的目录)，并且按照字母降序排序(A->Z --> a->z)
git_dirs = glob.glob(os.path.join(ROOT_PATH, '**', '.git'), recursive=True)
git_dirs.sort(reverse=True)

for repo_git in git_dirs:
    repo_dir = os.path.dirname(repo_git)
    with open(LOG_FILE, 'a') as log_file:
        log_file.write("⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\n")
        log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} --> {repo_dir} is updating now .......\n")

    with open(os.path.join(repo_git, 'config')) as config_file:
        repo_url = [line for line in config_file if 'url =' in line][0]
        real_url = re.sub(r'url = ', '', repo_url).strip()

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> {repo_dir} remote url is {real_url}\n")

    if any(fnmatch.fnmatch(repo_dir, pattern) for pattern in ["*RxMVP*", "*viponapp*", "*wukong*", "*stable-diffusion-*"]):
        continue

    os.chdir(repo_dir)
    REMOTE_URL = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
    branch_name = subprocess.check_output(['git', 'branch']).decode().strip().split('\n')[0].replace('* ', '')
    branch_exists = int(subprocess.check_output(['git', 'ls-remote', '--heads', 'origin', branch_name]).decode().strip().split('\n')[-1] != '')
    branch_updated = int(subprocess.check_output(['git', 'log', '--since=3\ days\ ago', '--oneline']).decode().strip().split('\n')[-1] != '')

    for dir_to_remove in ['.idea', '.gradle', '*/build', '.venv']:
        for path in glob.glob(os.path.join(repo_dir, dir_to_remove), recursive=True):
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)

    if branch_exists == 1:
        local_hash = subprocess.check_output(['git', 'log', branch_name, '-n', '1', '--pretty=format:"%H"']).decode().strip()
        remote_hash = subprocess.check_output(['git', 'log', f'remotes/origin/{branch_name}', '-n', '1', '--pretty=format:"%H"']).decode().strip()

        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> local hash is {local_hash}, remote hash is {remote_hash}\n")

        if local_hash == remote_hash:
            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> {branch_name} of {repo_dir} is up-to-date\n")
                status = "up-to-date"
        else:
            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> {repo_dir} has linked remote, branch is {branch_name}\n")

            subprocess.run(['git', 'reflog', 'expire', '--expire=now', '--all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'fsck', '--full', '--unreachable'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'repack', '-A', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'gc', '--prune=now', '--aggressive'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> recent git log is {subprocess.check_output(['git', 'log', '--pretty=oneline', '-1']).decode().strip()}\n")

            git_status = int(subprocess.check_output(['git', 'status', '--short', '-uno']).decode().strip().split('\n')[-1] != '')

            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')} ---> {repo_dir} branch is {branch_name}, git status -s is {git_status}\n")
                log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> reset command is git reset --hard origin/{branch_name}\n")

            subprocess.run(['git', 'rerere', 'clear'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'fetch', '--all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'reset', '--hard', f'origin/{branch_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with open(LOG_FILE, 'a') as log_file:
                log_file.write(subprocess.check_output(['git', 'count-objects', '-vH']).decode().strip())
                log_file.write(f"\n⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> {repo_dir} has been updated\n")
                status = "updated"

    else:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"⭐️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> {repo_dir} could not access from remote or none commit within 3 days ago\n")
            status = "no-access"

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"⭐ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> current dir is {os.getcwd()}\n")
        log_file.write("⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\n")
        log_file.write("\n\n")

    # 插入或更新数据库记录
    cursor.execute('''
    INSERT INTO repos (repo_path, remote_url, last_updated, branch_name, local_hash, remote_hash, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(repo_path) DO UPDATE SET
    remote_url = excluded.remote_url,
    last_updated = excluded.last_updated,
    branch_name = excluded.branch_name,
    local_hash = excluded.local_hash,
    remote_hash = excluded.remote_hash,
    status = excluded.status
    ''', (repo_dir, real_url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), branch_name, local_hash, remote_hash, status))
    conn.commit()

with open(LOG_FILE, 'a') as log_file:
    log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---> all repositories in {ROOT_PATH} are updated\n")

stop_time = datetime.datetime.now().timestamp()
using_duration = int(stop_time - start_time)

with open(LOG_FILE, 'a') as log_file:
    log_file.write(f"TIME: {using_duration} s\n")

# 关闭数据库连接
conn.close()
