from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QAction

from dao.category_dao import CateDao
from data.table import create_table


class Category(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui/category.ui')
        self.cdt = CateDao()
        
        self.ui.table_category.setColumnCount(2)
        self.table_category = create_table(table=self.ui.table_category, data=['no','종류'])

        self.load_category()
        self.set_context_menu(self.ui.table_category)
        self.ui.btn_ins_category.clicked.connect(self.ins_cate)
        self.ui.btn_del_category.clicked.connect(self.del_cate)
        self.ui.btn_edit_category.clicked.connect(self.edit_cate)

        self.ui.btn_edit_category.setEnabled(False)
        self.ui.btn_edit_category.setText('편집시 우클릭')

        self.ui.show()

    def ins_cate(self):
        name = self.ui.le_category.text()
        no = int(self.ui.le_no.text())
        check_no = [(no,)]
        check_name = [(name,)]


        if no == '':
            QMessageBox.information(self, '제품 관리', '번호를 입력해주세요.', QMessageBox.Ok)
        elif check_no == self.cdt.select_item_no(no):
            QMessageBox.information(self, '제품 관리', '번호가 중복입니다.', QMessageBox.Ok)
        else:
            if name == '':
                QMessageBox.information(self, '제품 관리', '이름을 입력해주세요.', QMessageBox.Ok)
            elif check_name == self.cdt.select_item_name(name):
                QMessageBox.information(self, '제품 관리', '이름이 중복입니다.', QMessageBox.Ok)
            else:
                self.cdt.insert_item(no, name)
                self.load_category()

    def del_cate(self):
        selectionIdxs = self.ui.table_category.selectedIndexes()[0]
        name = self.ui.table_category.item(selectionIdxs.row(), 1).text()
        self.cdt.delete_item(name)
        self.load_category()

    def edit_cate(self):
        self.ui.btn_edit_category.setEnabled(False)
        self.ui.btn_edit_category.setText('편집시 우클릭')

        name = self.ui.le_category.text()
        no = self.ui.le_no.text()

        self.cdt.update_item(name, no)

        self.ui.btn_del_category.setEnabled(True)
        self.ui.btn_ins_category.setEnabled(True)
        self.ui.le_no.setEnabled(True)
        self.load_category()
    
    def load_category(self):
        self.ui.table_category.setRowCount(0)
        res = self.cdt.select_item()
        for (no, name) in res:
            item_no, item_name= self.pro_create_item(no, name)
            nextIdx = self.ui.table_category.rowCount()
            self.ui.table_category.insertRow(nextIdx)
            self.ui.table_category.setItem(nextIdx, 0, item_no)
            self.ui.table_category.setItem(nextIdx, 1, item_name)

    def pro_create_item(self, no, name):
        item_no = QTableWidgetItem()
        item_no.setTextAlignment(Qt.AlignCenter)
        item_no.setData(Qt.DisplayRole, no)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        return item_no, item_name

    def set_context_menu(self,tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction('수정', tv)
        tv.addAction(update_action)
        update_action.triggered.connect(self.update)

    def update(self):
        self.ui.btn_edit_category.setEnabled(True)
        self.ui.btn_edit_category.setText('edit')

        selectionIdxs = self.ui.table_category.selectedIndexes()[0]
        returnIdxs1 = self.ui.table_category.item(selectionIdxs.row(), 0).text()
        returnIdxs2 = self.ui.table_category.item(selectionIdxs.row(), 1).text()

        self.ui.le_no.setText(returnIdxs1)
        self.ui.le_category.setText(returnIdxs2)

        self.ui.le_no.setEnabled(False)
        self.ui.btn_del_category.setEnabled(False)
        self.ui.btn_ins_category.setEnabled(False)