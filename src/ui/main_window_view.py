# ui/mainwindow_view.py

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import Qt, QColor
from PySide6.QtCore import QTimer
from .ui_main_window import Ui_MainWindow
from modules.message_utils import show_information, show_warning, ask_confirmation
from modules.calculator import normalize_phone, format_phone


class MainWindow(QMainWindow):
    """
    메인 화면 View.

    역할:
        고객 목록과 상세 패널을 표시한다.

    책임:
        UI 렌더링과 사용자 피드백 표시만 수행한다.

    외부 의존성:
        PySide6 위젯, Ui_MainWindow, message_utils.
    """
    def __init__(self):
        super().__init__()

        # UI 로드
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._toast_timer = QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self._clear_status_toast)

        # 테이블 기본 설정
        self.ui.tblCustomers.verticalHeader().setVisible(False)
        self.ui.tblCustomers.setSortingEnabled(True)
        self.ui.tblCustomers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblCustomers.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.btnGrantReward.setEnabled(False)
        self.apply_column_ratio()
        # 창 제목 설정
        self.setWindowTitle("고객 포인트 관리")
        
    # =========================================================
    # Controller가 명령하는 메서드
    # =========================================================
    def connect_controller(self, controller_instance):
        """
        Controller 참조를 연결한다.

        Args:
            controller_instance: Controller 인스턴스.

        Returns:
            None

        Side Effects:
            내부 controller 참조를 갱신한다.

        Raises:
            없음
        """
        self.controller = controller_instance
        
    def clear_search_input(self):
        """
        검색 입력 필드를 초기화한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            검색 입력창이 비워진다.

        Raises:
            없음
        """
        # self.ui를 통해 검색 입력 위젯에 접근하고 clear() 메서드를 호출
        self.ui.leSearch.clear()
        
    def get_selected_phone(self):
        """
        선택된 row의 전화번호를 반환한다.

        Args:
            없음

        Returns:
            str | None: 선택된 전화번호 또는 None.

        Side Effects:
            없음

        Raises:
            없음
        """
        table = self.ui.tblCustomers
        row = table.currentRow()
        if row < 0:
            return None
        phone_display = table.item(row, 1).text()
        return normalize_phone(phone_display)
    
    def get_search_keyword(self):
        """
        검색 입력창 텍스트를 반환한다.

        Args:
            없음

        Returns:
            str: 검색 키워드.

        Side Effects:
            없음

        Raises:
            없음
        """
        return self.ui.leSearch.text().strip()

    def select_row_by_phone(self, phone: str):
        """
        전화번호로 테이블 행을 선택한다.

        Args:
            phone: 전화번호(숫자만).

        Returns:
            None

        Side Effects:
            테이블 선택 행이 변경된다.

        Raises:
            없음
        """
        table = self.ui.tblCustomers
        for row in range(table.rowCount()):
            phone_display = table.item(row, 1).text()
            if normalize_phone(phone_display) == phone:
                table.setCurrentCell(row, 0)
                return
        
    def render_customer_table(self, data_list):
        """
        Controller가 준비한 데이터를 테이블에 표시한다.
        
        Args:
        data_list (List[Dict]): 고객 정보가 담긴 딕셔너리 리스트.
            각 딕셔너리는 다음 키를 반드시 포함해야 합니다:
            - 'name': 이름 (str)
            - 'phone': 전화번호 (str)
            - 'points_remaining': 잔여 포인트 (int)
            - 'month_count': 이번달 방문 (int)
            - 'last_visit_at': 최근 방문 (str)
            - 'reward_needed': 지급 필요 여부 (bool)
    
        Returns:
            None

        Side Effects:
            테이블 행이 초기화되고 재구성된다.

        Raises:
            없음
        """
        table = self.ui.tblCustomers
        table.setRowCount(0) # 기존 행 제거
        
        # 1. Controller로부터 받은 데이터를 테이블에 채우는 순수한 View 로직
        for row_data in data_list:
            row = table.rowCount()
            table.insertRow(row)
            
            reward_item = self._create_styled_item(row_data['reward_needed'])

            table.setItem(row, 0, self._item(str(row_data['name'])))
            table.setItem(row, 1, self._item(str(format_phone(row_data['phone']))))
            table.setItem(row, 2, self._item(str(row_data['points_remaining'])))
            table.setItem(row, 3, self._item(str(row_data['month_count'])))
            table.setItem(row, 4, self._item(str(row_data['last_visit_at'])))
            table.setItem(row, 5, reward_item)
            
    def set_reward_button_enabled(self, enabled: bool):
        """
        포인트 지급 버튼 활성/비활성 제어.

        Args:
            enabled: 활성 여부.

        Returns:
            None

        Side Effects:
            지급 버튼 활성 상태가 변경된다.

        Raises:
            없음
        """
        self.ui.btnGrantReward.setEnabled(False)

    def set_action_buttons_enabled(self, enabled: bool):
        """
        주요 액션 버튼 활성/비활성 제어.

        Args:
            enabled: 활성 여부.

        Returns:
            None

        Side Effects:
            주요 버튼 활성 상태가 변경된다.

        Raises:
            없음
        """
        self.ui.btnLaundryPlus.setEnabled(enabled)
        self.ui.btnDryPlus.setEnabled(enabled)
        self.ui.btnBundlePlus.setEnabled(enabled)
        self.ui.btnPointUse.setEnabled(enabled)
        self.ui.btnGrantReward.setEnabled(enabled)
        self.ui.btnOpenFullHistory.setEnabled(enabled)

    def set_point_use_enabled(self, enabled: bool):
        """
        포인트 사용 버튼 활성/비활성.

        Args:
            enabled: 활성 여부.

        Returns:
            None

        Side Effects:
            포인트 사용 버튼 활성 상태가 변경된다.

        Raises:
            없음
        """
        self.ui.btnPointUse.setEnabled(enabled)
        
    # -------------------------------------------
    # 메시지 팝업 실행 (view의 책임을 message_utils에 위임)
    # -------------------------------------------
    def show_information(self, title, message):
        """
        정보 메시지 팝업을 표시한다.

        Args:
            title: 제목 문자열.
            message: 본문 문자열.

        Returns:
            None

        Side Effects:
            QMessageBox가 표시된다.

        Raises:
            없음
        """
        show_information(self, title, message)
        
    def show_warning(self, title, message):
        """
        경고 메시지 팝업을 표시한다.

        Args:
            title: 제목 문자열.
            message: 본문 문자열.

        Returns:
            None

        Side Effects:
            QMessageBox가 표시된다.

        Raises:
            없음
        """
        show_warning(self, title, message)
        
    def ask_confirmation(self, title, question):
        """
        확인 질문을 띄우고 응답을 반환한다.

        Args:
            title: 제목 문자열.
            question: 질문 문자열.

        Returns:
            bool: 사용자의 응답.

        Side Effects:
            QMessageBox가 표시된다.

        Raises:
            없음
        """
        return ask_confirmation(self, title, question)
    
    # ---------------------------------------------------------
    # UI 내부 Helper 메서드 (테이블 스타일링 및 비율 계산)
    # ---------------------------------------------------------  
    def apply_column_ratio(self):
        """
        테이블 컬럼 비율을 적용한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            테이블 컬럼 너비가 변경된다.

        Raises:
            없음
        """
        table = self.ui.tblCustomers
        header = table.horizontalHeader()
        
        # 모든 컬럼을 내용물 크기에 딱 맞게 줄이기
        # ResizeToContents를 쓰면 글자 수만큼만 공간을 차지함.
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # 넓게 보여주고 싶은 핵심 컬럼만 Stretch(남은 공간 꽉 채우기)로 설정
        
        # 0번: 이름
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        # 1번: 전화번호
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # 5번: 지급 필요
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
    
    def _create_styled_item(self, reward_needed):
        """지급 필요 셀 스타일링 로직 (View의 책임)"""
        
        reward_text = "필요" if reward_needed else ""
        reward_item = self._item(reward_text)
        
        if reward_needed:
            reward_item.setBackground(QColor("#1721D4"))
            reward_item.setForeground(QColor("#FAF9F7"))
        return reward_item
    
    def _item(self, text):
        """가운데 정렬 아이템 생성 및 편집 불가능 설정"""
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def update_customer_panel(self, customer: dict):
        """
        선택 고객 상세 패널을 갱신한다.

        Args:
            customer: 고객 데이터 dict.

        Returns:
            None

        Side Effects:
            상세 패널 라벨이 갱신된다.

        Raises:
            없음
        """
        self.ui.lblCustomerName.setText(customer.get("name", ""))
        self.ui.lblCustomerPhone.setText(format_phone(customer.get("phone", "")))
        self.ui.lblPointsRemaining.setText(str(customer.get("points_remaining", 0)))
        self.ui.lblLaundryCount.setText(str(customer.get("laundry", 0)))
        self.ui.lblDryCount.setText(str(customer.get("dry", 0)))
        self.ui.lblTotalCount.setText(str(customer.get("total", 0)))
        self.ui.lblLastVisit.setText(customer.get("last_visit_at", ""))
        self.ui.lblMonthCount.setText(str(customer.get("month_count", 0)))
        reward_text = "지급 필요" if customer.get("reward_needed", False) else "지급 없음"
        self.ui.lblRewardNeededBadge.setText(reward_text)
        self.set_point_use_enabled(customer.get("points_remaining", 0) > 0)

    def clear_customer_panel(self):
        """
        선택 고객 패널을 초기화한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            상세 패널 라벨이 초기화된다.

        Raises:
            없음
        """
        self.ui.lblCustomerName.setText("-")
        self.ui.lblCustomerPhone.setText("-")
        self.ui.lblPointsRemaining.setText("-")
        self.ui.lblLaundryCount.setText("-")
        self.ui.lblDryCount.setText("-")
        self.ui.lblTotalCount.setText("-")
        self.ui.lblLastVisit.setText("-")
        self.ui.lblMonthCount.setText("-")
        self.ui.lblRewardNeededBadge.setText("-")
        self.update_recent_history([])

    def update_recent_history(self, logs: list):
        """
        최근 기록 리스트를 갱신한다.

        Args:
            logs: 로그 리스트.

        Returns:
            None

        Side Effects:
            리스트 위젯 내용이 변경된다.

        Raises:
            없음
        """
        self.ui.listRecentHistory.clear()
        if not logs:
            return
        for log in logs:
            date = log.get("date", "")
            log_type = log.get("type", "")
            reason = log.get("reason", "")
            text = f"{date} | {log_type} {reason}".strip()
            self.ui.listRecentHistory.addItem(text)

    def show_status(self, message: str, timeout_ms: int = 3000):
        """
        상태 토스트를 표시한다.

        Args:
            message: 상태 메시지.
            timeout_ms: 표시 시간(ms).

        Returns:
            None

        Side Effects:
            상태 라벨 내용이 변경된다.

        Raises:
            없음
        """
        self.ui.lblStatusToast.setText(message)
        self._toast_timer.start(timeout_ms)

    def _clear_status_toast(self):
        self.ui.lblStatusToast.setText("")