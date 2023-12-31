# -*- coding: utf-8 -*-
"""exam05_heart_disease_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VnhrWIUt4hXlWZgDZH9nqTEOgheKgDYA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

column_name = ['age', 'sex', 'cp', 'treshbps', 'chol', 'fbs', 'restecg',
               'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'HeartDisease']
raw_data = pd.read_excel('./datasets/heart-disease.xlsx', header = None, names = column_name)
raw_data.head()       # 앞의 5개만 출력

print(raw_data.describe())      # 데이터의 정보 요약을 보고 싶을때 사용
                                # 칼럼별 총 데이터 수, 평균, 표준편차, 데이터 최소값,
                                # 백분위수의 각 지점으로 분포를 반영해 평균을 보완하는 목적, 데이터 최대값

raw_data.info()

clean_data = raw_data.replace('?', np.nan)    # NaN = 숫자가 아닌 것, 연산은 되지만 연산 결과는 무조건 NaN
clean_data = clean_data.dropna()
clean_data.info()

keep = column_name.pop()    # .pop() 리스트의 마지막 인덱스를 가져옴
print(keep)                 # 마지막 인덱스 HeartDisease가 keep에 저장됨
print(column_name)          # 마지막 인덱스 HeartDisease가 column_name에서 빠짐

training_data = clean_data[column_name]
target = clean_data[[keep]]
print(training_data.head())
print(target.head())

print(target['HeartDisease'].sum())

print(target['HeartDisease'].mean())    # 값이 지금처럼 반에 가깝지 않다면 반에 가깝게 맞춰줘야 함

"""스케일링을 하는 이유:
- 하나의 값이 너무 크면 결과값을 예측하는 데 있어서 그 값만 유무의한 영향을 끼친다.
- 값을 예측하는 데 있어 각각의 열의 비율만 따지기 때문에 비율만 유지하면 스케일링 하는데 문제가 없다.

"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(training_data)
scaled_data = pd.DataFrame(scaled_data, columns = column_name)
print(scaled_data.head())

print(scaled_data.describe().T)   # 평균은 0, 표준 편차는 1에 가깝게 모든 값을 스케일링한 것을 확인할 수 있음
# .T -> 행과 열의 위치를 바꿔서 출력

boxplot = scaled_data.boxplot(column = column_name, showmeans = True)
plt.show()

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    scaled_data, target, test_size = 0.3)
print('X_train shape :', X_train.shape)
print('Y_train shape :', Y_train.shape)
print('X_test shape :', X_test.shape)
print('Y_test shape :', Y_test.shape)

model = Sequential()
model.add(Dense(512, input_dim = 13, activation = 'relu'))
model.add(Dropout(0.25))                    # 과적합을 막기 위해서 사용, 레이어가 아님->
                                                # 랜덤하게 25%는 값을 수정을 하지 않는다.
                                                  # ex> faceID의 경우 한번은 코를 빼고 학습하고 한번은 입을, 이런 방식으로 25%씩 빼고 수정
model.add(Dense(256, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(1, activation = 'sigmoid'))
print(model.summary())

model.compile(loss = 'mse', optimizer = 'adam', metrics = ['binary_accuracy'])
fit_hist = model.fit(
    X_train, Y_train, batch_size = 50, epochs = 50, validation_split = 0.2, verbose = 1)
# validation_split = train_test_split으로 잘라서 남은 값의 20%를 또 잘라내서 검증데이터로 사용함
# 단, epochs = 50 번 돌렸기 때문에 모든 데이터를 학습에 사용함(사용되지 않을 확률 : 0.2*0.2*50번)
# 사용하는 이유 -> 모델을 너무 입력했을 경우 컴퓨터가 과적합(특정 패턴을 외우는 것)이 될 수 있기 때문에 사용
# 과적합이 일어나면 오히려 성능이 떨어지기 때문에 따로 20%를 떼어내서 검증한 뒤 과적합이 일어나면 중단시켜야 함
# 1 epochs -> 레이어가 모두 동작하고 출력값과 결과값을 비교하고 error를 찾아 미분하고 다시 역동작하는 것까지.
# batch_size -> 1 epochs에 여러번 weight 값과 bias를 계산하는데 데이터를 50개씩 잘라서 여러번 학습함을 의미
# ex> 데이터가 207개니까 1epochs 당 4번씩 학습함

plt.plot(fit_hist.history['binary_accuracy'])
plt.plot(fit_hist.history['val_binary_accuracy'])
plt.show()

score = model.evaluate(X_test, Y_test, verbose = 0)   # verbose = 0 이면 출력하지 않음
print('Keras DNN model lose :', score[0])           # loss 값
print('Keras DNN model accuracy :', score[1])       # 진단 정확도

from sklearn.metrics import confusion_matrix as cm
from sklearn.metrics import f1_score
pred = model.predict(X_test)
pred = (pred > 0.1)         # 조금이라도 이상이 있으면 검사를 받도록 유도
print(cm(Y_test, pred))
print(f1_score(Y_test, pred, average = 'micro'))

