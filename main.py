import readline
from PyQt5.QtWidgets import QApplication
from ui_control.login_ui import Login

if __name__ == '__main__':
    app = QApplication([])
    w = Login()
    app.exec_()
