import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from dao.id_dao import IDDao
from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao
from data.table import create_table
from ui_control.manager import management_system
from ui_control.sale_manage import SaleMenu
from ui_control.user_setting import Setting


class Main(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pdt = ProductDao()
        self.idt = IDDao()
        self.sdt = SaleDao()
        self.ui = uic.loadUi("ui/main_menu.ui", self)

        self.month_count = 14
        self.graphcount = 0

        # combobox
        self.combobox_setting()

        # graph
        self.graph()

        # table
        self.table_pro = create_table(table=self.ui.table_pro, data=['제품코드', '제품명', '종류', '제품가격', '마진율(%)'])
        self.sale_pro = create_table(table=self.ui.table_sale, data=['제품명', '판매량', '판매금액', '판매일'])

        self.load_pro_all()
        self.load_sale_all()

        self.ui.btn_out.clicked.connect(self.exit)  # logout
        self.ui.btn_manage.clicked.connect(self.manage)
        self.ui.btn_sale.clicked.connect(self.sale_manage)
        self.ui.btn_exit.clicked.connect(self.exit)
        self.ui.btn_set.clicked.connect(self.user_setting)
        self.ui.combo_menu.currentIndexChanged.connect(self.select_menu)
        self.ui.combo_sale_year.currentIndexChanged.connect(self.select_sale)
        self.ui.combo_sale_month.currentIndexChanged.connect(self.select_month)
        self.ui.show()

    # button ui
    def manage(self):
        self.ms = management_system()
        self.ms.ui.lbl_ID.setText(self.ui.lbl_ID.text())
        self.ms.ui.lbl_mode.setText(list(self.idt.select_item(self.ui.lbl_ID.text()))[0][1])
        self.ms.check_grant()

    def sale_manage(self):
        self.sale = SaleMenu()
        grant = []
        for i in range(len(IDDao().select_grant('admin'))):
            a = IDDao().select_grant(self.ui.lbl_mode.text()).count(IDDao().select_grant('admin')[i])
            grant.append(a)
        if grant[2] == 0:
            self.sale.ui.tab_product.removeTab(0)

    def logout(self):
        self.ui.close()

    def exit(self):
        self.ui.close()

    def combobox_setting(self):
        self.ui.combo_menu.addItem('all')
        self.ui.combo_sale_year.addItem('all')
        self.ui.combo_sale_month.addItem('년도를 선택해주세요')

        for i in range(len(self.pdt.select_category())):
            self.ui.combo_menu.addItems(self.pdt.select_category()[i])
        for i in range(len(self.sdt.select_item(True))):
            self.ui.combo_sale_year.addItems(tuple(self.sdt.select_item(True)[i]))

    # product table
    def select_menu(self):
        if self.ui.combo_menu.currentText() == 'all':
            self.load_pro_all()
        else:
            res = list(self.pdt.select_menu(self.ui.combo_menu.currentText()))
            self.load_pro(res)

    def load_pro(self, res):
        self.ui.table_pro.setRowCount(0)
        for (code, name, price, marginrate, category) in res:
            item_code, item_name, item_price, item_marginrate, item_category = self.pro_create_item(code, name, price,
                                                                                                    marginrate,
                                                                                                    category)
            nextIdx = self.ui.table_pro.rowCount()
            self.ui.table_pro.insertRow(nextIdx)
            self.ui.table_pro.setItem(nextIdx, 0, item_code)
            self.ui.table_pro.setItem(nextIdx, 1, item_name)
            self.ui.table_pro.setItem(nextIdx, 2, item_category)
            self.ui.table_pro.setItem(nextIdx, 3, item_price)
            self.ui.table_pro.setItem(nextIdx, 4, item_marginrate)

    def pro_create_item(self, code, name, price, marginrate, category):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

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

        item_category = QTableWidgetItem()
        item_category.setTextAlignment(Qt.AlignCenter)
        item_category.setData(Qt.DisplayRole, category)

        return item_code, item_name, item_price, item_marginrate, item_category

    def load_pro_all(self):
        self.ui.table_pro.setRowCount(0)
        res = self.pdt.select_menu2()
        for (code, name, price, marginrate, category) in res:
            item_code, item_name, item_price, item_marginrate, item_category = self.pro_create_item(code, name, price,
                                                                                                    marginrate,
                                                                                                    category)
            nextIdx = self.ui.table_pro.rowCount()
            self.ui.table_pro.insertRow(nextIdx)
            self.ui.table_pro.setItem(nextIdx, 0, item_code)
            self.ui.table_pro.setItem(nextIdx, 1, item_name)
            self.ui.table_pro.setItem(nextIdx, 2, item_category)
            self.ui.table_pro.setItem(nextIdx, 3, item_price)
            self.ui.table_pro.setItem(nextIdx, 4, item_marginrate)

    # sale_table
    def sale_create_item(self, name, salecnt, sale_price, date):
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_salecnt = QTableWidgetItem()
        item_salecnt.setTextAlignment(Qt.AlignCenter)
        item_salecnt.setData(Qt.DisplayRole, salecnt)

        item_sale_price = QTableWidgetItem()
        item_sale_price.setTextAlignment(Qt.AlignRight)
        item_sale_price.setData(Qt.DisplayRole, format(int(sale_price), ',d'))

        item_date = QTableWidgetItem()
        item_date.setTextAlignment(Qt.AlignCenter)
        item_date.setData(Qt.DisplayRole, date)

        return item_name, item_salecnt, item_sale_price, item_date

    def load_sale_all(self):
        self.ui.table_sale.setRowCount(0)
        res = self.sdt.select_item()
        for (name, salecnt, sale_price, date) in res:
            item_name, item_salecnt, item_sale_price, item_date = self.sale_create_item(name, salecnt, sale_price, date)
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_name)
            self.ui.table_sale.setItem(nextIdx, 1, item_salecnt)
            self.ui.table_sale.setItem(nextIdx, 2, item_sale_price)
            self.ui.table_sale.setItem(nextIdx, 3, item_date)

    def select_sale(self):
        if self.ui.combo_sale_year.currentText() == 'all':
            for i in range(0, self.month_count):
                self.ui.combo_sale_month.removeItem(0)
            self.ui.combo_sale_month.addItem('년도를 선택해주세요')
            self.load_sale_all()
        else:
            res = list(self.sdt.select_date(self.ui.combo_sale_year.currentText()))

            for i in range(0, self.month_count):
                self.ui.combo_sale_month.removeItem(0)
            self.ui.combo_sale_month.addItem('all')
            self.load_sale(res)
            for i in range(len(self.sdt.select_date(self.ui.combo_sale_year.currentText(), 2))):
                self.ui.combo_sale_month.addItems(self.sdt.select_date(self.ui.combo_sale_year.currentText(), 2)[i])

    def load_sale(self, res):
        self.ui.table_sale.setRowCount(0)

        for (name, salecnt, sale_price, date) in res:
            item_name, item_salecnt, item_sale_price, item_date = self.sale_create_item(name, salecnt, sale_price, date)
            nextIdx = self.ui.table_sale.rowCount()
            self.ui.table_sale.insertRow(nextIdx)
            self.ui.table_sale.setItem(nextIdx, 0, item_name)
            self.ui.table_sale.setItem(nextIdx, 1, item_salecnt)
            self.ui.table_sale.setItem(nextIdx, 2, item_sale_price)
            self.ui.table_sale.setItem(nextIdx, 3, item_date)

    def select_month(self, res):
        if self.ui.combo_sale_month.currentText() is None or self.ui.combo_sale_month.currentText() == 'all':
            self.load_sale(self.sdt.select_date(self.ui.combo_sale_year.currentText()))
        else:
            date = self.sdt.select_date(
                self.ui.combo_sale_year.currentText() + ' ' + self.ui.combo_sale_month.currentText(), 3)
            self.load_sale(date)

    # 계정관리
    def user_setting(self):
        self.set = Setting()
        self.set.ui.lbl_id.setText(self.ui.lbl_ID.text())
        self.set.ui.lbl_name.setText(self.idt.select_item_id(self.ui.lbl_ID.text())[0][0])
        self.set.ui.lbl_mode.setText(self.idt.select_item_id(self.ui.lbl_ID.text())[0][1])

    # graph
    def graph(self):
        # 글꼴
        mpl.rcParams['font.family'] = 'NanumGothic'
        mpl.rcParams['axes.unicode_minus'] = False
        # data
        name, price = self.sdt.select_graph_product()
        fig, ax1 = plt.subplots()

        # plot
        self.plotWidget = FigureCanvas(fig)


        ax1.set_title("커피 판매량")
        self.lay = QtWidgets.QVBoxLayout(self.ui.content_plot)
        self.lay.addWidget(self.plotWidget)

        ax1.pie(price, labels=name, autopct=lambda pct: self.func(pct, price), shadow=False,
                     startangle=90, radius=1.0)

    def func(self, pct, data):
        absolute = round(int(pct * float(math.ceil(np.sum(data)))) / 100)
        return "{:.1f}%\n({:,d})".format(pct, absolute)