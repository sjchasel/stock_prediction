# -*- coding:utf-8 -*-
import re
import pandas as pd
import random

PATH = 'C:/Users/12968/Desktop/数据科学实战-stock prediction/程序/词典/'


class Stroke():
    def __init__(self, text):
        self.text = text
        strokes_path = 'C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/Corpus-master/Corpus-master/zh_dict/strokes.txt'
        # 如果返回 0, 则也是在unicode中不存在kTotalStrokes字段
        strokes = []
        with open(strokes_path, 'r') as fr:
            for line in fr:
                strokes.append(int(line.strip()))
        self.strokes = strokes

    def get_chinese(self):
       regStr = ".*?([\u4E00-\u9FA5]+).*?"
       aa = re.findall(regStr, self.text)
       return ''.join(aa)

    def cal_stroke(self):
        chinese_text = self.get_chinese()
        sum = 0
        count = len(chinese_text)
        for i in chinese_text:
            sum += self.get_stroke(i)
        return sum / count

    def get_stroke(self, c):
        unicode_ = ord(c)

        if 13312 <= unicode_ <= 64045:
            return self.strokes[unicode_ - 13312]
        elif 131072 <= unicode_ <= 194998:
            return self.strokes[unicode_ - 80338]
        else:
            print("c should be a CJK char, or not have stroke in unihan data.")
            # can also return 0


if __name__ == '__main__':
    data = pd.read_csv('C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/新浪公司研报.csv')
    samples = random.sample(list(data['content']), 500)
    result = []
    for sample in samples:
        stroke = Stroke(sample)
        result.append(stroke.cal_stroke())
