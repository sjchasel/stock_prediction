import jieba
import pandas as pd
import re
import random

PATH = 'C:/Users/12968/Desktop/数据科学实战-stock prediction/程序/词典/'


class FourWords:
    def __init__(self, text):
        self.text = text
        self.stopwords = []

    def read_file(self, filename='C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/新浪公司研报.CSV'):
        """
        提取csv文件中的研报内容，存入list并返回
        :param filename:
        :return:
        """
        data = pd.read_csv(filename)
        return list(data.content)

    def dict_load(self, path):
        dict = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line.strip() != '':  # 养成去空好习惯
                    dict.append(line.strip())
        return dict

    def load_dicts(self):
        stop = PATH + 'stop1205.txt'
        self.stopwords = self.dict_load(stop)

    def seg_sentence(self):
        sentence = self.text
        sentence = re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', sentence))
        jieba.load_userdict('C:/Users/12968/Desktop/数据科学实战-stock prediction/程序/词典/userdict.txt')
        sentence_seged = jieba.cut(sentence.strip())
        outstr = ''
        for word in sentence_seged:
            if word not in self.stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        word_list = outstr.split(' ')
        pattern = '[A-Za-z]*[0-9]*[\'\"\%.\s\@\!\#\$\^\&\*\(\)\-\<\>\?\/\,\~\`\:\;]*[：；”“ ‘’+-——！，。？、~@#￥%……&*（）【】]*'
        t = [re.sub(pattern, "", x.strip()) for x in word_list]
        return [x for x in t if x != '']

    def cal_four(self):
        """
        计算四个字组成的词数占词总数的比例
        :return:
        """
        sum = 0
        for i in self.seg_sentence():
            if len(i) >= 4:
                sum += 1
        return sum / len(self.seg_sentence())


if __name__ == '__main__':
    data = pd.read_csv('C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/新浪公司研报.csv')
    samples = random.sample(list(data['content']), 500)
    result = []
    for sample in samples:
        four = FourWords(sample)
        result.append(four.cal_four())

    # data = pd.read_csv('C:/Users/12968/Desktop/数据科学实战-stock prediction/数据/新浪公司研报.csv')
    # result = []
    # duo = 0
    # duo_id = 0
    # shao = 100000000000
    # shao_id = 0
    # samples = random.sample(list(data['content']), 500)
    # for i in range(len(samples)):
    #     sample = samples[i]
    #     sample = re.sub(' ', '', re.sub('\xa0\xa0\xa0\r\n', '', sample))
    #     four = FourWords(sample)
    #     res = four.cal_four()
    #     result.append(res)
    #     if res >= duo:
    #         duo_id = i
    #         duo = res
    #         duo_sentence = four.seg_sentence()
    #     if res <= shao:
    #         shao_id = i
    #         shao = res
    #         shao_sentence = four.seg_sentence()
    #
    # # print(duo_id)
    # print(samples[duo_id])
    # print(result[duo_id])
    # print(duo_sentence)
    # print('-------------------')
    # # print(shao_id)
    # print(samples[shao_id])
    # print(result[shao_id])
    # print(shao_sentence)
