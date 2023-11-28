import os

def_value = '************************'
execl_ext = '.xls'
csv_ext = '.csv'
dart_ext = '.dart'
json_ext = '.json'
execl_path = 'backup'
# 语言标识
languages = ['zh_hans', 'en_us', 'ja_jp', 'ko_kr']
def_prefix = 'zh_hans'
# zh-hant
def_zhTW = 'zh-tw'
def_wifi = ['wifi', 'WiFi', 'WIFI', 'wi-fi']

# 数据库配置信息
database = "{0}/database/mixdata.db".format(os.getcwd())
issueTable = "issues"
departTable = "employees"
debuggable = True
# status
issueDoing = ["New", "InProgress", "Reopen", "Reviewed"]
issueFinish = ["Resolved", "Cancel1", "Cancel2", "Reject", "Closed"]

REPOS_PATH = "/Users/nathaniel/workspace"


def convert_lang(prefix):
    if prefix == 'zh_hans':
        return 'chinese'
    elif prefix == 'en_us':
        return 'english'
    elif prefix == 'ja_jp':
        return 'japanese'
    elif prefix == 'ko_kr':
        return 'korea'
    else:
        return 'known'
