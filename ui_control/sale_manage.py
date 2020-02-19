from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QAction
from mysql.connector import Error

from dao.category_dao import CateDao
from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao
from dao.select_dao import SelDao
from data.table import create_table
from ui_control.Category import Category


class SaleMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/sale_manage.ui")
        self.pdt = ProductDao()
        self.sdt = SaleDao()
        self.ui.table_sale.setColumnCount(5)
        self.ui.table_order.setColumnCount(3)
        self.table_order = create_table(table=self.ui.table_order, data=['제품명', '종류', '갯수'])
        self.table_sale = create_table(table=self.ui.table_sale, data=['제품코드', '제품명','종류', '제품가격', '마진율(%)'])
        self.ui.combo_menu.addItem('all')
        self.ui.combo_sel_pro.addItem('--select--')
        self.count = 0
        self.nextIdx = 0
        self.namelist = []
        self.order_list = {}

        for i in range(len(self.pdt.select_category())):
            self.ui.combo_menu.addItems(self.pdt.select_category()[i])

        self.ui.combo_category.addItem('all')
        for i in range(len(self.pdt.select_category())):
            self.ui.combo_category.addItems(self.pdt.select_category()[i])
        for i in range(len(self.pdt.select_name())):
            self.ui.combo_sel_pro.addItems(self.pdt.select_name()[i])

        self.ui.btn_insert_menu.clicked.connect(self.ins_menu)
        self.ui.btn_del_menu.clicked.connect(self.del_menu)
        self.ui.btn_edit_menu.clicked.connect(self.edit_menu)
        self.ui.btn_ins_category.clicked.connect(self.category)
        self.ui.combo_menu.currentIndexChanged.connect(self.select_menu)
        self.ui.btn_exit.clicked.connect(self.exit)

        self.load_pro_all()

        # sale_manage
        self.ui.tab_product.currentChanged.connect(self.tab_change)
        self.ui.btn_insert.clicked.connect(self.ins_order)
        self.ui.combo_category.currentIndexChanged.connect(self.order_category)
        self.ui.btn_edit.clicked.connect(self.edit_order)
        self.ui.btn_delete.clicked.connect(self.del_order)
        self.ui.btn_reset.clicked.connect(self.reset_order)
        self.ui.btn_ok.clicked.connect(self.ok_order)

        # select
        self.ui.btn_select.clicked.connect(self.select_sale_detail)
        self.ui.btn_init.clicked.connect(self.select_init)

        self.set_context_menu(self.ui.table_sale)
        self.set_context_menu_order(self.ui.table_order)

        self.ui.btn_edit_menu.setEnabled(False)
        self.ui.btn_edit.setEnabled(False)
        self.ui.btn_edit_menu.setText('편집시 우클릭')
        self.ui.btn_edit.setText('편집시 우클릭')

        self.ui.show()

    #product manage
    def ins_menu(self):
        item_mode = self.ui.combo_menu.currentText()

        count = 0
        if item_mode == 'all':
            QMessageBox.information(self, '제품 관리', '제품의 종류를 설정해 주세요.', QMessageBox.Ok)
            count = 1
        else:
            item_code = self.ui.le_pro_code.text().upper()
            item_name = self.ui.le_pro_name.text()
            item_price = self.ui.le_pro_price.text()
            item_margin = self.ui.le_pro_margin.text()
            check_name = [(item_name.upper(),)]
            check_code = [(item_code,)]

        if count == 0:
            if item_code == '':
                QMessageBox.information(self, '제품 관리', '코드를 입력해주세요.', QMessageBox.Ok)
                count = 1
            else:
                if item_name == '':
                    QMessageBox.information(self, '제품 관리', '제품명을 입력해주세요.', QMessageBox.Ok)
                    count = 1

                elif check_code == self.pdt.select_check_menu_code(item_code):
                    QMessageBox.information(self, '제품 관리', '코드가 이미 있습니다.', QMessageBox.Ok)
                    count = 1

                else:
                    if  check_name == self.pdt.select_check_menu_name(item_name):
                        QMessageBox.information(self, '제품 관리', '해당 메뉴가 이미 있습니다.', QMessageBox.Ok)
                        count = 1

                    elif item_price == '':
                        QMessageBox.information(self, '제품 관리', '가격을 입력해주세요.', QMessageBox.Ok)
                        count = 1
                    else:
                        if item_margin == '':
                            QMessageBox.information(self, '제품 관리', '마진율을 입력해주세요.', QMessageBox.Ok)
                            count = 1

        if count == 0:
            self.pdt.insert_item(item_code, item_name, item_mode, item_price, item_margin)
            self.load_pro_all()

    def del_menu(self):
        selectionIdxs = self.ui.table_sale.selectedIndexes()[0]
        item_code = self.ui.table_sale.item(selectionIdxs.row(), 0).text().upper()
        category = self.ui.combo_menu.currentText()
        self.pdt.delete_item(item_code)
        if category == 'all':
            self.load_pro_all()
        else:
            res = list(self.pdt.select_menu(self.ui.combo_menu.currentText()))
            self.load_pro(res)

    def edit_menu(self):
        code = self.ui.le_pro_code.text()
        category = self.ui.combo_menu.currentText()
        name = self.ui.le_pro_name.text()
        price = self.ui.le_pro_price.text()
        margin = self.ui.le_pro_margin.text()

        if category == 'all':
            QMessageBox.information(self, '제품 관리', '제품의 종류 설정해 주세요.', QMessageBox.Ok)
        else:
            item_code, item_name, item_price, item_margin = self.pro_create_item(code, name, price, margin)

            # selectionIdxs = self.ui.table_sale.selectedIndexes()[0]
            countIdxs = self.ui.table_sale.rowCount()

            self.ui.table_sale.setItem(countIdxs, 0, item_code)
            self.ui.table_sale.setItem(countIdxs, 1, item_name)
            self.ui.table_sale.setItem(countIdxs, 3, item_price)
            self.ui.table_sale.setItem(countIdxs, 4, item_margin)

            self.pdt.update_item(name, price, margin, category, code)
            QMessageBox.information(self, '사용자 관리', '확인', QMessageBox.Ok)

            self.ui.btn_del_menu.setEnabled(True)
            self.ui.btn_insert_menu.setEnabled(True)
            self.ui.btn_edit_menu.setEnabled(False)
            self.ui.btn_edit_menu.setText('편집시 우클릭')
            self.ui.le_pro_code.setEnabled(True)
            self.ui.btn_insert.setEnabled(False)
            self.ui.btn_ins_category.setEnabled(True)
            self.ui.btn_ins_category.clicked.connect(self.category)

            self.ui.le_pro_price.clear()
            self.ui.le_pro_code.clear()
            self.ui.le_pro_margin.clear()
            self.ui.le_pro_name.clear()
            if category == 'all':
                self.load_pro_all()
            else:
                res = list(self.pdt.select_menu(self.ui.combo_menu.currentText()))
                self.load_pro(res)

    def load_pro(self,res):
        # res = self.pdt.select_menu2()
        self.ui.table_sale.setRowCount(0)
        for (code, name, category, price, marginrate) in res:
            item_code, item_name, item_category, item_price, item_marginrate = self.pro_create_item(code, name, category, price, marginrate, )
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_code)
            self.ui.table_sale.setItem(nextIdx, 1, item_name)
            self.ui.table_sale.setItem(nextIdx, 2, item_category)
            self.ui.table_sale.setItem(nextIdx, 3, item_price)
            self.ui.table_sale.setItem(nextIdx, 4, item_marginrate)

    def pro_create_item(self, code, name, price, marginrate, category):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_category = QTableWidgetItem()
        item_category.setTextAlignment(Qt.AlignCenter)
        item_category.setData(Qt.DisplayRole, category)

        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignRight)
        if price != None:
            item_price.setData(Qt.DisplayRole, format(int(price), ',d'))
        else:
            item_price.setData(Qt.DisplayRole, '-')

        item_marginrate = QTableWidgetItem()
        item_marginrate.setTextAlignment(Qt.AlignRight)
        if marginrate != None:
            item_marginrate.setData(Qt.DisplayRole, (marginrate))
        else:
            item_marginrate.setData(Qt.DisplayRole, '-')

        return item_code, item_name, item_category, item_price, item_marginrate

    def select_menu(self):
        if self.ui.combo_menu.currentText() == 'all':
            self.load_pro_all()
        else:
            res = list(self.pdt.select_menu(self.ui.combo_menu.currentText()))
            self.load_pro(res)

    def load_pro_all(self):
        self.ui.table_sale.setRowCount(0)
        res = self.pdt.select_menu2()
        for (code, name, category, price, marginrate) in res:
            item_code, item_name, item_category, item_price, item_marginrate = self.pro_create_item(code, name, category, price, marginrate)
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_code)
            self.ui.table_sale.setItem(nextIdx, 1, item_name)
            self.ui.table_sale.setItem(nextIdx, 2, item_category)
            self.ui.table_sale.setItem(nextIdx, 3, item_price)
            self.ui.table_sale.setItem(nextIdx, 4, item_marginrate)

    def set_context_menu(self,tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction('수정', tv)
        tv.addAction(update_action)
        update_action.triggered.connect(self.update)

    def update(self):
        selectionIdxs = self.ui.table_sale.selectedIndexes()[0]
        if self.ui.tab_product.currentIndex() == 0:
            QMessageBox.information(self, '제품 관리', '제품의 종류 설정해 주세요.', QMessageBox.Ok)
            returnIdxs1 = self.ui.table_sale.item(selectionIdxs.row(), 0).text()
            returnIdxs2 = self.ui.table_sale.item(selectionIdxs.row(), 1).text()
            if self.ui.table_sale.item(selectionIdxs.row(), 3).text().count(',') >= 1:
                returnIdxs3 = self.ui.table_sale.item(selectionIdxs.row(), 3).text().split(',')[0] + self.ui.table_sale.item(selectionIdxs.row(), 3).text().split(',')[1]
            else:
                returnIdxs3 = self.ui.table_sale.item(selectionIdxs.row(), 3).text()
            returnIdxs4 = self.ui.table_sale.item(selectionIdxs.row(), 3).text()

            self.ui.le_pro_code.setText(returnIdxs1)
            self.ui.le_pro_name.setText(returnIdxs2)
            self.ui.le_pro_price.setText(returnIdxs3)
            self.ui.le_pro_margin.setText(returnIdxs4)

            self.ui.btn_insert.setEnabled(False)
            self.ui.btn_del_menu.setEnabled(False)
            self.ui.btn_insert_menu.setEnabled(False)
            self.ui.btn_edit_menu.setEnabled(True)
            self.ui.btn_edit_menu.setText('편집')
            self.ui.le_pro_code.setEnabled(False)
            self.ui.btn_ins_category.setEnabled(False)

        # if self.ui.tab_product.currentIndex() == 1:
        #     returnIdxs = self.ui.table_sale.item(selectionIdxs.row(), 2).text()
        #
        #     self.ui.le_salecnt.setText(returnIdxs)
        #
        #     self.ui.btn_ok.setEnabled(False)
        #     self.ui.btn_reset.setEnabled(False)
        #     self.ui.btn_delete.setEnabled(False)
        #     self.ui.btn_exit.setEnabled(False)
        #     self.ui.btn_edit.setEnabled(True)

    def category(self):
        self.ca = Category()
        # self.ca.ui.btn_out.clicked.connect(self.select_menu)

        self.ca.ui.btn_ins_category.clicked.connect(self.init_category)
        self.ca.ui.btn_del_category.clicked.connect(self.init_category2)
        self.ca.ui.btn_edit_category.clicked.connect(self.init_category)

    def init_category(self):
        cdt = CateDao()
        for i in range(len(cdt.select_item()) + 1):
            self.ui.combo_menu.removeItem(0)
        self.ui.combo_menu.addItem('all')
        for i in range(len(cdt.select_item())):
            self.ui.combo_menu.addItems(self.pdt.select_category()[i])

        self.load_pro_all()

    def init_category2(self):
        cdt = CateDao()
        for i in range(len(cdt.select_item()) + 2):
            self.ui.combo_menu.removeItem(0)
        self.ui.combo_menu.addItem('all')
        for i in range(len(cdt.select_item())):
            self.ui.combo_menu.addItems(self.pdt.select_category()[i])

        self.load_pro_all()

    def load_order(self):
        if self.ui.tab_product.currentIndex() == 0:
            self.ui.table_sale.setColumnCount(5)
            self.table_sale = create_table(table=self.ui.table_sale, data=['제품코드', '제품명', '종류', '제품가격', '마진율(%)'])
            self.load_pro_all()
            self.ui.table_order.hide()
            self.ui.lb_order.hide()
        elif self.ui.tab_product.currentIndex() == 1:
            self.ui.table_sale.setColumnCount(7)
            self.table_sale_detail = create_table(table=self.ui.table_sale, data=['제품명', '종류', '판매량', '판매액', '세금', '마진액', '판매 시간'])
            self.ui.table_order.setColumnCount(3)
            self.table_sale_order = create_table(table=self.ui.table_order,data=['제품명', '종류', '갯수'])
            self.ui.table_order.show()
            self.ui.lb_order.show()
            self.load_sale()

        elif self.ui.tab_product.currentIndex() == 2:
            self.ui.table_sale.setColumnCount(4)
            self.table_select = create_table(table=self.ui.table_sale, data=['제품명', '판매량', '판매가', '판매시간'])
            self.ui.table_order.hide()
            self.ui.lb_order.hide()
            self.load_select()

    def order_category(self):
        self.init_combo_pro_name()
        category = self.ui.combo_category.currentText()
        res = list(self.pdt.select_order_name(category))
        for i in range(len(self.pdt.select_order_name(category))):
            self.ui.combo_pro_name.addItems(res[i])
            self.count += 1

    def ins_order(self):
        name = self.ui.combo_pro_name.currentText()
        category = self.pdt.select_order_name_category(name)
        category = str(category).strip(("[('")).strip("',)]")
        cnt = self.ui.le_salecnt.text()
        # if name in self.order_list.keys:
        if name in self.order_list.keys():
            self.order_list[name] = int(self.order_list[name])+int(cnt)
        else:
            self.order_list[name] = int(cnt)
            self.namelist.append(name)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_category = QTableWidgetItem()
        item_category.setTextAlignment(Qt.AlignCenter)
        item_category.setData(Qt.DisplayRole, category)

        item_cnt = QTableWidgetItem()
        item_cnt.setTextAlignment(Qt.AlignRight)
        item_cnt.setData(Qt.DisplayRole, cnt)

        self.ui.table_order.insertRow(self.nextIdx)
        self.ui.table_order.setItem(self.nextIdx, 0, item_name)
        self.ui.table_order.setItem(self.nextIdx, 1, item_category)
        self.ui.table_order.setItem(self.nextIdx, 2, item_cnt)

        self.nextIdx += 1
        self.ui.le_salecnt.clear()

    def init_combo_pro_name(self):
        for i in range(self.count):
            self.ui.combo_pro_name.removeItem(0)
        self.count = 0

    def tab_change(self):
        self.init_combo_pro_name()
        for i in range(len(self.pdt.select_category())+1):
            self.ui.combo_category.removeItem(0)
        self.ui.combo_category.addItem('--select--')
        for i in range(len(self.pdt.select_category())):
            self.ui.combo_category.addItems(self.pdt.select_category()[i])
            self.count += 1
        self.load_order()

    def edit_order(self):
        try:
            self.ui.btn_edit.setText('편집시 우클릭')
            self.ui.btn_ok.setEnabled(True)
            self.ui.btn_reset.setEnabled(True)
            self.ui.btn_delete.setEnabled(True)
            self.ui.btn_exit.setEnabled(True)
            self.ui.btn_insert.setEnabled(True)

            self.ui.btn_edit.setEnabled(False)

            selectionIdxs = self.ui.table_order.selectedIndexes()[0]
            # self.ui.tab_sale.currentIndex()
            cnt = self.ui.le_salecnt.text()

            item_cnt = QTableWidgetItem()
            item_cnt.setTextAlignment(Qt.AlignCenter)
            item_cnt.setData(Qt.DisplayRole, int(cnt))

            self.ui.table_order.setItem(selectionIdxs.row(), 2, item_cnt)
        except Error as err:
            print(err)

    def del_order(self):
        selectionIdxs = self.ui.table_order.selectedIndexes()[0]
        self.ui.table_order.removeRow(selectionIdxs.row())

    def reset_order(self):
        for i in range(self.nextIdx):
            self.ui.table_order.removeRow(0)
        self.nextIdx = 0

    def load_sale(self):
        self.ui.table_sale.setRowCount(0)
        res = self.sdt.select_sale_table()
        for (name, category, cnt, sale_price, tax, margin_price, time) in res:
            item_name, item_category, item_cnt, item_sale_price, item_tax, item_margin_price, item_time = self.sale_create_item(name, category, cnt, sale_price, tax, margin_price, time)
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_name)
            self.ui.table_sale.setItem(nextIdx, 1, item_category)
            self.ui.table_sale.setItem(nextIdx, 2, item_cnt)
            self.ui.table_sale.setItem(nextIdx, 3, item_sale_price)
            self.ui.table_sale.setItem(nextIdx, 4, item_tax)
            self.ui.table_sale.setItem(nextIdx, 5, item_margin_price)
            self.ui.table_sale.setItem(nextIdx, 6, item_time)

    def sale_create_item(self, name, category, cnt, sale_price, tax, margin_price, time):
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_category = QTableWidgetItem()
        item_category.setTextAlignment(Qt.AlignCenter)
        item_category.setData(Qt.DisplayRole, category)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_cnt = QTableWidgetItem()
        item_cnt.setTextAlignment(Qt.AlignRight)
        if cnt != None:
            item_cnt.setData(Qt.DisplayRole, format(int(cnt), ',d'))
        else:
            item_cnt.setData(Qt.DisplayRole, '-')

        item_sale_price = QTableWidgetItem()
        item_sale_price.setTextAlignment(Qt.AlignRight)
        item_sale_price.setData(Qt.DisplayRole, format(int(sale_price), ',d'))

        item_tax = QTableWidgetItem()
        item_tax.setTextAlignment(Qt.AlignRight)
        item_tax.setData(Qt.DisplayRole, format(int(tax), ',d'))

        item_margin_price = QTableWidgetItem()
        item_margin_price.setTextAlignment(Qt.AlignRight)
        item_margin_price.setData(Qt.DisplayRole, format(int(margin_price),',d'))

        item_time = QTableWidgetItem()
        item_time.setTextAlignment(Qt.AlignCenter)
        item_time.setData(Qt.DisplayRole, time)

        return item_name, item_category, item_cnt, item_sale_price, item_tax, item_margin_price, item_time

    def set_context_menu_order(self,tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction('수정', tv)
        tv.addAction(update_action)
        update_action.triggered.connect(self.update_order)

    def update_order(self,tv):
        selectionIdxs = self.ui.table_order.selectedIndexes()[0]

        returnIdxs = self.ui.table_order.item(selectionIdxs.row(), 2).text()
        self.ui.le_salecnt.setText(returnIdxs)

        self.ui.btn_ok.setEnabled(False)
        self.ui.btn_reset.setEnabled(False)
        self.ui.btn_insert.setEnabled(False)
        self.ui.btn_delete.setEnabled(False)
        self.ui.btn_exit.setEnabled(False)

        self.ui.btn_edit.setText('편집')
        self.ui.btn_edit.setEnabled(True)

    def ok_order(self):
        self.ui.table_order.setRowCount(0)
        for i in range(len(self.namelist)):
            self.sdt.insert_item(self.namelist[i], self.order_list[self.namelist[i]])

        self.ui.le_salecnt.clear()
        self.nextIdx = 0
        self.load_sale()

    # tab index = 3
    def load_select(self):
        self.ui.table_sale.setRowCount(0)
        seldt = SelDao()
        res = seldt.select_item_where()
        for (name, cnt, sale_price, date) in res:
            item_name, item_cnt, item_sale_price, item_date = self.select_create_item(name, cnt, sale_price, date)
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_name)
            self.ui.table_sale.setItem(nextIdx, 1, item_cnt)
            self.ui.table_sale.setItem(nextIdx, 2, item_sale_price)
            self.ui.table_sale.setItem(nextIdx, 3, item_date)

    def select_create_item(self, name, cnt, sale_price, date):
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_cnt = QTableWidgetItem()
        item_cnt.setTextAlignment(Qt.AlignCenter)
        item_cnt.setData(Qt.DisplayRole, format(int(cnt), 'd'))

        item_sale_price = QTableWidgetItem()
        item_sale_price.setTextAlignment(Qt.AlignRight)
        item_sale_price.setData(Qt.DisplayRole, format(int(sale_price), ',d'))

        item_date = QTableWidgetItem()
        item_date.setTextAlignment(Qt.AlignRight)
        item_date.setData(Qt.DisplayRole, date)

        return item_name, item_cnt, item_sale_price, item_date

    def select_sale_detail(self):
        name = self.ui.combo_sel_pro.currentText()
        seldt = SelDao()
        if name == '--select--':
            name = ''
        min_price = self.ui.le_min_price.text()
        max_price = self.ui.le_max_price.text()
        min_date = self.ui.le_min_date_y.text() +'-'+ self.ui.le_min_date_m.text() +'-'+ self.ui.le_min_date_d.text()
        max_date = self.ui.le_max_date_y.text() +'-'+ self.ui.le_max_date_m.text() +'-'+ self.ui.le_max_date_d.text()
        if min_date == '--':
            min_date = ''
        if max_date == '--':
            max_date = ''

        self.ui.table_sale.setRowCount(0)

        res = seldt.select_item_where(name,min_price,max_price,min_date,max_date)

        for (name, cnt, sale_price, date) in res:
            item_name, item_cnt, item_sale_price, item_date = self.select_create_item(name, cnt, sale_price, date)
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_name)
            self.ui.table_sale.setItem(nextIdx, 1, item_cnt)
            self.ui.table_sale.setItem(nextIdx, 2, item_sale_price)
            self.ui.table_sale.setItem(nextIdx, 3, item_date)

    def select_init(self):
        self.load_select()
        self.ui.le_min_price.setText('0')
        self.ui.le_max_price.clear()
        self.ui.le_min_date_d.clear()
        self.ui.le_min_date_m.clear()
        self.ui.le_min_date_y.clear()
        self.ui.le_max_date_d.clear()
        self.ui.le_max_date_m.clear()
        self.ui.le_max_date_y.clear()

    def exit(self):
        self.ui.close()