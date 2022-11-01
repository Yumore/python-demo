from datetime import datetime

from utility import data_utils
from utility.bazaar import bazaar
from utility.mobei import mobei
from utility.qihu import qihu
from utility.virusscan import virusscan
from utility.yyb import yyb

name = data_utils.parse_cfg('download', 'type', 'yyb')
start_time = datetime.today().now()
# data_utils.merge_data()
# data_utils.permission_csv_mysql('./permission.csv')
# data_utils.csv_mysql('./full.csv')
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

m = mobei()
# m.start()

b = bazaar()
# b.start()
vs = virusscan()
vs.start()

duration = datetime.today().now() - start_time
print("duration : %s" % duration)
