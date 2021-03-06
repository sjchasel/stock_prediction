#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from preprocess import *

class ParagraphFeature:

    def __init__(self, text):
        self.text = text

    def sum_paragraph(self):
        """
        段落数
        :return:
        """
        return len(split_paragraph(self.text))

    def sentences_per_para(self):
        """
        平均段落句子数
        :return:
        """
        para_sum = self.sum_paragraph()
        if para_sum == 0:
            print("段落数为0，出错数据为"+str(self.text))
            return '-'
        else:
            sentence_corse = len(split_sentence_coarse(self.text))
            return sentence_corse / para_sum
    
    def get_res(self):
        res = {}
        res['sum_para'] = self.sum_paragraph()
        res['sen_per_para'] = self.sentences_per_para()
        return res



