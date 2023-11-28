import os

import pandas
from poprogress import simple_progress

from utility import configs, sqliteUtils, fileUtils, langUtils, barUtils


def parse_position(key, lists):
    position = -1
    for index, head in enumerate(lists):
        if head == key:
            position = index
            break
    return position


def parse_datas(headers, xls_path):
    if configs.debuggable:
        sqliteUtils.show_table()
        fileUtils.format_logger("parse_datas", headers)
    arg_pro = langUtils.chinese2pinyin("项目")
    projects = sqliteUtils.query_distinct(arg_pro)
    arg_sts = langUtils.chinese2pinyin("状态")
    states = sqliteUtils.query_distinct(arg_sts)
    fileUtils.format_logger("parse_datas", "状态: {}".format(states))
    arg_maj = langUtils.chinese2pinyin("优先级")
    majors = sqliteUtils.query_distinct(arg_maj)
    fileUtils.format_logger("parse_datas", "优先级: {}".format(majors))
    arg_ele = langUtils.chinese2pinyin("指派给")
    employees = sqliteUtils.query_distinct(arg_ele)
    arg_mdl = langUtils.chinese2pinyin("Def-问题分类")
    modules = sqliteUtils.query_distinct(arg_mdl)
    fileUtils.format_logger("parse_datas", "模块: {}".format(modules))
    departs = sqliteUtils.query_distinct("depart", configs.departTable)
    fileUtils.format_logger("parse_datas", "部门: {}".format(departs))
    dataframes = {}
    for project in simple_progress(projects, desc='项目分析进度'):
        project_status = [["状态", project]]
        for state in states:
            count = sqliteUtils.query_count([arg_pro, arg_sts], [project, state])
            project_status.append([state, count])
        dataframes["项目问题数"] = pandas.DataFrame(project_status)
        project_major = [["优先级", project]]
        for major in majors:
            count = sqliteUtils.query_count([arg_pro, arg_maj], [project, major])
            project_major.append([major, count])
        dataframes["项目优先级问题数"] = pandas.DataFrame(project_major)
        module_status = [["所属模块", "已完成", "未完成"]]
        major_header = ["所属模块"]
        major_header.extend(majors)
        module_major = [major_header]
        for module in simple_progress(modules, desc="模块问题分析进度"):
            doing_count = 0
            finish_count = 0
            for state in configs.issueDoing:
                doing_count += sqliteUtils.query_count([arg_pro, arg_sts, arg_mdl], [project, state, module])
            for state in configs.issueFinish:
                finish_count += sqliteUtils.query_count([arg_pro, arg_sts, arg_mdl], [project, state, module])
            module_status.append([module, finish_count, doing_count])
            major_counts = [module]
            for major in majors:
                count = sqliteUtils.query_count([arg_pro, arg_maj, arg_mdl], [project, major, module])
                major_counts.append(count)
            module_major.append(major_counts)
        dataframes["所属模块优先级"] = pandas.DataFrame(module_major)
        dataframes["所属模块状态"] = pandas.DataFrame(module_status)
        depart_status = {}
        employee_status = [["被指派人", "已完成", "未完成"]]
        for employee in simple_progress(employees, desc="人员分析进度"):
            depart = sqliteUtils.query_depart(employee)
            doing_count = 0
            finish_count = 0
            for state in configs.issueDoing:
                doing_count += sqliteUtils.query_count([arg_pro, arg_sts, arg_ele], [project, state, employee])
            for state in configs.issueFinish:
                finish_count += sqliteUtils.query_count([arg_pro, arg_sts, arg_ele], [project, state, employee])
            employee_status.append([employee, finish_count, doing_count])
            status = depart_status.get(depart)
            if status is None:
                status = [doing_count, finish_count]
            else:
                status[1] += doing_count
                status[0] += finish_count
            depart_status[depart] = status
        depart_counts = [["部门", "已完成", "未完成"]]
        for key in depart_status.keys():
            status = [key]
            status.extend(depart_status.get(key))
            depart_counts.append(status)
        dataframes["成员问题数"] = pandas.DataFrame(employee_status)
        dataframes["部门问题数"] = pandas.DataFrame(depart_counts)
        result_path = "{}/results.xlsx".format(os.getcwd())
        barUtils.generate_line(result_path, depart_counts)
    fileUtils.write_xlsx(project, xls_path, dataframes)
