from PIL import Image       # pillow, 이미지를 다루는 패키지
import glob
import numpy as np
from sklearn.model_selection import train_test_split


img_dir = '../datasets/train/'          # 이미지 경로
categories = ['cat', 'dog']
image_w = 64
image_h = 64

pixel = image_h * image_w * 3

X = []
Y = []
files = None

for idx, category in enumerate(categories):     # index를 앞에 붙여줌(ex> 0,1의 값이 idx값에 들어감)
                                                         # 고양이는 0, 강아지는 1이 됨
    files = glob.glob(img_dir + category + '*.jpg')
    # ()에 쓰인 형태들의 리스트를 반환
    for i, f in enumerate(files):
        try:
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((image_w, image_h))
            data = np.asarray(img)
            X.append(data)
            Y.append(idx)
            if i % 300 == 0:
                print(category, ':', f)
        except:
            print('error :', category, i)
X = np.array(X)
Y = np.array(Y)
X = X / 255

print(X[0])
print(Y[0])

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size =0.1)

xy = (X_train, X_test, Y_train, Y_test)

np.save('../datasets/binary_image_data.npy', xy)    # 피클 패키지, 데이터 타입을 변환 없이 그대로 저장
