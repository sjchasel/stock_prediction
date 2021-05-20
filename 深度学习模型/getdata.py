#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from utils import *
import pandas as pd


class GetData:

    def __init__(self):
        self.args = parse_args()
        self.data = pd.read_csv(self.args.data_path)
        self.data = self.data[['open', 'high', 'low', 'close', 'volume', 'date']]

    def preprocess(self):
        # 把日期设为索引
        self.data = self.data.set_index('date')
        # 归一化
        self.data = self.data.apply(lambda x: (x - min(x)) / (max(x) - min(x)))

    def process_data(self):
        n = self.args.days_num
        split_ratio = self.args.split_ratio
        # 拆分数据集
        feature = [
            self.data.iloc[i: i + n].values.tolist()
            for i in range(len(self.data) - n + 2)
            if i + n < len(self.data)
        ]
        label = [
            self.data.close.values[i + n]
            for i in range(len(self.data) - n + 2)
            if i + n < len(self.data)
        ]
        num = int(len(feature) * split_ratio)
        train_x = feature[:num]
        test_x = feature[num:]
        train_y = label[:num]
        test_y = label[num:]
        return train_x, test_x, train_y, test_y
