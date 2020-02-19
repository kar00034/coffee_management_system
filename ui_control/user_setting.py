from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLineEdit, QMessageBox

from dao.id_dao import IDDao


class Setting(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui/user_setting.ui')
        self.ui.lbl_id.setText('a')

        self.ui.le_pass.setEchoMode(QLineEdit.Password)

        self.ui.btn_ok.clicked.connect(self.update)
        self.ui.btn_can.clicked.connect(self.exit)

        self.ui.show()

    def update(self):
        name = self.ui.le_name.text()
        password = self.ui.le_pass.text()
        email = self.ui.le_email.text()
        self.idt = IDDao()
        print(self.idt.select_item_id(self.ui.lbl_id.text())[0][1])
        self.idt.update_setting(self.ui.lbl_id.text(),name, password, email)
        self.ui.lbl_name.setText(self.idt.select_item_id(self.ui.lbl_id.text())[0][0])
        QMessageBox.information(self, '사용자 정보', '변경되었습니다.', QMessageBox.Ok)



    def exit(self):
        self.ui.close()