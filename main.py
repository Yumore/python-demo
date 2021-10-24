#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime

import data_utils
from bazaar import bazaar

if __name__ == '__main__':
    name = data_utils.parse_cfg('download', 'type', 'yyb')
    start_time = datetime.today().now()
    # data_utils.merge_data()
    # data_utils.permission_csv_mysql('./permission.csv')
    # if name == 'qihu':
    #     # 360 应用市场
    #     a = qihu()
    #     a.start()
    # elif name == 'yyb':
    #     # 应用宝
    #     b = yyb()
    #     b.start()
    # else:
    #     print('unsupported market : %s ' % name)

    # m = mobei()
    # m.start()
    #
    b = bazaar()
    b.start()
    # viruscan.initialized()

    duration = datetime.today().now() - start_time
    print("duration : %s" % duration)

# python download_samples.py  --virustotal --vtapikey 1a7b7440ceca037b88fd160ef6c8e04b69ba434bdd76ef2ab0ab52a567xxxxx
