#coding:utf-8
import re
import matplotlib.pyplot as plt
import pandas as pd
import random


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def preprocess(text):
    """
    预处理：
    1. 去除换行符、多余的空格、百分号
    2. 分句，存入列表
    :return:返回句子列表
    """
    sentences = []
    text = re.sub('%', '', re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', text)))
    start = 0
    for i in range(len(text)):
        if text[i] in ['。', '!', '；', '？', '……', '.', '   ']:
            sentences.append(text[start:i + 1])
            start = i + 1
    return sentences

def calculate_avg_length(s, disp=False):
    lenn = 0  # 句子总长度
    num = 0  # 句子数
    sentences = preprocess(s)  # 把文本根据标点符号分割开
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
    return ( lenn / num )


data = pd.read_csv('C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/新浪公司研报.csv')
result = []
chang = 0
chang_id = 0
duan = 100000000000
duan_id = 0
samples = random.sample(list(data['content']), 500)
for i in range(len(samples)):
    sample = samples[i]
    sample = re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', sample))
    res = calculate_avg_length(sample, False)
    if res >= chang:
        chang_id = i
        chang = res
    if res <= duan:
        duan_id = i
        duan = res
    result.append(res)

print(chang_id)
print(samples[chang_id])
print(calculate_avg_length(samples[chang_id], True))
print('-------------------')
print(duan_id)
print(samples[duan_id])
print(calculate_avg_length(samples[duan_id], True))

# data = pd.read_csv('C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/新浪公司研报.csv')
# result = []
# samples = random.sample(list(data['content']), 500)
# for i in range(len(samples)):
#     sample = samples[i]
#     sample = re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', sample))
#     res = calculate_avg_length(sample, False)
#     result.append(res)

