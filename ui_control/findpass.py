import random
import string

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

from dao.id_dao import IDDao



class Find(QWidget):
    def __init__(self):
        super().__init__()
        self.idt = IDDao()
        self.ui = uic.loadUi('ui/findpass.ui')

        self.ui.btn_exit.clicked.connect(self.exit)
        self.ui.btn_find.clicked.connect(self.find)



        self.ui.show()

    def exit(self):
        self.ui.close()

    def find(self):
        id = self.ui.le_ID.text()
        name = self.ui.le_name.text()
        email = self.ui.le_email.text()

        try:
            count = 0
            if id ==self.idt.select_data(id,type='user_id')[0][0]:
                count = 1
                if name == self.idt.select_data(name,type='name')[0][1]:
                    count = 2
                    if email == self.idt.select_data(email,type='email')[0][2]:
                        _LENGTH = 15
                        _string = string.ascii_letters + string.digits
                        password = ""
                        for i in range(_LENGTH):
                            password += random.choice(_string)

                        QMessageBox.information(self, '비밀번호 찾기', '비밀번호는 ' + password + ' 로 변경되었습니다.', QMessageBox.Ok)
                        self.idt.find_pass(password, id, name, email)

        except:
            if count == 0:
                QMessageBox.information(self, '비밀번호 찾기', '아이디가 틀렸습니다', QMessageBox.Ok)
            elif count == 1:
                QMessageBox.information(self, '비밀번호 찾기', '이름이 틀렸습니다', QMessageBox.Ok)
            elif count == 2:
                QMessageBox.information(self, '비밀번호 찾기', '이메일이 틀렸습니다', QMessageBox.Ok)




