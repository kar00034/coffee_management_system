import os
import time

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QLineEdit, QAction

from dao.id_dao import IDDao
from data.table import create_table
from db_connection.Backup import BackupRestore
from db_connection.coffee_init_service import DbInit


class management_system(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/manager.ui")
        self.idt = IDDao()

        self.ui.btn_edit_user.setEnabled(False)

        # self.ui.lbl_ID.setText('a')
        # self.ui.lbl_mode.setText(self.idt.select_item(self.ui.lbl_ID.text())[0][1])

        self.table_user = create_table(table=self.ui.table_user, data=['ID','이름','권한','이메일'])
        self.load_user()
        # self.check_grant()

        self.ui.le_pass.setEchoMode(QLineEdit.Password)

        self.ui.com_grant.addItem('--select--')
        for i in range(len(self.idt.select_mode())):
            self.ui.com_grant.addItems(self.idt.select_mode()[i])

        self.set_context_menu(self.ui.table_user)
        self.ui.btn_init.clicked.connect(self.coffee_init)
        self.ui.btn_backup.clicked.connect(self.Backup)
        self.ui.btn_restore.clicked.connect(self.Restore)
        self.ui.btn_del_user.clicked.connect(self.del_user)
        self.ui.btn_insert_user.clicked.connect(self.ins_user)
        self.ui.btn_edit_user.clicked.connect(self.edit_user)

        self.ui.btn_exit.clicked.connect(self.exit)
        self.ui.show()

    def exit(self):
        self.ui.close()

    def msgbox1(self):
        QMessageBox.information(self, "Success", "초기화 성공")

    def msgbox2(self):
        QMessageBox.information(self, "Failed", "초기화 실패")

    def msgbox3(self):
        QMessageBox.information(self, "Success", "백업 성공")

    def msgbox3_1(self):
        QMessageBox.information(self, "Failed", "백업 실패")

    def msgbox4(self):
        QMessageBox.information(self, "Success", "복구 성공")

    def msgbox4_1(self):
        QMessageBox.information(self, "Failed", "복구 실패")

    def coffee_init(self):
        db = DbInit()
        # db.service()
        if db.service() == 0:
            self.msgbox1()
        else:
            self.msgbox2()

    def Backup(self):
        br = BackupRestore()
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        mkdir_backup = '/tmp/backup/' + now_date
        os.system('mkdir ' + mkdir_backup)
        os.system('chmod 777 '+mkdir_backup)
        tablename = ['product', 'sale', 'sale_detail', 'mode_grant', 'category', 'user_data', 'user_mode']
        try:
            for i in range(len(tablename)):
                br.data_backup(table_name=tablename[i])
        except:
            pass


    def Restore(self):
        br = BackupRestore()
        # br.delete_all_table()
        tablename = ['product','sale','sale_detail','mode_grant','category','user_data','user_mode']
        for i in range(len(tablename)):
            br.data_restore(table_name=tablename[i])

    def check_grant(self):
        grant = []
        for i in range(len(IDDao().select_grant('admin'))):
            a = IDDao().select_grant(self.ui.lbl_ID.text()).count(IDDao().select_grant('admin')[i])
            grant.append(a)
        # [view, sale, manage_pro, manage_user, system]

        if grant[4] == 0:
            self.ui.tab_manage.removeTab(1)
        if grant[3] == 0:
            self.ui.tab_manage.removeTab(0)

    #table
    def load_user(self):
        self.ui.table_user.setRowCount(0)
        res = self.idt.select_item_mode()
        for (ID, name, mode, email) in res:
            item_ID, item_name, item_mode, item_email = self.user_create_item(ID, name, mode, email)
            nextIdx = self.ui.table_user.rowCount()
            self.ui.table_user.insertRow(nextIdx)
            self.ui.table_user.setItem(nextIdx, 0, item_ID)
            self.ui.table_user.setItem(nextIdx, 1, item_name)
            self.ui.table_user.setItem(nextIdx, 2, item_mode)
            self.ui.table_user.setItem(nextIdx, 3, item_email)


    def user_create_item(self, ID, name, mode, email):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, ID)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_mode = QTableWidgetItem()
        item_mode.setTextAlignment(Qt.AlignCenter)
        item_mode.setData(Qt.DisplayRole, mode)

        item_email = QTableWidgetItem()
        item_email.setTextAlignment(Qt.AlignCenter)
        item_email.setData(Qt.DisplayRole, email)

        return item_code,item_name,item_mode,item_email

    #user_manage
    def del_user(self):
        selectionIdxs = self.ui.table_user.selectedIndexes()[0]
        user_id = self.ui.table_user.item(selectionIdxs.row(),0).text()

        self.ui.table_user.removeRow(selectionIdxs.row())
        self.idt.delete_item(user_id)

    def ins_user(self):
        item_mode = self.ui.com_grant.currentText()
        count = 0
        if item_mode == '--select--':
            QMessageBox.information(self, '사용자 관리', '유저 권한을 설정해 주세요.', QMessageBox.Ok)
        else:
            item_id = self.ui.le_user_id.text()
            item_name = self.ui.le_name.text()
            item_email = self.ui.le_email.text()
            item_pass = self.ui.le_pass.text()

        if item_id == '':
            QMessageBox.information(self, '사용자 관리', '아이디를 입력해주세요.', QMessageBox.Ok)
            count = 1
        if item_name == '':
            QMessageBox.information(self, '사용자 관리', '이름을 입력해주세요.', QMessageBox.Ok)
            count = 1
        if item_email == '':
            QMessageBox.information(self, '사용자 관리', '이메일을 입력해주세요.', QMessageBox.Ok)
            count = 1

        if count ==0:
            self.idt.insert_item(item_id,item_pass,item_mode,item_name,item_email)
            self.load_user()

    def edit_user(self):
        id = self.ui.le_user_id.text()
        mode = self.ui.com_grant.currentText()
        name = self.ui.le_name.text()
        email = self.ui.le_email.text()

        if mode == '--select--':
            QMessageBox.information(self, '사용자 관리', '유저 권한을 설정해 주세요.', QMessageBox.Ok)
        else:
            item_id, item_name ,item_mode, item_email = self.user_create_item(id,name,mode,email)

            selectionIdxs = self.ui.table_user.selectedIndexes()[0]

            self.ui.table_user.setItem(selectionIdxs.row(), 0, item_id)
            self.ui.table_user.setItem(selectionIdxs.row(), 1, item_name)
            self.ui.table_user.setItem(selectionIdxs.row(), 2, item_mode)
            self.ui.table_user.setItem(selectionIdxs.row(), 3, item_email)

            self.ui.btn_del_user.setEnabled(True)
            self.ui.btn_init.setEnabled(True)
            self.ui.btn_insert_user.setEnabled(True)
            self.ui.btn_edit_user.setEnabled(False)
            self.ui.le_pass.setEnabled(True)
            self.clear()

            self.idt.update_item(id,mode,name,email)
            QMessageBox.information(self, '사용자 관리', '확인', QMessageBox.Ok)

    def clear(self):
        self.ui.le_user_id.clear()
        self.ui.le_name.clear()
        self.ui.le_email.clear()
        self.ui.le_pass.clear()

    def update(self):
        selectionIdxs = self.ui.table_user.selectedIndexes()[0]
        returnIdxs1 = self.ui.table_user.item(selectionIdxs.row(), 0).text()
        returnIdxs2 = self.ui.table_user.item(selectionIdxs.row(), 1).text()
        returnIdxs3 = self.ui.table_user.item(selectionIdxs.row(), 2).text()
        returnIdxs4 = self.ui.table_user.item(selectionIdxs.row(), 3).text()

        self.ui.le_user_id.setText(returnIdxs1)
        self.ui.le_name.setText(returnIdxs2)
        self.ui.le_email.setText(returnIdxs4)

        self.ui.btn_edit_user.setEnabled(True)
        self.ui.btn_del_user.setEnabled(False)
        self.ui.btn_init.setEnabled(False)
        self.ui.btn_insert_user.setEnabled(False)
        self.ui.le_pass.setEnabled(False)

    def set_context_menu(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction('수정', tv)
        tv.addAction(update_action)
        update_action.triggered.connect(self.update)
