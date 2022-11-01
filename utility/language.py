import re
import string

import zhconv

remove_nota = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def filter_string(sentence):
    sentence = re.sub(remove_nota, '', sentence)
    sentence = sentence.translate(remove_punctuation_map)
    return sentence.strip()


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
