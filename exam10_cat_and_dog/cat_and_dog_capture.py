import sys
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_window = uic.loadUiType('./cat_and_dog.ui')[0]
# uic = ui 를 class 로 만들어 줌
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = load_model('./cat_and_dog_0.834.h5')

        self.btn_open.clicked.connect(self.btn_clicked_slot)

    def btn_clicked_slot(self):
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        flag = True

        while flag:
            v, frame = capture.read()
            if (v):
                cv2.imshow('VideoFrame', frame)
                cv2.imwrite('./capture.png', frame)
            # time.sleep(0.01)
            print(v)
            key = cv2.waitKey(50)  # key 입력을 50ms 동안 대기(20 프레임)
            # cv2.imshow('VideoFrame', frame)가 주석처리 되어 있으면 key 입력이 안됨
            if key == 27:  # esc 키 이름
                flag = False

            pixmap = QPixmap('./capture.png')
            self.lbl_img.setPixmap(pixmap)

            try:  # 파일 오픈 실패를 위한 예외처리
                img = Image.open('./capture.png')
                img = img.convert('RGB')
                img = img.resize((64, 64))
                data = np.asarray(img)
                data = data / 255   # 0~1 사이의 값을 만들기 위해 min-max 스케일링
                                    # 픽셀 값은 0~255사이의 값이기 때문에 255로 나눔
                data = data.reshape(1, 64, 64, 3)

                pred = self.model.predict(data)
                print(pred)
                if pred < 0.5:
                    self.lbl_result.setText('고양이 입니다.')
                else:
                    self.lbl_result.setText('강아지 입니다.')
            except:
                print('error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())





