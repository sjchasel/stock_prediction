#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from preprocess import *
import jieba.posseg as peg

class WordFeature:

    def __init__(self, text):
        """
        传入的text（string）是需要处理的文本
        :param text:
        """
        self.text = text
        self.strokes = deal_wrap("../词典/strokes.txt")
        self.para = split_paragraph(self.text)

    def get_stroke(self, c):
        """
        得到c这个字的笔画数
        :param c:
        :return:
        """
        unicode_ = ord(c)

        if 13312 <= unicode_ <= 64045:
            return self.strokes[unicode_ - 13312]
        elif 131072 <= unicode_ <= 194998:
            return self.strokes[unicode_ - 80338]
        else:
            print("c should be a CJK char, or not have stroke in unihan data.")
            # can also return 0

    def avg_strokes(self):
        """
        平均字笔画数
        :return:
        """
        chinese_text = chinese_chars(self.text)
        sum = 0
        count = len(chinese_text)
        for i in chinese_text:
            sum += int(self.get_stroke(i))
        return sum / count

    def four_word(self):
        """
        至少四个字组成的词数
        :return:
        """
        sum = 0
        for i in segment(self.text):
            if len(i) >= 4:
                sum += 1
        return sum / len(segment(self.text))

    def words_to_phrases(self):
        """
        单字与词组的比例
        :return:
        """
        dan = 0
        for i in segment(self.text):
            if len(i) == 1:
                dan += 1
        return dan / (len(segment(self.text)) - dan)

    def more_nine_word(self):
        """
        超过九笔字比例
        :return:
        """
        chinese_text = chinese_chars(self.text)
        more_9 = 0
        count = len(chinese_text)
        for i in chinese_text:
            if int(self.get_stroke(i)) > 9:
                more_9 += 1
        return more_9 / count

    def ratio_n_and_function(self):
        """
        名词比例(信息价值)
        连接词数与虚词数（可读性和信息价值）
        :return:
        """
        text = ''.join(self.para)
        words = peg.cut(text)  # 通过jieba分词获取词的属性
        nw = 0
        allw = 0
        pcu = 0
        for word, flag in words:
            allw = allw + 1
            if flag[0] == "n":
                nw = nw + 1
            if flag[0] == "p" or flag[0] == "c" or flag[0] == "u":
                pcu = pcu + 1

        return nw / allw, pcu / allw

    def phrase_frequency(self):
        """
        词频统计：计算文章词组频率，利用描述性统计量进行分析（max最大频率，mean平均频率，var频率方差等）
        :return:
        """
        