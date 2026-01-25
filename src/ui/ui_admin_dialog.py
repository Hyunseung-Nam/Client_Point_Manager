# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QListWidget,
    QGroupBox,
)


class Ui_AdminDialog(object):
    def setupUi(self, AdminDialog: QDialog):
        if not AdminDialog.objectName():
            AdminDialog.setObjectName("AdminDialog")
        AdminDialog.resize(520, 520)
        AdminDialog.setStyleSheet(
            "QWidget {"
            "  font-family: 'Noto Sans KR';"
            "  font-size: 13px;"
            "  color: #1D1D1F;"
            "  background-color: #F5F5F7;"
            "}"
            "QLineEdit, QSpinBox, QTextEdit, QComboBox {"
            "  background: #FFFFFF;"
            "  border: 1px solid #D2D2D7;"
            "  border-radius: 8px;"
            "  padding: 6px 8px;"
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
            "QGroupBox {"
            "  border: 1px solid #E5E5EA;"
            "  border-radius: 12px;"
            "  margin-top: 8px;"
            "  background: #FFFFFF;"
            "}"
            "QGroupBox::title {"
            "  subcontrol-origin: margin;"
            "  left: 12px;"
            "  padding: 0 4px;"
            "  font-weight: 600;"
            "}"
        )

        root_layout = QVBoxLayout(AdminDialog)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # Month selector
        top_row = QHBoxLayout()
        self.cmbMonth = QComboBox(AdminDialog)
        self.cmbMonth.setObjectName("cmbMonth")
        top_row.addWidget(QLabel("월 선택"))
        top_row.addWidget(self.cmbMonth)
        root_layout.addLayout(top_row)

        # Stats
        stats_group = QGroupBox("월 통계", AdminDialog)
        stats_layout = QGridLayout(stats_group)
        stats_layout.setHorizontalSpacing(12)
        stats_layout.setVerticalSpacing(8)
        self.lblStatTotalVisits = QLabel("-", stats_group)
        self.lblStatTotalVisits.setObjectName("lblStatTotalVisits")
        self.lblStatRewardGranted = QLabel("-", stats_group)
        self.lblStatRewardGranted.setObjectName("lblStatRewardGranted")
        self.lblStatPointUsed = QLabel("-", stats_group)
        self.lblStatPointUsed.setObjectName("lblStatPointUsed")
        self.lblStatLoyalRatio = QLabel("-", stats_group)
        self.lblStatLoyalRatio.setObjectName("lblStatLoyalRatio")
        self.lblStatMoMCompare = QLabel("-", stats_group)
        self.lblStatMoMCompare.setObjectName("lblStatMoMCompare")
        self.listTop5Customers = QListWidget(stats_group)
        self.listTop5Customers.setObjectName("listTop5Customers")

        stats_layout.addWidget(QLabel("이번달 입력횟수"), 0, 0)
        stats_layout.addWidget(self.lblStatTotalVisits, 0, 1)
        stats_layout.addWidget(QLabel("포인트 지급 횟수"), 1, 0)
        stats_layout.addWidget(self.lblStatRewardGranted, 1, 1)
        stats_layout.addWidget(QLabel("포인트 사용 횟수"), 2, 0)
        stats_layout.addWidget(self.lblStatPointUsed, 2, 1)
        stats_layout.addWidget(QLabel("단골 비율"), 3, 0)
        stats_layout.addWidget(self.lblStatLoyalRatio, 3, 1)
        stats_layout.addWidget(QLabel("Top5"), 4, 0)
        stats_layout.addWidget(self.listTop5Customers, 4, 1)
        stats_layout.addWidget(QLabel("전월 대비"), 5, 0)
        stats_layout.addWidget(self.lblStatMoMCompare, 5, 1)
        root_layout.addWidget(stats_group)

        # Manual grant
        manual_group = QGroupBox("포인트 수동 지급", AdminDialog)
        manual_layout = QGridLayout(manual_group)
        manual_layout.setHorizontalSpacing(12)
        manual_layout.setVerticalSpacing(8)
        self.leManualPhone = QLineEdit(manual_group)
        self.leManualPhone.setObjectName("leManualPhone")
        self.leManualPhone.setPlaceholderText("전화번호(숫자만)")
        self.spnManualPoints = QSpinBox(manual_group)
        self.spnManualPoints.setObjectName("spnManualPoints")
        self.spnManualPoints.setMinimum(1)
        self.spnManualPoints.setValue(1)
        self.leManualReason = QLineEdit(manual_group)
        self.leManualReason.setObjectName("leManualReason")
        self.leManualReason.setPlaceholderText("지급 사유(필수)")
        self.btnManualGrant = QPushButton("포인트 수동 지급", manual_group)
        self.btnManualGrant.setObjectName("btnManualGrant")
        manual_layout.addWidget(QLabel("전화번호"), 0, 0)
        manual_layout.addWidget(self.leManualPhone, 0, 1)
        manual_layout.addWidget(QLabel("포인트"), 1, 0)
        manual_layout.addWidget(self.spnManualPoints, 1, 1)
        manual_layout.addWidget(QLabel("사유"), 2, 0)
        manual_layout.addWidget(self.leManualReason, 2, 1)
        manual_layout.addWidget(self.btnManualGrant, 3, 0, 1, 2)
        root_layout.addWidget(manual_group)

        # Delete customer
        delete_group = QGroupBox("고객 삭제", AdminDialog)
        delete_group.setObjectName("grpDeleteCustomer")
        delete_layout = QGridLayout(delete_group)
        delete_layout.setHorizontalSpacing(12)
        delete_layout.setVerticalSpacing(8)
        self.leDeletePhone = QLineEdit(delete_group)
        self.leDeletePhone.setObjectName("leDeletePhone")
        self.leDeletePhone.setPlaceholderText("전화번호(숫자만)")
        self.btnDeleteCustomer = QPushButton("고객 삭제", delete_group)
        self.btnDeleteCustomer.setObjectName("btnDeleteCustomer")
        delete_layout.addWidget(QLabel("전화번호"), 0, 0)
        delete_layout.addWidget(self.leDeletePhone, 0, 1)
        delete_layout.addWidget(self.btnDeleteCustomer, 1, 0, 1, 2)
        root_layout.addWidget(delete_group)

        # Close
        self.btnCloseAdmin = QPushButton("닫기", AdminDialog)
        self.btnCloseAdmin.setObjectName("btnCloseAdmin")
        root_layout.addWidget(self.btnCloseAdmin)

        self.retranslateUi(AdminDialog)

    def retranslateUi(self, AdminDialog):
        AdminDialog.setWindowTitle(QCoreApplication.translate("AdminDialog", "Admin", None))
