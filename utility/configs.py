import os

def_value = '************************'
execl_ext = '.xls'
csv_ext = '.csv'
dart_ext = '.dart'
json_ext = '.json'
execl_path = 'backup'

# 数据库配置信息
database = "{0}/database/mixdata.db".format(os.getcwd())
outputs = "{0}/output/logcat-pid.txt".format(os.getcwd())
logcats = "{0}/output/AdayoLog/logcat".format(os.getcwd())

issueTable = "issues"
reposTable = "repos"
departTable = "employees"
debuggable = True
# status
issueDoing = ["New", "InProgress", "Reopen", "Reviewed"]
issueFinish = ["Resolved", "Cancel1", "Cancel2", "Reject", "Closed"]

reposPath = "/Users/nathaniel/workspace"
