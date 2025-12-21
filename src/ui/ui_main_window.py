# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowlxDfwx.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1173, 700)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.background = QTableWidget(self.centralwidget)
        self.background.setObjectName(u"background")
        self.background.setGeometry(QRect(-10, -20, 1191, 721))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        self.background.setFont(font)
        self.background.setStyleSheet(u"QWidget {\n"
"    background-color: #f5f6fa;\n"
"    font-family: 'Segoe UI';\n"
"    color: #2f3640;\n"
"    font-size: 14px;\n"
"}")
        self.background.setShowGrid(True)
        self.background.horizontalHeader().setDefaultSectionSize(107)
        self.btnAddCustomer = QPushButton(self.centralwidget)
        self.btnAddCustomer.setObjectName(u"btnAddCustomer")
        self.btnAddCustomer.setGeometry(QRect(1030, 50, 121, 31))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR"])
        font1.setPointSize(11)
        font1.setBold(True)
        self.btnAddCustomer.setFont(font1)
        self.btnAddCustomer.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b7bec;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
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
        self.btnOpenLog = QPushButton(self.centralwidget)
        self.btnOpenLog.setObjectName(u"btnOpenLog")
        self.btnOpenLog.setGeometry(QRect(880, 570, 271, 31))
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR"])
        font2.setPointSize(11)
        font2.setBold(False)
        self.btnOpenLog.setFont(font2)
        self.btnOpenLog.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b7bec;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
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
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(450, 10, 331, 31))
        font3 = QFont()
        font3.setFamilies([u"Noto Sans KR"])
        font3.setPointSize(17)
        font3.setBold(True)
        self.label.setFont(font3)
        self.label.setMouseTracking(False)
        self.label.setTabletTracking(False)
        self.searchInput = QLineEdit(self.centralwidget)
        self.searchInput.setObjectName(u"searchInput")
        self.searchInput.setGeometry(QRect(30, 50, 871, 31))
        font4 = QFont()
        font4.setFamilies([u"Noto Sans KR"])
        font4.setPointSize(11)
        self.searchInput.setFont(font4)
        self.searchInput.setStyleSheet(u"QLineEdit {\n"
"    background-color: white;\n"
"    border: 1px solid #dcdde1;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4b7bec;\n"
"}\n"
"")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(30, 90, 1121, 471))
        self.tableWidget.setFont(font2)
        self.tableWidget.setStyleSheet(u"QTableWidget#tableWidget {\n"
"    background: white;\n"
"    border: 1px solid #E0E0E0;\n"
"    gridline-color: #E0E0E0;\n"
"    alternate-background-color: #F7F7F7;\n"
"    selection-background-color: #D6E4FF;\n"
"    selection-color: #000000;\n"
"    border-radius: 11px;\n"
"    padding: 8px;\n"
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
"/* \ud3ec\ucee4\uc2a4 \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"QTableWidget::item:focus {\n"
"    outline: none;\n"
"    border: none;\n"
"}")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(138)
        self.tableWidget.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.btnGivePoints = QPushButton(self.centralwidget)
        self.btnGivePoints.setObjectName(u"btnGivePoints")
        self.btnGivePoints.setGeometry(QRect(30, 570, 561, 31))
        self.btnGivePoints.setFont(font1)
        self.btnGivePoints.setStyleSheet(u"QPushButton {\n"
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
        self.btnSearch = QPushButton(self.centralwidget)
        self.btnSearch.setObjectName(u"btnSearch")
        self.btnSearch.setGeometry(QRect(910, 50, 111, 31))
        self.btnSearch.setFont(font2)
        self.btnSearch.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b7bec;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
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
        self.btnRefresh = QPushButton(self.centralwidget)
        self.btnRefresh.setObjectName(u"btnRefresh")
        self.btnRefresh.setGeometry(QRect(1060, 10, 91, 31))
        font5 = QFont()
        font5.setFamilies([u"Noto Sans KR"])
        font5.setPointSize(10)
        font5.setBold(False)
        self.btnRefresh.setFont(font5)
        self.btnRefresh.setStyleSheet(u"QPushButton#btnRefresh {\n"
"    background-color: #F5F5F5;\n"
"    color: #333333;\n"
"    border: 1px solid #CCCCCC;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QPushButton#btnRefresh:hover {\n"
"    background-color: #E0E0E0;\n"
"}\n"
"\n"
"QPushButton#btnRefresh:pressed {\n"
"    background-color: #D9D9D9;\n"
"}")
        self.btnAddUsage = QPushButton(self.centralwidget)
        self.btnAddUsage.setObjectName(u"btnAddUsage")
        self.btnAddUsage.setGeometry(QRect(600, 570, 271, 31))
        self.btnAddUsage.setFont(font1)
        self.btnAddUsage.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b7bec;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
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
        self.btnDeleteCustomer = QPushButton(self.centralwidget)
        self.btnDeleteCustomer.setObjectName(u"btnDeleteCustomer")
        self.btnDeleteCustomer.setGeometry(QRect(1010, 610, 141, 31))
        self.btnDeleteCustomer.setFont(font1)
        self.btnDeleteCustomer.setStyleSheet(u"QPushButton {\n"
"    background-color: #C62828;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #B71C1C;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #8E0000;\n"
"}\n"
"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1173, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btnAddCustomer.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc \uc0ac\uc6a9\uc790 \ub4f1\ub85d", None))
        self.btnOpenLog.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8 \ubcf4\uae30", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc790 \ud3ec\uc778\ud2b8 \uad00\ub9ac \ud504\ub85c\uadf8\ub7a8", None))
        self.searchInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\uc804\ud654\ubc88\ud638\ub97c \uc785\ub825\ud574\uc8fc\uc138\uc694", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\uc804\ud654\ubc88\ud638", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\ud65c\ub3d9 A", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\ud65c\ub3d9 B", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\ud569\uacc4", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\ud3ec\uc778\ud2b8 \uc9c0\uae09 \ud544\uc694", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\ub0a8\uc740 \ud69f\uc218", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\ucd1d \ud3ec\uc778\ud2b8", None));
        self.btnGivePoints.setText(QCoreApplication.translate("MainWindow", u"\ud3ec\uc778\ud2b8 \uc9c0\uae09", None))
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.btnRefresh.setText(QCoreApplication.translate("MainWindow", u"\uc0c8\ub85c \uace0\uce68", None))
        self.btnAddUsage.setText(QCoreApplication.translate("MainWindow", u"\ud65c\ub3d9 \ud69f\uc218 \ucd94\uac00", None))
        self.btnDeleteCustomer.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc790 \uc0ad\uc81c", None))
    # retranslateUi

