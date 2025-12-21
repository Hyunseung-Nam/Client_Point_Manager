# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_dialogjFQmSa.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpinBox, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_InputDialog(object):
    def setupUi(self, InputDialog):
        if not InputDialog.objectName():
            InputDialog.setObjectName(u"InputDialog")
        InputDialog.resize(348, 330)
        self.buttonBox = QDialogButtonBox(InputDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.tableWidget_2 = QTableWidget(InputDialog)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(-50, -50, 521, 421))
        self.tableWidget_2.setStyleSheet(u"QWidget {\n"
"    background-color: #f5f6fa;\n"
"    font-family: 'Segoe UI';\n"
"    color: #2f3640;\n"
"    font-size: 14px;\n"
"}")
        self.label_5 = QLabel(InputDialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(110, 30, 161, 21))
        font = QFont()
        font.setFamilies([u"Noto Sans KR"])
        font.setPointSize(14)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label = QLabel(InputDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 80, 71, 51))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR"])
        font1.setPointSize(11)
        font1.setBold(False)
        self.label.setFont(font1)
        self.inputPhone = QLineEdit(InputDialog)
        self.inputPhone.setObjectName(u"inputPhone")
        self.inputPhone.setGeometry(QRect(110, 90, 211, 31))
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR"])
        font2.setPointSize(11)
        self.inputPhone.setFont(font2)
        self.inputPhone.setStyleSheet(u"QLineEdit {\n"
"    background-color: white;\n"
"    border: 1px solid #dcdde1;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #4b7bec;\n"
"}\n"
"\n"
"QLineEdit:placeholder {\n"
"    color: #888888;     \n"
"    font-style: italic;  \n"
"}")
        self.label_3 = QLabel(InputDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 130, 71, 51))
        self.label_3.setFont(font1)
        self.spinLaundry = QSpinBox(InputDialog)
        self.spinLaundry.setObjectName(u"spinLaundry")
        self.spinLaundry.setGeometry(QRect(110, 140, 81, 31))
        font3 = QFont()
        font3.setPointSize(11)
        self.spinLaundry.setFont(font3)
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
        self.label_2 = QLabel(InputDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 180, 71, 51))
        self.label_2.setFont(font1)
        self.btnSubmit = QPushButton(InputDialog)
        self.btnSubmit.setObjectName(u"btnSubmit")
        self.btnSubmit.setGeometry(QRect(30, 260, 131, 31))
        font4 = QFont()
        font4.setFamilies([u"Noto Sans KR"])
        font4.setPointSize(11)
        font4.setBold(True)
        self.btnSubmit.setFont(font4)
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
        self.btnCancel = QPushButton(InputDialog)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setGeometry(QRect(180, 260, 131, 31))
        self.btnCancel.setFont(font4)
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
        self.spinDry = QSpinBox(InputDialog)
        self.spinDry.setObjectName(u"spinDry")
        self.spinDry.setGeometry(QRect(110, 190, 81, 31))
        self.spinDry.setFont(font3)
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

        self.retranslateUi(InputDialog)
        self.buttonBox.accepted.connect(InputDialog.accept)
        self.buttonBox.rejected.connect(InputDialog.reject)

        QMetaObject.connectSlotsByName(InputDialog)
    # setupUi

    def retranslateUi(self, InputDialog):
        InputDialog.setWindowTitle(QCoreApplication.translate("InputDialog", u"Dialog", None))
        self.label_5.setText(QCoreApplication.translate("InputDialog", u"\uc2e0\uaddc \uc0ac\uc6a9\uc790 \ub4f1\ub85d", None))
        self.label.setText(QCoreApplication.translate("InputDialog", u"\uc804\ud654\ubc88\ud638", None))
        self.inputPhone.setPlaceholderText(QCoreApplication.translate("InputDialog", u"\uc804\ud654\ubc88\ud638\ub97c \uc785\ub825\ud574\uc8fc\uc138\uc694", None))
        self.label_3.setText(QCoreApplication.translate("InputDialog", u"\ud65c\ub3d9 A \ud69f\uc218", None))
        self.label_2.setText(QCoreApplication.translate("InputDialog", u"\ud65c\ub3d9 B \ud69f\uc218", None))
        self.btnSubmit.setText(QCoreApplication.translate("InputDialog", u"\ucd94\uac00", None))
        self.btnCancel.setText(QCoreApplication.translate("InputDialog", u"\ucde8\uc18c", None))
    # retranslateUi

