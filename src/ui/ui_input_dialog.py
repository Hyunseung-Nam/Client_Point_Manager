# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)


class Ui_InputDialog(object):
    def setupUi(self, InputDialog: QDialog):
        if not InputDialog.objectName():
            InputDialog.setObjectName("InputDialog")
        InputDialog.resize(360, 280)

        root_layout = QVBoxLayout(InputDialog)
        title = QLabel("신규 고객 등록", InputDialog)
        title.setAlignment(Qt.AlignCenter)
        root_layout.addWidget(title)

        form_layout = QGridLayout()
        root_layout.addLayout(form_layout)

        self.leName = QLineEdit(InputDialog)
        self.leName.setObjectName("leName")
        self.lePhone = QLineEdit(InputDialog)
        self.lePhone.setObjectName("lePhone")
        self.lePhone.setPlaceholderText("전화번호(숫자만)")
        self.teMemo = QTextEdit(InputDialog)
        self.teMemo.setObjectName("teMemo")

        form_layout.addWidget(QLabel("이름"), 0, 0)
        form_layout.addWidget(self.leName, 0, 1)
        form_layout.addWidget(QLabel("전화번호"), 1, 0)
        form_layout.addWidget(self.lePhone, 1, 1)
        form_layout.addWidget(QLabel("메모"), 2, 0)
        form_layout.addWidget(self.teMemo, 2, 1)

        btn_row = QHBoxLayout()
        self.btnSubmit = QPushButton("추가", InputDialog)
        self.btnSubmit.setObjectName("btnSubmit")
        self.btnCancel = QPushButton("취소", InputDialog)
        self.btnCancel.setObjectName("btnCancel")
        btn_row.addWidget(self.btnSubmit)
        btn_row.addWidget(self.btnCancel)
        root_layout.addLayout(btn_row)

        self.retranslateUi(InputDialog)

    def retranslateUi(self, InputDialog: QDialog):
        InputDialog.setWindowTitle(QCoreApplication.translate("InputDialog", "Dialog", None))
