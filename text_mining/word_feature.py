#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from preprocess import chinese_chars,segment

class WordFeature:

    def __init__(self, text):
        """
        传入的text（string）是需要处理的文本
        :param text:
        """
        self.text = text
        strokes_path = 'C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/Corpus-master/Corpus-master/zh_dict/strokes.txt'
        # 如果返回 0, 则也是在unicode中不存在kTotalStrokes字段
        strokes = []
        with open(strokes_path, 'r') as fr:
            for line in fr:
                strokes.append(int(line.strip()))
        self.strokes = strokes

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
        chinese_text = self.text.chinese_chars()
        sum = 0
        count = len(chinese_text)
        for i in chinese_text:
            sum += self.get_stroke(i)
        return sum / count

    def four_word(self):
        """
        至少四个字组成的词数
        :return:
        """
        sum = 0
        for i in self.text.segment():
            if len(i) >= 4:
                sum += 1
        return sum / len(self.text.segment())

    def words_to_phrases(self):
        """
        单字与词组的比例
        :return:
        """

    def more_nine_word(self):
        """
        超过九笔字比例
        :return:
        """

    def ratio_n(self):
        """
        名词比例(信息价值)
        :return:
        """

    def function_word(self):
        """
        连接词数与虚词数（可读性和信息价值）
        :return:
        """
    def phrase_frequency(self):
        """
        词频统计：计算文章词组频率，利用描述性统计量进行分析（max最大频率，mean平均频率，var频率方差等）
        :return:
        """