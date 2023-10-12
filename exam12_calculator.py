import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_window = uic.loadUiType('./calculator.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.first_input_flag = True
        self.opcode = ''
        self.number1 = None
        btns = [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
                self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9]
        for idx, btn in enumerate(btns):
            btn.clicked.connect(self.btn_number_clicked_slot)
            btn.setShortcut(str(idx))
        btn_ops = [self.btn_add, self.btn_sub, self.btn_mul, self.btn_div, self.btn_eq]
        shortcut_opcode = ['+', '-', '*', '/', 'Return']
        for idx, btn in enumerate(btn_ops):
            btn.clicked.connect(self.btn_op_clicked_slot)
            btn.setShortcut(shortcut_opcode[idx])
        self.btn_cl.clicked.connect(self.btn_clear_clicked_slot)


    def btn_number_clicked_slot(self):
        btn = self.sender()
        if(self.first_input_flag or self.lbl_num.text()=='0'):
            self.first_input_flag = False
            self.lbl_num.setText('')
        self.lbl_num.setText(self.lbl_num.text() + btn.objectName()[-1])

    def btn_op_clicked_slot(self):
        if not self.first_input_flag:
            self.first_input_flag = True
            self.calculate()
        self.number1 = float(self.lbl_num.text())
        self.opcode = self.sender().objectName()[-3:]
        # print(self.opcode)
        # print(self.number1)

    def calculate(self):
        number2 = float(self.lbl_num.text())
        if self.opcode == 'add':
            self.lbl_num.setText(str(self.number1 + number2))
        elif self.opcode == 'sub':
            self.lbl_num.setText(str(self.number1 - number2))
        elif self.opcode == 'mul':
            self.lbl_num.setText(str(self.number1 * number2))
        elif self.opcode == 'div':
            if number2: self.lbl_num.setText(str(self.number1 / number2))
            else: self.lbl_num.setText('infinity')  # infinity는 무한대 값, float으로 형변환이 가능

    def btn_clear_clicked_slot(self):
        self.first_input_flag = True
        self.opcode = ''
        self.number1 = None
        self.lbl_num.setText('0')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())



