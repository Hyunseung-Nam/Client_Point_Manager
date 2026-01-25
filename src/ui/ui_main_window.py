# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QLabel,
    QTableWidget,
    QGroupBox,
    QListWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 720)
        MainWindow.setStyleSheet(
            "QWidget {"
            "  font-family: 'Noto Sans KR';"
            "  font-size: 14px;"
            "  color: #1D1D1F;"
            "  background-color: #F5F5F7;"
            "}"
            "QLineEdit, QSpinBox, QTextEdit, QComboBox {"
            "  background: #FFFFFF;"
            "  border: 1px solid #D2D2D7;"
            "  border-radius: 8px;"
            "  padding: 6px 8px;"
            "}"
            "QLineEdit:focus, QSpinBox:focus, QTextEdit:focus, QComboBox:focus {"
            "  border: 1px solid #0071E3;"
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

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        root_layout = QVBoxLayout(self.centralwidget)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # Top bar
        top_bar = QHBoxLayout()
        self.leSearch = QLineEdit(self.centralwidget)
        self.leSearch.setObjectName("leSearch")
        self.leSearch.setPlaceholderText("고객 검색(이름/전화)")

        self.btnAddCustomer = QPushButton(self.centralwidget)
        self.btnAddCustomer.setObjectName("btnAddCustomer")
        self.btnAddCustomer.setText("고객 추가")

        self.btnRefresh = QPushButton(self.centralwidget)
        self.btnRefresh.setObjectName("btnRefresh")
        self.btnRefresh.setText("새로고침")

        self.lblStatusToast = QLabel(self.centralwidget)
        self.lblStatusToast.setObjectName("lblStatusToast")
        self.lblStatusToast.setText("")
        self.lblStatusToast.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lblStatusToast.setStyleSheet("color: #6E6E73;")

        top_bar.addWidget(self.leSearch, 3)
        top_bar.addWidget(self.btnAddCustomer, 0)
        top_bar.addWidget(self.btnRefresh, 0)
        top_bar.addWidget(self.lblStatusToast, 2)

        root_layout.addLayout(top_bar)

        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)
        root_layout.addLayout(content_layout, 1)

        # Left table
        self.tblCustomers = QTableWidget(self.centralwidget)
        self.tblCustomers.setObjectName("tblCustomers")
        self.tblCustomers.setColumnCount(6)
        self.tblCustomers.setHorizontalHeaderLabels(
            ["이름", "전화번호", "잔여포인트", "이번달", "최근방문", "지급필요"]
        )
        self.tblCustomers.setAlternatingRowColors(True)
        content_layout.addWidget(self.tblCustomers, 3)

        # Right panel
        right_panel = QVBoxLayout()
        content_layout.addLayout(right_panel, 2)

        self.grpCustomer = QGroupBox(self.centralwidget)
        self.grpCustomer.setObjectName("grpCustomer")
        self.grpCustomer.setTitle("고객 정보")
        customer_layout = QGridLayout(self.grpCustomer)
        customer_layout.setHorizontalSpacing(12)
        customer_layout.setVerticalSpacing(8)

        self.lblCustomerName = QLabel("-")
        self.lblCustomerName.setObjectName("lblCustomerName")
        self.lblCustomerPhone = QLabel("-")
        self.lblCustomerPhone.setObjectName("lblCustomerPhone")
        self.lblPointsRemaining = QLabel("-")
        self.lblPointsRemaining.setObjectName("lblPointsRemaining")
        self.lblLaundryCount = QLabel("-")
        self.lblLaundryCount.setObjectName("lblLaundryCount")
        self.lblDryCount = QLabel("-")
        self.lblDryCount.setObjectName("lblDryCount")
        self.lblTotalCount = QLabel("-")
        self.lblTotalCount.setObjectName("lblTotalCount")
        self.lblLastVisit = QLabel("-")
        self.lblLastVisit.setObjectName("lblLastVisit")
        self.lblMonthCount = QLabel("-")
        self.lblMonthCount.setObjectName("lblMonthCount")
        self.lblRewardNeededBadge = QLabel("-")
        self.lblRewardNeededBadge.setObjectName("lblRewardNeededBadge")

        customer_layout.addWidget(QLabel("이름"), 0, 0)
        customer_layout.addWidget(self.lblCustomerName, 0, 1)
        customer_layout.addWidget(QLabel("전화번호"), 1, 0)
        customer_layout.addWidget(self.lblCustomerPhone, 1, 1)
        customer_layout.addWidget(QLabel("잔여 포인트"), 2, 0)
        customer_layout.addWidget(self.lblPointsRemaining, 2, 1)
        customer_layout.addWidget(QLabel("빨래"), 3, 0)
        customer_layout.addWidget(self.lblLaundryCount, 3, 1)
        customer_layout.addWidget(QLabel("건조"), 4, 0)
        customer_layout.addWidget(self.lblDryCount, 4, 1)
        customer_layout.addWidget(QLabel("총합"), 5, 0)
        customer_layout.addWidget(self.lblTotalCount, 5, 1)
        customer_layout.addWidget(QLabel("최근 방문"), 6, 0)
        customer_layout.addWidget(self.lblLastVisit, 6, 1)
        customer_layout.addWidget(QLabel("이번달 방문"), 7, 0)
        customer_layout.addWidget(self.lblMonthCount, 7, 1)
        customer_layout.addWidget(QLabel("지급 필요"), 8, 0)
        customer_layout.addWidget(self.lblRewardNeededBadge, 8, 1)

        right_panel.addWidget(self.grpCustomer)

        # One-click buttons
        btn_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        self.btnLaundryPlus = QPushButton("빨래 +1")
        self.btnLaundryPlus.setObjectName("btnLaundryPlus")
        self.btnDryPlus = QPushButton("건조 +1")
        self.btnDryPlus.setObjectName("btnDryPlus")
        self.btnBundlePlus = QPushButton("빨래+건조 +1")
        self.btnBundlePlus.setObjectName("btnBundlePlus")
        self.btnPointUse = QPushButton("포인트 사용")
        self.btnPointUse.setObjectName("btnPointUse")
        self.btnGrantReward = QPushButton("지급 완료")
        self.btnGrantReward.setObjectName("btnGrantReward")

        row1.addWidget(self.btnLaundryPlus)
        row1.addWidget(self.btnDryPlus)
        row2.addWidget(self.btnBundlePlus)
        row2.addWidget(self.btnPointUse)
        btn_layout.addLayout(row1)
        btn_layout.addLayout(row2)
        btn_layout.addWidget(self.btnGrantReward)
        right_panel.addLayout(btn_layout)

        # Recent history
        self.grpRecentHistory = QGroupBox(self.centralwidget)
        self.grpRecentHistory.setObjectName("grpRecentHistory")
        self.grpRecentHistory.setTitle("최근 기록")
        history_layout = QVBoxLayout(self.grpRecentHistory)
        self.listRecentHistory = QListWidget(self.grpRecentHistory)
        self.listRecentHistory.setObjectName("listRecentHistory")
        self.btnOpenFullHistory = QPushButton("전체 기록 보기", self.grpRecentHistory)
        self.btnOpenFullHistory.setObjectName("btnOpenFullHistory")
        history_layout.addWidget(self.listRecentHistory)
        history_layout.addWidget(self.btnOpenFullHistory)
        right_panel.addWidget(self.grpRecentHistory, 1)

        # Bottom bar
        bottom_bar = QHBoxLayout()
        self.btnUndo = QPushButton("되돌리기", self.centralwidget)
        self.btnUndo.setObjectName("btnUndo")
        self.btnAdmin = QPushButton("관리자", self.centralwidget)
        self.btnAdmin.setObjectName("btnAdmin")
        bottom_bar.addWidget(self.btnUndo)
        bottom_bar.addWidget(self.btnAdmin)
        root_layout.addLayout(bottom_bar)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
