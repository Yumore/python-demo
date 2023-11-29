import os
import subprocess

from configs import configs
from database import sqlitex


def update_repos():
    sql_string = "CREATE TABLE IF NOT EXISTS repos(rid INTEGER PRIMARY KEY, local_dir TEXT, repo_url TEXT, branch TEXT, update_time TEXT, logs TEXT);"
    sqlitex.create_table(sql_string)
    cmd = "find {} -maxdepth 5 -type d -name .git | sort -t '\\0' -n".format(configs.reposPath)
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    for outline in res.stdout.readlines():
        repo_info = {}
        repo_dir = outline.decode("utf-8").strip()
        repo_info['local_dir'] = repo_dir.split(".")[0]
        config_file = "{}/config".format(repo_dir)
        if not os.path.exists(config_file):
            print(repo_dir, config_file)
            continue
        file = open(config_file, 'r')
        contents = file.readlines()
        for line in contents:
            line = line.strip()
            if line.startswith("url"):
                repo_info['repo_url'] = line.split("=")[1].strip()
            if line.startswith("merge"):
                repo_info['branch'] = line.split("/")[2].strip()
        file.close()

        fetch_update(repo_info)


def fetch_update(infos: dict):
    local_dir = infos.get("local_dir")
