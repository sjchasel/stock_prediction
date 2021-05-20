#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import argparse
import torch
import os
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm
from copy import deepcopy as copy
from torch.utils.data import DataLoader, TensorDataset
sns.set()
def seed_torch(seed=1122):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed) # 为了禁止hash随机化，使得实验可复现
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
seed_torch()
import sys
import warnings
import os
if not sys.warnoptions:
    warnings.simplefilter('ignore')

def parse_args(args=None):
    """
    传递参数
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-days_num", type=int, default=5, help='')
    parser.add_argument("-epoch", type=int, default=20, help='')
    parser.add_argument("-fea", type=int, default=5, help='')
    parser.add_argument("-batch_size", type=int, default=20, help='')
    parser.add_argument("-early_stop", type=int, default=5, help='')
    parser.add_argument("-data_path", type=str, default="history_sh.000002_stock_k_data.csv", help='')
    parser.add_argument("-split_ratio", default=0.9, help='')

    args = parser.parse_args(args)
    return args

