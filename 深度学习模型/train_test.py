#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from model import *

def train(epoch, train_dataloader, test_dataloader):
    best_model = None
    train_loss = 0
    test_loss = 0
    best_loss = 10000
    epoch_cnt = 0

    for _ in range(epoch):
        total_train_loss = 0
        total_train_num = 0
        total_test_loss = 0
        total_test_num = 0

        for x, y in tqdm(train_dataloader,
                         desc='Epoch: {}| Train Loss: {}| Test Loss: {}'.format(_, train_loss, test_loss)):
            x_num = len(x)  # 这批数据中有几个样本
            lstm_model = model(x)
            loss = loss_func(lstm_model, y)
            optimizer.zero_grad()  # 优化器清零梯度
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()
            total_train_num += x_num

        train_loss = total_train_loss / total_train_num  # 平均每个样本的train_loss

        for x, y in test_dataloader:
            x_num = len(x)
            lstm_model = model(x)
            loss = loss_func(lstm_model, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_test_loss += loss.item()
            total_test_num += x_num
        test_loss = total_test_loss / total_test_num  # 平均每个样本上的test_loss

        # early_stop，防止过拟合
        if best_loss > test_loss:
            best_loss = test_loss
            best_model = copy(model)
            torch.save(best_model.state_dict(), 'lstm.pth')
            epoch_cnt = 0
        else:
            epoch_cnt += 1  # 记录着已经有几个epoch是loss没下降了

        if epoch_cnt > early_stop:
            # 如果已经有early_stop个epoch，loss没下降，就停止训练
            torch.save(best_model.state_dict(), 'lstm.pth')
            break

def test_model(test_dataloader, feature_num):
    pred = []
    label = []
    model_ = Model(feature_num)  # 传入特征数作为input_size
    model_.load_state_dict(torch.load("lstm.pth"))  # 加载训练所得的模型
    model_.eval()  # 不启用 BatchNormalization 和 Dropout，保证BN和dropout不发生变化
    total_test_loss = 0
    total_test_num = 0
    for x, y in test_dataloader:
        x_num = len(x)  # 这批有多少数据
        lstm_model = model_(x)  # 把数据输入模型
        loss = loss_func(lstm_model, y)
        total_test_loss += loss.item()
        total_test_num += x_num
        # 把预测值和真实值加入列表，之后用于画图
        pred.extend(lstm_model.data.squeeze(1).tolist())
        label.extend(y.tolist())
    test_loss = total_test_loss / total_test_num
    return pred, label, test_loss


def show_img(data, pred):
    plt.plot(range(len(pred)), pred, color='green')
    plt.plot(range(len(data)), data, color='b')
    # for i in range(0, len(pred) - 3, 5):
    #     price = [data[i] + pred[j] - pred[i] for j in range(i, i + 3)]
    #     plt.plot(range(i, i + 3), price, color='r')
    plt.xlabel('Date')
    plt.ylabel('close')
    plt.show()