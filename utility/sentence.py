class Sentence:
    __slots__ = ('__chinese', '__translate', '__proofread', '__important')

    # 构造函数
    def __init__(self, chinese, translate, proofread):
        self.__important = False
        self.__chinese = chinese
        self.__translate = translate
        self.__proofread = proofread

    @property
    def chinese(self):
        return self.__chinese

    @chinese.setter
    def name(self, chinese):
        self.__chinese = chinese

    @property
    def translate(self):
        return self.__translate

    @translate.setter
    def translate(self, translate):
        self.__translate = translate

    @property
    def proofread(self):
        return self.__proofread

    @proofread.setter
    def translate(self, proofread):
        self.__proofread = proofread

    @property
    def important(self):
        return self.__important

    @important.setter
    def translate(self, important):
        self.__important = important

    # 相当于java的toString方法
    def __str__(self):
        return "中文: %s 翻译: %s, 校对: %s, 有先: %b" % (self.__chinese, self.__translate, self.__proofread, self.__important)

    # 相当于java的toString方法
    def __repr__(self):
        return "中文: %s 翻译: %s, 校对: %s, 有先: %b" % (self.__chinese, self.__translate, self.__proofread, self.__important)

    # 相当于java的equals方法
    def __eq__(self, other):
        return self.__chinese == other.chinese
