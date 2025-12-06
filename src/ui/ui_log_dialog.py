# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_dialogLAHPzS.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        if not LogDialog.objectName():
            LogDialog.setObjectName(u"LogDialog")
        LogDialog.resize(780, 350)
        self.tableWidget = QTableWidget(LogDialog)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(-40, -50, 841, 411))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(False)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet(u"QWidget {\n"
"    background-color: #f5f6fa;\n"
"    font-family: 'Segoe UI';\n"
"    color: #2f3640;\n"
"    font-size: 14px;\n"
"}")
        self.label_5 = QLabel(LogDialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(330, 10, 221, 31))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR"])
        font1.setPointSize(11)
        font1.setBold(True)
        self.label_5.setFont(font1)
        self.tableLogs = QTableWidget(LogDialog)
        if (self.tableLogs.columnCount() < 5):
            self.tableLogs.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableLogs.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableLogs.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableLogs.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableLogs.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableLogs.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableLogs.setObjectName(u"tableLogs")
        self.tableLogs.setGeometry(QRect(20, 50, 741, 251))
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR"])
        self.tableLogs.setFont(font2)
        self.tableLogs.setStyleSheet(u"QTableWidget {\n"
"    background: white;\n"
"    border: 1px solid #E0E0E0;\n"
"    gridline-color: #E0E0E0;\n"
"    alternate-background-color: #F7F7F7;\n"
"    selection-background-color: #D6E4FF;\n"
"    selection-color: #000000;\n"
"    \n"
"    border-radius: 10px;\n"
"    padding: 8px; \n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #F0F0F0;\n"
"    padding: 6px;\n"
"    border: 0px;\n"
"    font-weight: bold;\n"
"    color: #444;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QWidget#centralwidget {\n"
"    background-color: #F2F2F2;\n"
"}")
        self.tableLogs.setColumnCount(5)
        self.tableLogs.horizontalHeader().setDefaultSectionSize(144)
        self.tableLogs.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.btnClose = QPushButton(LogDialog)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(20, 310, 741, 31))
        font3 = QFont()
        font3.setFamilies([u"Noto Sans KR"])
        font3.setBold(True)
        self.btnClose.setFont(font3)
        self.btnClose.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b7bec;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3867d6;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2d5dc0;\n"
"}\n"
"")

        self.retranslateUi(LogDialog)

        QMetaObject.connectSlotsByName(LogDialog)
    # setupUi

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(QCoreApplication.translate("LogDialog", u"Dialog", None))
        self.label_5.setText(QCoreApplication.translate("LogDialog", u"\ud3ec\uc778\ud2b8 \uc9c0\uae09 \ub0b4\uc5ed", None))
        ___qtablewidgetitem = self.tableLogs.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LogDialog", u"\ubc88\ud638", None));
        ___qtablewidgetitem1 = self.tableLogs.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LogDialog", u"\ub0a0\uc9dc / \uc2dc\uac04", None));
        ___qtablewidgetitem2 = self.tableLogs.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LogDialog", u"\uc804\ud654\ubc88\ud638", None));
        ___qtablewidgetitem3 = self.tableLogs.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("LogDialog", u"\ud3ec\uc778\ud2b8", None));
        ___qtablewidgetitem4 = self.tableLogs.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("LogDialog", u"\uc9c0\uae09 \uc0ac\uc720", None));
        self.btnClose.setText(QCoreApplication.translate("LogDialog", u"\ub2eb\uae30", None))
    # retranslateUi

