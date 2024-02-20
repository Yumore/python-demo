from database import sqlitex
from utility import loggerx


def analyzer_logcat(index: int, limit: int):
    pid_string = f"SELECT DISTINCT lc.pid, COUNT(*) AS count, lp.NAME FROM LOGCAT{0} AS lc INNER JOIN LOGPID AS lp WHERE lc.pid=lp.pid GROUP BY lc.pid ORDER BY count DESC LIMIT {1};".format(index, limit)
    results = sqlitex.query_values(pid_string)
    for result in results:
        tags = query_tags_pid(result[0], index)
        analyzer = {'pid': result[0], 'counts': result[1], 'tags': tags}
        loggerx.logger("analyzer_logcat", analyzer)


def query_tags_pid(pid: str, index: int):
    tag_string = "SELECT DISTINCT tag FROM LOGCAT{0} WHERE pid={1}".format(index, pid)
    tag_results = sqlitex.query_values(tag_string)
    tag_list = []
    for tag_result in tag_results:
        tag_list.append(tag_result[0])
    return tag_list
