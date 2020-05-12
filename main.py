import readline
from PyQt5.QtWidgets import QApplication
from ui_control.login_ui import Login
from ui_control.init_ui import Init

if __name__ == '__main__':
    app = QApplication([])
    w = Login()
#     I = Init()
    app.exec_()
