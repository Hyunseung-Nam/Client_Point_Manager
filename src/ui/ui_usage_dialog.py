# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'usage_dialogLDTLsq.ui'
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
    QPushButton, QSizePolicy, QSpinBox, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_UsageDialog(object):
    def setupUi(self, UsageDialog):
        if not UsageDialog.objectName():
            UsageDialog.setObjectName(u"UsageDialog")
        UsageDialog.resize(295, 283)
        self.tableWidget_2 = QTableWidget(UsageDialog)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(-20, -50, 521, 421))
        self.tableWidget_2.setStyleSheet(u"QWidget {\n"
"    background-color: #f5f6fa;\n"
"    font-family: 'Segoe UI';\n"
"    color: #2f3640;\n"
"    font-size: 14px;\n"
"}")
        self.label_6 = QLabel(UsageDialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(80, 30, 171, 21))
        font = QFont()
        font.setFamilies([u"Noto Sans KR"])
        font.setPointSize(14)
        font.setBold(True)
        self.label_6.setFont(font)
        self.spinLaundry = QSpinBox(UsageDialog)
        self.spinLaundry.setObjectName(u"spinLaundry")
        self.spinLaundry.setGeometry(QRect(150, 90, 81, 31))
        font1 = QFont()
        font1.setPointSize(11)
        self.spinLaundry.setFont(font1)
        self.spinLaundry.setStyleSheet(u"QSpinBox {\n"
"    background-color: white;\n"
"    border: 1px solid #dcdde1;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QSpinBox:focus {\n"
"    border: 1px solid #4b7bec;\n"
"}\n"
"\n"
"QSpinBox {\n"
"    background: #FFFFFF;      /* \ud770\uc0c9 \ubc30\uacbd */\n"
"    color: #000000;           /* \uac80\uc740 \uae00\uc790 */\n"
"    border: 1px solid #D0D0D0;\n"
"    border-radius: 6px;\n"
"    padding: 4px 6px;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.spinLaundry.setMaximum(20)
        self.spinDry = QSpinBox(UsageDialog)
        self.spinDry.setObjectName(u"spinDry")
        self.spinDry.setGeometry(QRect(150, 140, 81, 31))
        self.spinDry.setFont(font1)
        self.spinDry.setStyleSheet(u"QSpinBox {\n"
"    background-color: white;\n"
"    border: 1px solid #dcdde1;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QSpinBox:focus {\n"
"    border: 1px solid #4b7bec;\n"
"}\n"
"\n"
"QSpinBox {\n"
"    background: #FFFFFF;      /* \ud770\uc0c9 \ubc30\uacbd */\n"
"    color: #000000;           /* \uac80\uc740 \uae00\uc790 */\n"
"    border: 1px solid #D0D0D0;\n"
"    border-radius: 6px;\n"
"    padding: 4px 6px;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.spinDry.setMaximum(20)
        self.label_4 = QLabel(UsageDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 80, 81, 51))
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR"])
        font2.setPointSize(11)
        font2.setBold(False)
        self.label_4.setFont(font2)
        self.label_3 = QLabel(UsageDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 130, 81, 51))
        self.label_3.setFont(font2)
        self.btnSubmit = QPushButton(UsageDialog)
        self.btnSubmit.setObjectName(u"btnSubmit")
        self.btnSubmit.setGeometry(QRect(40, 220, 101, 31))
        font3 = QFont()
        font3.setFamilies([u"Noto Sans KR"])
        font3.setPointSize(11)
        font3.setBold(True)
        self.btnSubmit.setFont(font3)
        self.btnSubmit.setStyleSheet(u"QPushButton {\n"
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
        self.btnCancel = QPushButton(UsageDialog)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setGeometry(QRect(160, 220, 101, 31))
        self.btnCancel.setFont(font3)
        self.btnCancel.setStyleSheet(u"QPushButton {\n"
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

        self.retranslateUi(UsageDialog)

        QMetaObject.connectSlotsByName(UsageDialog)
    # setupUi

    def retranslateUi(self, UsageDialog):
        UsageDialog.setWindowTitle(QCoreApplication.translate("UsageDialog", u"Dialog", None))
        self.label_6.setText(QCoreApplication.translate("UsageDialog", u"\ud65c\ub3d9 \ud69f\uc218 \ucd94\uac00", None))
        self.label_4.setText(QCoreApplication.translate("UsageDialog", u"\ud65c\ub3d9 A \ud69f\uc218", None))
        self.label_3.setText(QCoreApplication.translate("UsageDialog", u"\ud65c\ub3d9 B \ud69f\uc218", None))
        self.btnSubmit.setText(QCoreApplication.translate("UsageDialog", u"\ucd94\uac00", None))
        self.btnCancel.setText(QCoreApplication.translate("UsageDialog", u"\ucde8\uc18c", None))
    # retranslateUi

