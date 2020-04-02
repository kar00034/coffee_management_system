import os
import subprocess

from PyQt5.QtWidgets import QApplication
import time

from dao.product_dao import ProductDao
from dao.select_dao import SelDao
from ui_control.Category import Category
from ui_control.User_registration import Sign_up
from ui_control.login_ui import Login
from ui_control.main_menu import Main
from ui_control.manager import management_system
from ui_control.sale_manage import SaleMenu

if __name__ == '__main__':
    app = QApplication([])
    # w = Login()
    m = Main() # 그래프
    # ma = management_system() # 권한추가
    # s = SaleMenu()
    app.exec_()

"""
select p.name, if(count(select salecnt from sale where DATE_FORMAT(date,'%Y %m') = '2020 02')=0,0,salecnt) from product p left join sale s on p.code = s.code GROUP by p.name;
select name from product p join sale s on p.code=s.code where p.name = '팥빙수' and DATE_FORMAT(date,'%Y %m') = '2020 02' GROUP by name;
select if(count(select salecnt from sale where DATE_FORMAT(date,'%Y %m') = '2020 02')=0,0,salecnt) from product p left join sale s on p.code = s.code GROUP by p.name;
select salecnt from sale where DATE_FORMAT(date,'%Y %m') = '2020 02';

lib = qt, pyqt5
"""