import sys
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import numpy as np
from tensorflow.keras.models import load_model
from PyQt5 import uic


form_window = uic.loadUiType('./cat_and_dog.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(600)
        self.setFixedHeight(600)
        self.setupUi(self)
        self.btn_open.clicked.connect(self.btn_clicked_slot) # 버튼의 클릭 시그널을 함수에 연결
        model_path = './cat_and_dog_0.834.h5'
        self.model = load_model(model_path)
        self.path = ('../datasets/test/cat01.jpg', '')
        pixmap = QPixmap(self.path[0])
        self.lbl_img.setPixmap(pixmap)

    def btn_clicked_slot(self):
        old_path = self.path
        self.path = QFileDialog.getOpenFileName(self, 'Open file',
        '../datasets', 'Image Files(*.jpg;*.png);;All Files(*.*)')
        if self.path[0] == '': self.path = old_path     #취소 누른 경우를 위한 예외처리
        pixmap = QPixmap(self.path[0])
        self.lbl_img.setPixmap(pixmap)
        try:                                        # 파일 오픈 실패를 위한 예외처리
            img = Image.open(self.path[0])
            img = img.convert('RGB')
            img = img.resize((64, 64))
            data = np.asarray(img)
            data = data / 255
            data = data.reshape(1, 64, 64, 3)
            pred = self.model.predict(data)
            print(pred)
            if pred < 0.5:
                self.lbl_result.setText('고양이 입니다.')
            else : self.lbl_result.setText('강아지 입니다.')
        except:
            print('error : {}'.format(self.path[0]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())



