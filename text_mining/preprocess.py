import jieba
from nltk.tree import Tree
import re
import numpy as np
import logging
from stanfordcorenlp import StanfordCoreNLP
import random
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt

PATH = '../词典/'

# 标点符号
puncs_fine = ['……', '\r\n', '，', '。', ';', '；', '…', '！',
              '!', '?', '？', '\r', '\n', '“', '”', '‘', '’',
              '：']
puncs_coarse = ['。', '!', '；', '？', '……', '\n']
front_quote_list = ['“', '‘']
back_quote_list = ['”', '’']

# 分段符号
para_flag = ['\xa0\xa0\xa0\r\n', '\xa0\xa0\xa0\r\n\u3000\u3000','???\r\r\r\n']
# 词典

def deal_wrap(filedict):
    temp = []
    for x in open(filedict, 'r', encoding='utf-8').readlines():
        temp.append(x.strip())
    return temp


posdict = deal_wrap(PATH + 'positive.txt')
negdict = deal_wrap(PATH + 'negative.txt')
# 程度副词词典
mostdict = deal_wrap(PATH + 'most.txt')  # 权值为2
verydict = deal_wrap(PATH + 'very.txt')  # 权值为1.5
moredict = deal_wrap(PATH + 'more.txt')  # 权值为1.25
ishdict = deal_wrap(PATH + 'ish.txt')  # 权值为0.5
insufficientdict = deal_wrap(PATH + 'insufficiently.txt')  # 权值为0.25
inversedict = deal_wrap(PATH + 'inverse.txt')  # 权值为-1
stopwords = deal_wrap(PATH + 'stop1205.txt')
strokes = deal_wrap(PATH + 'strokes.txt')


def split_paragraph(text):
    """
    把输入的文本分段，返回装着每个段落的列表
    """
    for flag in para_flag:
        para_list = []
        if flag in text:
            para_list = text.split(flag)
    res = [i.strip() for i in para_list]
    return res


def split_sentence_coarse(text):
    """
    按照。！？“”等中文完整句子语义来分句
    1. 去除换行符、多余的空格、百分号
    2. 分句，存入列表
    :return:装着每个句子的列表（包括标点符号）
    """
    sentences = []
    text = re.sub('%', '', re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', text)))
    start = 0
    for i in range(len(text)):
        if text[i] in puncs_coarse:
            sentences.append(text[start:i + 1])
            start = i + 1
    return sentences


def split_sentence_fine(text):
    """
    按照。！？，：；、“”‘’ 等中文短句来分句
    :return:返回装着每个句子的列表（包括标点符号）
    """
    sentences = []
    text = re.sub('%', '', re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', text)))
    start = 0
    for i in range(len(text)):
        if text[i] in puncs_fine:
            sentences.append(text[start:i + 1])
            start = i + 1
    return sentences


def segment(sentence):
    """
    基于user_dict词典与jieba的分词
    :return:
    """
    sentence = re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', sentence))
    jieba.load_userdict('../词典/userdict.txt')
    sentence_seged = jieba.cut(sentence.strip())
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    word_list = outstr.split(' ')
    pattern = '[A-Za-z]*[0-9]*[\'\"\%.\s\@\!\#\$\^\&\*\(\)\-\<\>\?\/\,\~\`\:\;]*[：；”“ ‘’+-——！，。？、~@#￥%……&*（）【】]*'
    t = [re.sub(pattern, "", x.strip()) for x in word_list]
    return [x for x in t if x != '']


def chinese_chars(text):
    """
    返回所有中文字（可用于计算笔画数
    :return:
    """
    regStr = ".*?([\u4E00-\u9FA5]+).*?"
    aa = re.findall(regStr, text)
    return ''.join(aa)
