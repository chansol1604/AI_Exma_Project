import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import EarlyStopping    # 과적합을 막기 위해 사용
import matplotlib.pyplot as plt


X_train, X_test, Y_train, Y_test = np.load(
    'D:\work\python\AI_exam_project\datasets/binary_image_data.npy', allow_pickle =True)
# 폴더 경로는 '/', '\' 둘 다 사용 가능, 위의 경우에는 '\b'의 설정이 있어서 '\\', '/' 사용
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Conv2D(32, kernel_size = (3, 3), padding = 'same',
                 input_shape = (64, 64, 3), activation = 'relu'))
model.add(MaxPool2D(pool_size = (2, 2)))
model.add(Conv2D(32, kernel_size = (3, 3), padding = 'same',
                  activation = 'relu'))
model.add(MaxPool2D(pool_size = (2, 2)))
model.add(Conv2D(32, kernel_size = (3, 3), padding = 'same',
                  activation = 'relu'))
model.add(MaxPool2D(pool_size = (2, 2)))
model.add(Flatten())
model.add(Dense(256, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))
model.summary()

model.compile(loss = 'binary_crossentropy', optimizer = 'adam',
              metrics = ['binary_accuracy'])
early_stopping = EarlyStopping(monitor = 'val_binary_accuracy', patience = 5)
# val_binary_accuracy이 좋아지지 않으면 멈춤, patience = 5 -> 5에폭 동안 에폭이 낮거나 같으면 멈춤
fit_hist = model.fit(X_train, Y_train, batch_size = 64, epochs = 100,
                     validation_split = 0.15, callbacks = [early_stopping])
score = model.evaluate(X_test, Y_test)
print('Evaluation loss :', score[0])
print('Evaluation accuracy :', score[1])
model.save('./cat_and_dog_{}.h5'.format(str(np.around(score[1], 3))))
# 중괄호 안에 score[1]의 값을 소수점 3자리에서 반올림한 것을 넣어서 저장

plt.plot(fit_hist.history['binary_accuracy'], label = 'binary_accuracy')
plt.plot(fit_hist.history['val_binary_accuracy'], label = 'val_binary_accuracy')
plt.legend()
plt.show()
plt.plot(fit_hist.history['loss'], label = 'loss')
plt.plot(fit_hist.history['val_loss'], label = 'val_loss')
plt.show()


