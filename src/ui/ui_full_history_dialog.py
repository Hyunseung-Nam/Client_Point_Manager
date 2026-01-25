# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
)


class Ui_FullHistoryDialog(object):
    def setupUi(self, Dialog: QDialog):
        if not Dialog.objectName():
            Dialog.setObjectName("dlgFullHistory")
        Dialog.resize(720, 420)
        Dialog.setStyleSheet(
            "QWidget {"
            "  font-family: 'Noto Sans KR';"
            "  font-size: 13px;"
            "  color: #1D1D1F;"
            "  background-color: #F5F5F7;"
            "}"
            "QTableWidget {"
            "  background: #FFFFFF;"
            "  border: 1px solid #E5E5EA;"
            "  border-radius: 12px;"
            "  gridline-color: #E5E5EA;"
            "}"
            "QHeaderView::section {"
            "  background: #F5F5F7;"
            "  color: #1D1D1F;"
            "  border: none;"
            "  padding: 6px;"
            "  font-weight: 600;"
            "}"
            "QPushButton {"
            "  background: #0071E3;"
            "  color: #FFFFFF;"
            "  border: none;"
            "  border-radius: 8px;"
            "  padding: 8px 12px;"
            "}"
            "QPushButton:disabled {"
            "  background: #C7C7CC;"
            "  color: #FFFFFF;"
            "}"
        )

        root_layout = QVBoxLayout(Dialog)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)
        self.lblHistoryTitle = QLabel("전체 기록", Dialog)
        self.lblHistoryTitle.setObjectName("lblHistoryTitle")
        root_layout.addWidget(self.lblHistoryTitle)

        self.tblFullHistory = QTableWidget(Dialog)
        self.tblFullHistory.setObjectName("tblFullHistory")
        self.tblFullHistory.setColumnCount(4)
        self.tblFullHistory.setHorizontalHeaderLabels(["날짜", "내용", "포인트변화", "잔여포인트"])
        root_layout.addWidget(self.tblFullHistory)

        self.btnCloseHistory = QPushButton("닫기", Dialog)
        self.btnCloseHistory.setObjectName("btnCloseHistory")
        root_layout.addWidget(self.btnCloseHistory)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog: QDialog):
        Dialog.setWindowTitle(QCoreApplication.translate("FullHistoryDialog", "Dialog", None))
