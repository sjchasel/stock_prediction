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
from summarize import *


PATH = '../词典/'


class ParseTree:

    def __init__(self, text):
        self.text = text  # 传入的文本
        # 定义模型
        self.nlp = StanfordCoreNLP(r'E:/py/stanford-corenlp-4.2.0', lang='zh', quiet=False, logging_level=logging.DEBUG)
        # 分句
        self.sentences = self.preprocess()
        print(self.sentences)
        self.stopwords = []

    def load_dicts(self):
        stop = PATH + 'stop1205.txt'
        self.stopwords = self.dict_load(stop)

#     def preprocess(self):
#         """
#         预处理：
#         1. 去除换行符、多余的空格、百分号
#         2. 分句，存入列表
#         :return:返回句子列表
#         """
#         sentences = []
#         self.text = re.sub('%', '', re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', self.text)))
#         start = 0
#         for i in range(len(self.text)):
#             if self.text[i] in ['。', '!', '；', '？', '……']:
#                 sentences.append(self.text[start:i + 1])
#                 start = i + 1
#         return sentences

    def preprocess(self):
        """
        把文本处理成摘要句子列表
        """
        return get_sum(self.text)
        
    def tree(self, sentence):
        sentence = sentence.replace(' ','')
        print(sentence)
        res = self.nlp.parse(sentence)
        # nlp.close()
        return res

    def sum_of_heights(self):
        """
        计算整篇文本的每句话构成的语法分析树的高度之和
        :return: 高度之和
        """
        sumHeights = []
        for sentence in self.sentences:
            sentence.replace('%','')
            res = self.tree(sentence)  # 语法树，是个字符串
            sumHeights.append(len(res.split("\r\n")))
        return np.sum(sumHeights)

    def avg_height(self):
        """
        这篇文章的每句话的语法分析树的平均高度
        :return:
        """
        return self.sum_of_heights() / len(self.sentences)

    def no_less_than_16(self):
        """
        计算整篇文本的高度不大于16的语法分析树的个数
        :return:
        """
        num = 0
        for sentence in self.sentences:
            res = self.tree(sentence)
            if len(res) >= 16:
                num += 1
        return num

    def no_less_than_16_percent(self):
        """
        高度不低于１６的语法分析树的比例
        :return:
        """
        return self.no_less_than_16() / len(self.sentences)

    def nodes_sum(self):
        """
        总节点数
        :return:
        """
        node_sums = []
        for sentence in self.sentences:
            res = self.nlp.parse(sentence)
            result = -1  # 去除root
            for i in res:
                if i == '(':
                    result += 1
            node_sums.append(result)
        return np.sum(node_sums)

    def avg_nodes_sentence(self):
        """
        每句话的平均节点
        :return:
        """
        return self.nodes_sum() / len(self.sentences)

    def seg_sentence(self, sentence):
        """
        输入字符串，返回分词后的列表
        :param sentence:
        :return:
        """
        jieba.load_userdict('../词典/userdict.txt')
        sentence_seged = jieba.cut(sentence.strip())
        outstr = ''
        for word in sentence_seged:
            if word not in self.stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr.split(' ')

    def avg_nodes_word(self):
        """
        每个词的平均节点
        :return:
        """
        # 计算有几个词
        num = 0
        for sentence in self.sentences:
            sentence = self.seg_sentence(sentence)
            num += len(sentence)
        return self.nodes_sum() / num

    def np_sum(self):
        """
        计算整篇文章里的名词短语个数
        :return:
        """
        num = 0
        for sentence in self.sentences:
            res = self.tree(sentence).split("\r\n")
            for i in res:
                if 'NP' in i:
                    num += 1
        return num

    def avg_np(self):
        """
        语法分析树的平均名词短语个数
        :return:
        """
        return self.np_sum() / len(self.sentences)

    def vp_sum(self):
        """
        计算整篇文章里的动词短语个数
        :return:
        """
        num = 0
        for sentence in self.sentences:
            print(sentence)
            res = self.tree(sentence).split("\r\n")
            for i in res:
                if 'VP' in i:
                    num += 1
        return num

    def avg_vp(self):
        """
        语法分析树的平均动词短语个数
        :return:
        """
        return self.vp_sum() / len(self.sentences)

    def adjp_sum(self):
        """
        计算整篇文章里的形容词短语个数
        :return:
        """
        num = 0
        for sentence in self.sentences:
            res = self.tree(sentence).split("\r\n")
            for i in res:
                if 'ADJP' in i:
                    num += 1
        return num

    def avg_adjp(self):
        """
        语法分析树的平均形容词短语个数
        :return:
        """
        return self.adjp_sum() / len(self.sentences)

    def get_res(self):
        res = {}
        res['sum_height'] = self.sum_of_heights()
        res['height_16'] = self.no_less_than_16()
        res['sum_node'] = self.nodes_sum()
        res['sum_n'] = self.np_sum()
        res['sum_v'] = self.vp_sum()
        res['sum_adj'] = self.adjp_sum()
        res['avg_height'] = self.avg_height()
        res['16_ratio'] = self.no_less_than_16_percent()
        res['avg_node'] = self.avg_nodes_sentence()
        res['word_avg_node'] = self.avg_nodes_word()
        res['avg_n'] = self.avg_np()
        res['avg_v'] = self.avg_vp()
        res['avg_adj'] = self.avg_adjp()
        return res
