import jieba
from nltk.tree import Tree
import re
import numpy as np
import logging
from stanfordcorenlp import StanfordCoreNLP
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

PATH = 'C:/Users/12968/Desktop/数据科学实战-stock prediction/程序/词典/'


class Preprocess:

    def __init__(self, text):
        self.text = text
        # 标点符号
        self.puncs_fine = ['……', '\r\n', '，', '。', ';', '；', '…', '！',
                           '!', '?', '？', '\r', '\n', '“', '”', '‘', '’',
                           '：']
        self.puncs_coarse = ['。', '！', '？', '\n', '“', '”', '‘', '’']
        self.front_quote_list = ['“', '‘']
        self.back_quote_list = ['”', '’']

        self.puncs_coarse_ptn = re.compile('([。“”！？\n])')
        self.puncs_fine_ptn = re.compile('([，：。;“”；…！!?？\r\n])')
        # 分段符号
        self.para_flag = ['\xa0\xa0\xa0\r\n', '\xa0\xa0\xa0\r\n\u3000\u3000']

    def split_paragraph(self):
        """
        把输入的文本分段，返回装着每个段落的列表
        """
        for flag in self.para_flag:
            if flag in self.text:
                para_list = self.text.split(flag)
        res = [i.strip() for i in para_list]
        return res

    def split_sentence_coarse(self):
        """
        按照。！？“”等中文完整句子语义来分句
        :return:装着每个句子的列表（包括标点符号）
        """

    def split_sentence_fine(self):
        """
        按照。！？，：；、“”‘’ 等中文短句来分句
        :return:返回装着每个句子的列表（包括标点符号）
        """

    def segment(self):
        """
        基于user_dict词典与jieba的分词
        :return:
        """
