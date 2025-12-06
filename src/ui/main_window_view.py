# ui/mainwindow_view.py

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtGui import Qt, QColor
from .ui_main_window import Ui_MainWindow
from modules.message_utils import show_information, show_warning, ask_confirmation
from modules.calculator import normalize_phone, format_phone


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 로드
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 창 크기 고정
        self.setFixedSize(1053, 691)
        self.apply_column_ratio()
        # 창 제목 설정
        self.setWindowTitle("사용자 관리 시스템")
        
    # =========================================================
    # Controller가 명령하는 메서드
    # =========================================================
    def connect_controller(self, controller_instance):
        """View가 주도적으로 자신의 버튼을 Controller의 메서드에 연결"""
        self.ui.btnAddCustomer.clicked.connect(controller_instance.open_input_dialog)
        self.ui.btnAddUsage.clicked.connect(controller_instance.open_usage_dialog)
        self.ui.btnOpenLog.clicked.connect(controller_instance.open_log_dialog)
        self.ui.btnGivePoints.clicked.connect(controller_instance.handle_reward_click)
        self.ui.btnSearch.clicked.connect(controller_instance.filter_table)
        self.ui.btnRefresh.clicked.connect(controller_instance.update_dashboard_command)
        self.ui.btnDeleteCustomer.clicked.connect(controller_instance.handle_delete_click)
        
    def clear_search_input(self):
        """
        [View의 책임] Controller의 명령을 받아 검색 입력 필드를 초기화
        """
        # self.ui를 통해 검색 입력 위젯에 접근하고 clear() 메서드를 호출
        self.ui.searchInput.clear()
        
    def get_selected_phones(self):
        """[View의 책임] 체크된 row의 전화번호 목록을 Controller에게 반환"""
        table = self.ui.tableWidget
        selected_phones = []
        # 테이블을 *직접 조작*하여 데이터를 추출 (View의 책임)
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                phone_display = table.item(row, 1).text()
                selected_phones.append(normalize_phone(phone_display))
        return selected_phones
    
    def get_search_keyword(self):
        """[View의 책임] 검색 입력창(QLineEdit)의 텍스트를 읽어와 반환"""
        search_input = self.ui.searchInput 
        
        return search_input.text().strip()
        
    def render_customer_list(self, data_list):
        """
        [Controller 명령 실행] Controller가 준비한 데이터를 받아 테이블에 표시
        (Controller가 이 함수를 호출할 때, 테이블 조작 로직이 시작됨)
        
        Args:
        data_list (List[Dict]): 고객 정보가 담긴 딕셔너리 리스트.
            각 딕셔너리는 다음 키를 반드시 포함해야 합니다:
            - 'phone': 전화번호 (str)
            - 'process1', 'process2': 작업 완료 횟수 (int)
            - 'total_counts': 총 횟수 (int)
            - 'reward_needed': 보상 필요 여부 (bool)
            - 'remaining': 잔여 횟수 (int)
            - 'total_points': 총 포인트 (int)
    
        Note:
        테이블을 렌더링하기 전 기존 행(row)은 모두 초기화됩니다.
        """
        table = self.ui.tableWidget
        table.setRowCount(0) # 기존 행 제거
        
        # 1. Controller로부터 받은 데이터를 테이블에 채우는 순수한 View 로직
        for row_data in data_list:
            row = table.rowCount()
            table.insertRow(row)
            
            # [View의 책임] QTableWidgetItem 생성 및 스타일링
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chk_item.setCheckState(Qt.Unchecked)
            
            reward_item = self._create_styled_item(row_data['reward_needed'])

            table.setItem(row, 0, chk_item) # 체크박스
            table.setItem(row, 1, self._item(str(format_phone(row_data['phone']))))
            table.setItem(row, 2, self._item(str(row_data['process1'])))
            table.setItem(row, 3, self._item(str(row_data['process2'])))
            table.setItem(row, 4, self._item(str(row_data['total_counts'])))
            table.setItem(row, 5, reward_item)
            table.setItem(row, 6, self._item(str(row_data['remaining'])))
            table.setItem(row, 7, self._item(str(row_data['total_points'])))
        
    # -------------------------------------------
    # 메시지 팝업 실행 (view의 책임을 message_utils에 위임)
    # -------------------------------------------
    def show_information(self, title, message):
        """정보 메시지 팝업 실행"""
        show_information(self, title, message)
        
    def show_warning(self, title, message):
        """경고 메시지 팝업 실행"""
        show_warning(self, title, message)
        
    def ask_confirmation(self, title, question):
        """확인 질문을 띄우고 응답을 반환"""
        return ask_confirmation(self, title, question)
    
    # ---------------------------------------------------------
    # UI 내부 Helper 메서드 (테이블 스타일링 및 비율 계산)
    # ---------------------------------------------------------  
    def apply_column_ratio(self):
        table = self.ui.tableWidget
        header = table.horizontalHeader()
        
        # 모든 컬럼을 내용물 크기에 딱 맞게 줄이기
        # ResizeToContents를 쓰면 글자 수만큼만 공간을 차지함.
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # 넓게 보여주고 싶은 핵심 컬럼만 Stretch(남은 공간 꽉 채우기)로 설정
        
        # 1번: 전화번호
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # 5번: 지급 필요
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        # 7번: 총 포인트
        header.setSectionResizeMode(7, QHeaderView.Stretch)
        
        # 체크박스(0번)는 너무 작아지지 않게 약간의 고정폭 주기
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        table.setColumnWidth(0, 40)
    
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