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
