# -*- coding: utf-8 -*-
"""exam14_predict_daily_stock_price

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12proyMewwTawhtGRn99aNZx365pIcAog
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

raw_data = pd.read_csv('./datasets/samsung231009.csv')
print(raw_data.head())
raw_data.info()

raw_data['Date'] = pd.to_datetime(raw_data['Date'])
raw_data.info()
raw_data.set_index('Date', inplace = True)
print(raw_data.head())

raw_data['Close'].plot()
plt.show()

data_test = raw_data.sort_values('Close')
print(data_test.head())
print(data_test.tail())

data_close = raw_data[['Close']]
print(data_close.head())

minmaxscaler = MinMaxScaler()
scaled_data = minmaxscaler.fit_transform(data_close)
print(scaled_data[:5])
print(scaled_data.shape)

sequence_X = []
sequence_Y = []
for i in range(len(scaled_data)-30):
  x = scaled_data[i:i+30]
  y = scaled_data[i+30]
  sequence_X.append(x)
  sequence_Y.append(y)
print(sequence_X[:5])
print(sequence_Y[:5])

sequence_X = np.array(sequence_X)
sequence_Y = np.array(sequence_Y)
print(sequence_X[0])
print(sequence_Y[0])
print(sequence_X.shape)
print(sequence_Y.shape)

X_train, X_test, Y_train, Y_test = train_test_split(
    sequence_X, sequence_Y, test_size = 0.2
)
print(X_train.shape, X_test.shape)
print(Y_train.shape, Y_test.shape)

model = Sequential()
model.add(LSTM(50, input_shape = (30, 1), activation = 'tanh'))      # lstm 사용시 'tanh' 사용
# LSTM, Simple_RNN, GRU
model.add(Flatten())
model.add(Dense(1))         # activation 사용하지 않음, 값을 예측하는 것이기 때문에 activation을 사용하면 예측값을 건듬
model.compile(loss='mse', optimizer = 'adam')
model.summary()

fit_hist = model.fit(X_train, Y_train, epochs = 100, validation_data = (X_test, Y_test), shuffle = False)
# shuffle = False. 평소에는 데이터를 섞어서 학습했는데 이번 같은 경우에는 순서도 중요해서 False

plt.plot(fit_hist.history['loss'][10:], label = 'loss')
plt.plot(fit_hist.history['val_loss'][10:], label = 'validation loss')
plt.legend()
plt.show()

model.save('./stock_close_predict.h5')

pred = model.predict(X_test)

plt.plot(Y_test[:30], label = 'actural')
plt.plot(pred[:30], label = 'predict')
plt.legend()
plt.show()

last_data_30 = scaled_data[-30:].reshape(1, 30, 1)
today_close = model.predict(last_data_30)
print(today_close)

today_close_won = minmaxscaler.inverse_transform(today_close)
print('%d 원' %today_close_won[0][0])

last_data_29 = scaled_data[-29:]
last_data_29_today = np.append(last_data_29, today_close)
last_data_29_today = last_data_29_today.reshape(1, 30, 1)

tomorrow_pred = model.predict(last_data_29_today)
tomorrow_pred_won = minmaxscaler.inverse_transform(tomorrow_pred)
print('%d 원'%tomorrow_pred_won[0][0])

pd.DataFrame(scaled_data[-30:]).plot()

