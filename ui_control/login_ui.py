from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit

from ui_control.findpass import Find
from dao.id_dao import IDDao
from ui_control.User_registration import Sign_up
from ui_control.main_menu import Main


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/log_in.ui")

        self.idt = IDDao()
        self.res = self.idt.select_item()

        self.ui.le_pass.setEchoMode(QLineEdit.Password)

        self.ui.btn_sign.clicked.connect(self.sign_up_ui)
        self.ui.btn_login.clicked.connect(self.sign_in)
        self.ui.btn_find.clicked.connect(self.find_pass)

        # line edit에서 enter키
        self.ui.le_pass.returnPressed.connect(self.sign_in)
        self.ui.le_id.returnPressed.connect(self.sign_in)

        self.ui.show()

    def sign_up_ui(self):
        self.s = Sign_up()

    def sign_in(self):
        self.res = self.idt.select_item()
        count = 0
        passerr = 0
        corr = [(1,)]
        password = self.ui.le_pass.text()
        login_id = self.ui.le_id.text()

        for id,mode,name in self.res:
            if login_id != id:
                count = -1
            else:
                if self.idt.select_password_item(login_id, password) == corr:
                    #ui 호출
                    self.ui.close()
                    self.main = Main()
                    self.main.ui.btn_out.clicked.connect(self.ui.show)
                    self.main.ui.lbl_ID.setText(self.idt.select_item(id)[0][0])
                    self.main.ui.lbl_mode.setText(self.idt.select_item(id)[0][1])
                    self.check_grant()
                    self.clear()

                    return
                else:
                    QMessageBox.information(self, '로그인', '비밀번호가 틀립니다.', QMessageBox.Ok)
                    count += 1
                    passerr = 1
        if passerr == 1:
            count = 0

        if count < 0:
            QMessageBox.information(self, '로그인', '해당 아이디가 없습니다.', QMessageBox.Ok)

        count = 0

    def clear(self):
        self.ui.le_pass.clear()
        self.ui.le_id.clear()

    def check_grant(self):
        grant = []
        for i in range(len(IDDao().select_grant('admin'))):
            a = IDDao().select_grant(self.main.ui.lbl_ID.text()).count(IDDao().select_grant('admin')[i])
            grant.append(a)

        if grant[1] == 0:
            self.main.ui.btn_sale.hide()
        if grant[2] == 0:
            self.main.ui.btn_manage.hide()

    def find_pass(self):
        self.find = Find()