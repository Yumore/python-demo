import subprocess

from py4git import configs


def list_repos():
    cmd = "find {} -maxdepth 5 -type d -name .git | sort -t '\\0' -n".format(configs.REPOS_PATH)
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    for line in res.stdout.readlines():
        repo_dir = line.decode("utf-8").strip()
        print("will update repo: {}".format(repo_dir))
        update_repos(repo_dir)


def update_repos(repo_dir: str):
    cmd = "cat {}/config | grep 'url = '".format(repo_dir)
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    for line in res.stdout.readlines():
        print(line.decode("utf-8").strip())
