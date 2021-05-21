#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from preprocess import split_sentence_fine, split_sentence_coarse, split_paragraph
import re

class SentenceFeature:

    def __init__(self, text):
        self.text = ''.join(split_paragraph(text))

    def avg_sentence(self, disp=False):
        """
        平均句长
        """
        lenn = 0  # 句子总长度
        num = 0  # 句子数
        sentences = split_sentence_coarse(self.text)  # 把文本根据标点符号分割开
        for stuff in sentences:
            lenn = lenn + len(stuff)
            num = num + 1

        # 是否可视化
        if disp:
            # 构建数据
            x_data = ["句子总数", "总句数", "平均句长"]
            y_data = [lenn, num, lenn / num]
            bar_width = 0.3
            plt.bar(x=x_data, height=y_data, label='',
                    color='steelblue', alpha=0.8, width=bar_width)
            for x, y in enumerate(y_data):
                plt.text(x, y + 100, '%s' % y, ha='center', va='bottom')
            plt.title("平局句长计算")
            plt.xlabel("类型")
            plt.ylabel("数量")
            plt.show()

        return lenn / num

    def no_en_ch():
        """
        非文本类信息比例:非中英文文本信息的字符所占比例
        """
        sum = 0
        for i in self.text:
            if self.isChinese(i) or self.isEnglish(i):
                pass
            else:
                sum += 1
        return sum / len(self.text)

    def isChinese(self, ch):
        """
        判断字符ch是否为中文
        """
        if '\u4e00' <= ch <= '\u9fff':
            return True
        return False

    def isEnglish(self, word):
        """
        判断一个字符是否是英文字母
        """
        if re.match("[A-Za-z]", word):
            return True
        return False
    
    def get_result(self):
        res['avg_sentence'] = self.avg_sentence()
        res['no_text'] = self. no_en_ch()
        return res

