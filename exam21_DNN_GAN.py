#GAM = 적대적 생성망, 서로 적대적으로 학습한다.
import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import *
from tensorflow.keras.models import *



OUT_DIR = './DNN_out'
img_shape = (28, 28, 1)
epochs = 100000
batch_size = 128
noise = 100                 # 노이즈 100픽셀
sample_interval = 100       # 100에폭 돌때마다 이미지 만들어서 저장하기 위함

(X_train, _), (_, _) = mnist.load_data()
print(X_train.shape)

X_train = X_train /127.5 - 1    # -1 ~ 1의 값
X_train = np.expand_dims(X_train, axis=3)   # reshape, 축 하나 늘림
print(X_train.shape)

generator = Sequential()
generator.add(Dense(128, input_dim=noise))
generator.add(LeakyReLU(alpha=0.01))    # 마이너스의 값도 사용하기 위함(alpha = 마이너스를 사용하는 기울기 값)
generator.add(Dense(784, activation='tanh'))
generator.add(Reshape(img_shape))
generator.summary()

lrelu = LeakyReLU(alpha=0.01)
discriminator = Sequential()
discriminator.add(Flatten(input_shape=img_shape))
discriminator.add(Dense(128, activation=lrelu))
discriminator.add(Dense(1, activation='sigmoid'))
discriminator.summary()

discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

gan_model = Sequential()
gan_model.add(generator)
gan_model.add(discriminator)
gan_model.summary()

gan_model.compile(loss='binary_crossentropy', optimizer='adam')

real = np.ones((batch_size, 1))
fake = np.zeros((batch_size, 1))
# print(real)
# print(fake)

for epochs in range(epochs):
    idx = np.random.randint(0, X_train.shape[0], batch_size)    # 0부터 60000 사이의 값을 128개를 랜덤으로 뽑음
    real_imgs = X_train[idx]

    z = np.random.normal(0, 1, (batch_size, noise))
    fake_imgs = generator.predict(z)

    d_hist_real = discriminator.train_on_batch(real_imgs, real)     # 데이터를 한 번 학습하고 끝냄
    d_hist_fake = discriminator.train_on_batch(fake_imgs, fake)

    d_loss, d_acc = 0.5 * np.add(d_hist_real, d_hist_fake)          # 평균 loss, acc 값 계산
    discriminator.trainable = False                                 # gan_model 학습시 discriminator 학습 정지

    if epochs % 2 == 0:             # generator가 학습을 더 잘해서 2번당 1번
        z = np.random.normal(0, 1, (batch_size, noise))
        gan_hist = gan_model.train_on_batch(z, real)

    if epochs % sample_interval == 0:
        print('%d [D loss: %f, acc : %.2f%%] [G loss: %f]'%(epochs, d_loss, d_acc*100, gan_hist))
        row = col = 4
        z = np.random.normal(0, 1, (row * col, noise))
        fake_imgs = generator.predict(z)
        fake_imgs = 0.5 * fake_imgs
        _, axs = plt.subplots(row, col, figsize=(row, col), sharey=True, sharex=True)
        count = 0
        for i in range(row):
            for j in range(col):
                axs[i, j].imshow(fake_imgs[count, :, :, 0], cmap='gray')
                axs[i, j].axis('off')
                count += 1

        path = os.path.join(OUT_DIR, 'immg-{}'.format(epochs+1))
        plt.savefig(path)
        plt.close()
