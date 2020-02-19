from PyQt5 import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem


def create_table(table=None, data=None):
    table.setHorizontalHeaderLabels(data)
    # row단위선택
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 수정불가
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 균일 간격 재배치
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    return table

