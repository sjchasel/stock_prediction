import re
import numpy as np
import pandas as pd
import random
import jieba

def words_count(s):
    stopwords = cn_stopwords
    np.append(stopwords,"公司")
    counts = {}
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~，。/；‘【】-=《》？：“{}——+、|~·！@#￥%……&*（）1234567890\u3000\xa0 \r\n':
        s = s.replace(ch,"")      # 将文本中特殊字符替换为空格
    for ch in stopwords:
        s = s.replace(ch,"")   
    words = jieba.lcut_for_search(s)     # 搜索引擎模式
    for word in words:
        counts[word] = counts.get(word, 0) + 1    # 遍历所有词语，每出现一次其对应的值加 1
    df = pd.DataFrame({"词":counts.keys(),"词频":counts.values()}).sort_values("词频",ascending=False)
    ans = [df["词频"].mean(),df["词频"].var(),df["词频"].max()]
    return ans

data = pd.read_csv('D://学习文件/个人/大三下/1 2 数据科学实战/非结构化数据分析/新浪公司研报.csv')
result = []
for sample in random.sample(list(data['content']), 500):
    sample = re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', sample))
    result.append(words_count(sample))