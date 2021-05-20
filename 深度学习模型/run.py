#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from model import *
from train_test import *
from utils import *
from getdata import *

# 参数准备
args = parse_args()
days_num = args.days_num
epoch = args.epoch
fea = args.fea
batch_size = args.batch_size
early_stop = args.early_stop

# 初始化模型
model = Model(args.fea)

# 数据准备
GD = GetData()
x_train, x_test, y_train, y_test = GD.process_data()
x_train = torch.tensor(x_train).float()
x_test = torch.tensor(x_test).float()
y_train = torch.tensor(y_train).float()
y_test = torch.tensor(y_test).float()
train_data = TensorDataset(x_train, y_train)
train_dataLoader = DataLoader(train_data, batch_size=batch_size)
test_data = TensorDataset(x_test, y_test)
test_dataLoader = DataLoader(test_data, batch_size=batch_size)

# 定义损失函数与优化器
loss_func = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
train_model(epoch, train_dataLoader, test_dataLoader)
p, y, test_loss = test_model(test_dataLoader, fea)

pred = [ele * (GD.close_max - GD.close_min) + GD.close_min for ele in p]
data = [ele * (GD.close_max - GD.close_min) + GD.close_min for ele in y]
show_img(data, pred)
print(test_loss)