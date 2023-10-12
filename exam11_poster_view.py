import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_window = uic.loadUiType('./poster.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.btn_nr.clicked.connect(self.btn_nr_clicked_slot)
        # self.btn_mv.clicked.connect(self.btn_mv_clicked_slot)
        # self.btn_gog.clicked.connect(self.btn_gog_clicked_slot)
        # self.btn_dr.clicked.connect(self.btn_dr_clicked_slot)
        self.btn_nr.clicked.connect(self.btn_clicked_slot) # 버튼과 함수 연결
        self.btn_mv.clicked.connect(self.btn_clicked_slot)
        self.btn_gog.clicked.connect(self.btn_clicked_slot)
        self.btn_dr.clicked.connect(self.btn_clicked_slot)

    def btn_clicked_slot(self):
        btn = self.sender()     # btn에 버튼 정보 받아서 저장
        self.lbl_nr.hide()
        self.lbl_mv.hide()
        self.lbl_gog.hide()
        self.lbl_dr.hide()
        if btn.objectName() == 'btn_nr': self.lbl_nr.show()
        elif btn.objectName() == 'btn_mv': self.lbl_mv.show()
        elif btn.objectName() == 'btn_gog': self.lbl_gog.show()
        elif btn.objectName() == 'btn_dr': self.lbl_dr.show()

    # def btn_nr_clicked_slot(self):
    #     self.lbl_nr.hide()
    #     self.lbl_mv.hide()
    #     self.lbl_gog.hide()
    #     self.lbl_dr.hide()
    #     self.lbl_nr.show()
    #
    # def btn_mv_clicked_slot(self):
    #     self.lbl_nr.hide()
    #     self.lbl_mv.hide()
    #     self.lbl_gog.hide()
    #     self.lbl_dr.hide()
    #     self.lbl_mv.show()
    #
    # def btn_gog_clicked_slot(self):
    #     self.lbl_nr.hide()
    #     self.lbl_mv.hide()
    #     self.lbl_gog.hide()
    #     self.lbl_dr.hide()
    #     self.lbl_gog.show()
    #
    # def btn_dr_clicked_slot(self):
    #     self.lbl_nr.hide()
    #     self.lbl_mv.hide()
    #     self.lbl_gog.hide()
    #     self.lbl_dr.hide()
    #     self.lbl_dr.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())



