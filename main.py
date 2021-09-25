#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime

import data_utils
from mobei import mobei
from qihu import qihu
from yyb import yyb

if __name__ == '__main__':
    name = data_utils.parse_cfg('download', 'type', 'yyb')
    start_time = datetime.today().now()
    # data_utils.merge_data()
    if name == 'qihu':
        # 360 应用市场
        a = qihu()
        a.start()
    elif name == 'yyb':
        # 应用宝
        b = yyb()
        b.start()
    else:
        print('unsupported market : %s ' % name)
    duration = datetime.today().now() - start_time
    print("duration : %s" % duration)
    m = mobei()
    m.start()

# python download_samples.py  --virustotal --vtapikey 1a7b7440ceca037b88fd160ef6c8e04b69ba434bdd76ef2ab0ab52a567xxxxx
