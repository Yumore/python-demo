import re
import string

import pypinyin
import zhconv

removed_string = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'
removed_map = dict((ord(char), None) for char in string.punctuation)


def filter_string(sentence):
    sentence = re.sub(removed_string, '', sentence)
    sentence = sentence.translate(removed_map)
    # sentence = sentence.replace(' ', '')
    sentence = ''.join(sentence.split(' '))
    sentence = ''.join([index for index in sentence if not index.isdigit()])
    return sentence


def filter_quotation(strings):
    if "'" in strings:
        strings = strings.replace("'", '"')
    return strings


def chinese2pinyin(strings):
    chars = []
    strings = filter_string(strings)
    # strings = ''.join([chr(int(index)) for index in strings if index.isdigit()])
    for char in strings:
        if char.isdigit():
            number = int(char) + 65
            chars.append(chr(number))
        else:
            chars.append(char)
    # fileUtils.format_logger("chinese2pinyin","chars is {} ==> {}".format(chars, strings))
    strings = ''.join([index for index in chars])
    result = ''.join(pypinyin.lazy_pinyin(strings, style=pypinyin.Style.NORMAL))
    # fileUtils.format_logger("chinese2pinyin", "strings is {}, result is {}".format(strings, result))
    return result


# 判断中日韩英
def judge_lang(strings):
    strings = filter_string(strings)
    result = []
    strings = re.sub('[0-9]', '', strings).strip()
    words = re.compile(u"[a-zA-Z]")
    res1 = re.findall(words, strings)
    res2 = re.sub('[a-zA-Z]', '', strings).strip()
    if len(res1) > 0:
        result.append('en')
    if len(res2) <= 0:
        return 'en'

    words = re.compile(u"[\u4e00-\u9fa5]+")
    res1 = re.findall(words, strings)
    res2 = re.sub(u"[\u4e00-\u9fa5]+", '', strings).strip()
    if len(res1) > 0:
        result.append('zh')
    if len(res2) <= 0:
        return 'zh'

    # unicode korean
    words = re.compile(u"[\uac00-\ud7ff]+")
    res1 = re.findall(words, strings)
    res2 = re.sub(u"[\uac00-\ud7ff]+", '', strings).strip()
    if len(res1) > 0:
        result.append('ko')
    if len(res2) <= 0:
        return 'ko'
    # unicode japanese katakana and unicode japanese hiragana
    words = re.compile(u"[\u30a0-\u30ff\u3040-\u309f]+")
    res1 = re.findall(words, strings)
    res2 = re.sub(u"[\u30a0-\u30ff\u3040-\u309f]+", '', strings).strip()
    if len(res1) > 0:
        result.append('ja')
    if len(res2) <= 0:
        return 'ja'
    return ','.join(result)


def string_convert(strings):
    strings = filter_string(strings)
    results = zhconv.convert(strings, 'zh-hans')
    return strings == results
