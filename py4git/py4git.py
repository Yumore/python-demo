import os
import subprocess

from git import Repo

from database import sqlitex
from utility import configs, loggerx


def clone_repo():
    local_path = os.path.join('test', 't1')
    repo = Repo(local_path)
    repo.git.pull()


def update_repos():
    fields_list = [
        {'name': 'rid', 'type': 'INTEGER PRIMARY KEY AUTOINCREMENT'},
        {'name': 'local_dir', 'type': 'TEXT'},
        {'name': 'repo_url', 'type': 'TEXT'},
        {'name': 'branch', 'type': 'TEXT'},
        {'name': 'update_time', 'type': 'TEXT'},
        {'name': 'logs', 'type': 'TEXT'}
    ]
    sqlitex.create_tables(configs.reposTable, fields_list)
    command = f"find {configs.reposPath} -maxdepth 5 -type d -name .git | sort -t '\\0' -n"
    loggerx.logger("update_repos", command)
    result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for outline in result.stdout.readlines():
        repo_info = {}
        repo_dir = outline.decode("utf-8").strip()
        repo_info['local_dir'] = repo_dir.split(".")[0]
        config_file = "{}/config".format(repo_dir)
        if not os.path.exists(config_file):
            print(repo_dir, config_file)
            continue
        file = open(config_file, 'r')
        for line in file.readlines():
            line = line.strip()
            if line.startswith("url"):
                repo_info['repo_url'] = line.split("=")[1].strip()
            if line.startswith("merge"):
                repo_info['branch'] = line.split("/")[2].strip()
        file.close()
        fetch_update(repo_info)


def fetch_update(infos: dict):
    loggerx.logger("fetch_update", infos)
    fields = []
    values = []
    for key in infos:
        fields.append(key)
        values.append(infos[key])
    sqlitex.insert_values(configs.reposTable, fields, values)
    # repo = Repo(infos.get('local_dir'))
    # repo.git.pull()
