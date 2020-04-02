from PyQt5 import QtWidgets, uic

from db_connection.coffee_init_service import DbInit


class Init(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ui = uic.loadUi("ui/init.ui")

        self.ui.btn_init.clicked.connect(self.start)

        self.ui.show()

    def start(self):
        db = DbInit()
        # db.service()
        if db.service() == 0:
            print("suc")
        else:
            print("fail")