from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLineEdit, QMessageBox

from dao.id_dao import IDDao


class Sign_up(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/User_registration.ui")

        self.idt = IDDao()
        self.idt.select_item()

        self.ui.le_pass.setEchoMode(QLineEdit.Password)

        self.ui.com_grant.addItem('--select--')
        for i in range(len(self.idt.select_mode())-1):
            self.ui.com_grant.addItems(self.idt.select_mode()[i+1])

        self.ui.btn_ok.clicked.connect(self.sign_up)
        self.ui.btn_can.clicked.connect(self.exit)

        self.ui.le_pass.returnPressed.connect(self.sign_up)
        self.ui.le_id.returnPressed.connect(self.sign_up)
        self.ui.le_name.returnPressed.connect(self.sign_up)
        self.ui.le_email.returnPressed.connect(self.sign_up)


        self.ui.show()

    def sign_up(self):
        check = 0
        id = self.ui.le_id.text()
        password = self.ui.le_pass.text()
        mode = self.ui.com_grant.currentText()
        name = self.ui.le_name.text()
        email = self.ui.le_email.text()

        if mode == '--select--':
            QMessageBox.information(self, '사용자 등록', '유저 권한을 설정해 주세요.', QMessageBox.Ok)
        else:
            if self.idt.select_item('{}'.format(id)):
                QMessageBox.information(self, '사용자 등록', '해당 아이디가 이미 있습니다.', QMessageBox.Ok)
                check = 1
            if id == '':
                QMessageBox.information(self, '사용자 등록', '아이디를 입력해주세요.', QMessageBox.Ok)
            if email == '':
                QMessageBox.information(self, '사용자 등록', '이메일를 입력해주세요.', QMessageBox.Ok)
            if name == '':
                QMessageBox.information(self, '사용자 등록', '이름를 입력해주세요.', QMessageBox.Ok)
            else:
                if check == 0:
                    QMessageBox.information(self, '사용자 등록', '등록되었습니다.', QMessageBox.Ok)
                    self.idt.insert_item(id,password,mode,name,email)
                    self.idt.select_item()
                    self.clear()

    def exit(self):
        self.clear()
        self.ui.close()

    def clear(self):
        self.ui.le_pass.clear()
        self.ui.le_id.clear()
        self.ui.le_name.clear()
        self.ui.le_email.clear()