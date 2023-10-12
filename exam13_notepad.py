import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

################################### 단축기 지정은 디자이너에서 설정 #############################
form_window = uic.loadUiType('./qt_notepad.ui')[0]

class Exam(QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.edited_flag = False
        self.path = ['제목 없음', '']
        self.title = self.path[0] + " - Qt Note Pad"
        self.setWindowTitle(self.title)

        self.actionNew.triggered.connect(self.action_new_slot)
        self.actionOpen.triggered.connect(self.action_open_slot)
        self.actionSave.triggered.connect(self.action_save_slot)
        self.actionSave_as.triggered.connect(self.action_save_as_slot)
        self.actionExit.triggered.connect(self.action_exit_slot)

        self.actionUndo.triggered.connect(self.plainTextEdit.undo)      # 기본으로 제공되는 함수
        self.actionCut.triggered.connect(self.plainTextEdit.cut)        # 기본으로 제공되는 함수
        self.actionCopy.triggered.connect(self.plainTextEdit.copy)      # 기본으로 제공되는 함수
        self.actionPaste.triggered.connect(self.plainTextEdit.paste)    # 기본으로 제공되는 함수
        self.actionDelete.triggered.connect(self.plainTextEdit.cut)     # delete는 제공되지 않음

        self.actionFont.triggered.connect(self.action_font_slot)

        self.actionAbout.triggered.connect(self.action_about_slot)


        self.plainTextEdit.textChanged.connect(self.text_changed_slot)  # plainTextEdit에 입력이 들어오는 지 확인
        self.statusbar.showMessage(self.path[0])        # statusbar 에 메시지 띄우는 방법



    def set_title(self):                 # title 제목 지정
        self.title = self.path[0].split('/')[-1] + " - Qt Note Pad"     # 경로에서 파일명만 지정
        self.setWindowTitle(self.title)
        self.edited_flag = False
        self.statusbar.showMessage(self.path[0])

    def text_changed_slot(self):    
        self.edited_flag = True
        self.setWindowTitle('*'+self.title)


    def action_new_slot(self):
        if self.edited_flag:
            ans = QMessageBox.question(self, '저장하기', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Cancel | QMessageBox.Yes,
                                       QMessageBox.Yes) # question 박스라 파란 물음표 표식, 따로 씀, QMessageBox.yes는 포커스 지정
            if ans == QMessageBox.Yes:
                if self.action_save_slot():
                    return
            elif ans == QMessageBox.Cancel: return
        self.plainTextEdit.setPlainText('')
        self.path = ['제목 없음', '']
        self.set_title()

    def action_open_slot(self):
        if self.edited_flag:
            ans = QMessageBox.question(self, '저장하기', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Cancel | QMessageBox.Yes,
                                       QMessageBox.Yes)
            if ans == QMessageBox.Yes: self.action_save_slot()
            elif ans == QMessageBox.Cancel: return
        old_path = self.path
        self.path = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Text File(*.txt);; Python File(*.py);; All File(*.*)'
        )
        if self.path[0] != '':
            with open(self.path[0], 'r') as f:
                str_read = f.read()
                self.plainTextEdit.setPlainText(str_read)       # plainText는 setPlainText()로 받아야 함
                self.set_title()
        else: self.path = old_path

    def action_save_slot(self):
        if self.path[0] != '제목 없음':
            with open(self.path[0], 'w') as f:
                f.write(self.plainTextEdit.toPlainText())
            self.set_title()
        else: return self.action_save_as_slot();

    def action_save_as_slot(self):
        old_path = self.path
        self.path = QFileDialog.getSaveFileName(
            self, 'Save file', '', 'Text Files(*.txt);; Python Files(*.py);; All Files(*.*)'
        )       # 경로만 리턴해 줌, 실제로 저장안 함
        print(self.path)
        if self.path[0] != '':
            with open(self.path[0], 'w') as f:
                f.write(self.plainTextEdit.toPlainText())   # plainText는 toplainText()로 읽어야 함
            self.set_title()
            return 0
        else:
            self.path = old_path
            return 1

    def action_exit_slot(self):
        if self.edited_flag:
            ans = QMessageBox.question(self, '저장하기', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Cancel | QMessageBox.Yes,
                                       QMessageBox.Yes)
            if ans == QMessageBox.Yes:
                if self.action_save_slot():
                    return
            elif ans == QMessageBox.Cancel:
                return
        self.close()


    def action_font_slot(self):
        font = QFontDialog.getFont()    # ex) (<PyQt5.QtGui.QFont object at 0x00000187B1629510>, True)
        if font[1]:         # ok 를 누르면 True, Cancle 을 누르면 False
            self.plainTextEdit.setFont(font[0]) # Font에 대한 정보, ex) <PyQt5.QtGui.QFont object at 0x00000187B1629510>


    def action_about_slot(self):
        QMessageBox.about(
            self, 'PyQT Notepad', '''만든이 : ABC lab\n\r버전 정보 : 1.0.0''')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())



