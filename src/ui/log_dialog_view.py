# ui/log_dialog_view.py

from PySide6.QtWidgets import QDialog, QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from .ui_log_dialog import Ui_LogDialog
from modules.storage import load_logs
from modules.calculator import format_phone


class LogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        
        self.setFixedSize(780, 350)
        
        self.setWindowTitle("포인트 지급 내역")

        # 버튼 연결
        self.ui.btnClose.clicked.connect(self.reject)

        # 로그 데이터 로딩
        self.load_log_table()
        
        # 열 비율 조정
        self.apply_column_ratio()
        
    # -------------------------------------------------
    # 열 비율 적용
    # -------------------------------------------------
    def apply_column_ratio(self):
        table = self.ui.tableLogs
        header = table.horizontalHeader()

        # 모든 컬럼을 내용물 크기에 딱 맞게 줄이기
        # ResizeToContents : 글자 수만큼만 공간 차지
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # 넓게 보여주고 싶은 핵심 컬럼만 Stretch(남은 공간 꽉 채우기)로 설정
        
        # 날짜
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # 전화번호
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        # 포인트
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        # 이유
        header.setSectionResizeMode(4, QHeaderView.Stretch)

    # -------------------------------------------------
    # 로그 테이블 채우기
    # -------------------------------------------------
    def load_log_table(self):
        logs = load_logs()

        table = self.ui.tableLogs
        table.setRowCount(0)

        for log in logs:
            row = table.rowCount()
            table.insertRow(row)

            # log 데이터 필드
            date = log.get("date", "")
            phone = log.get("phone", "")
            points = log.get("points","")
            reason = log.get("reason", "")
            row_idx = row + 1   # 새 행 번호
            formatted_phone = format_phone(phone)

            # 테이블에 삽입
            table.setItem(row, 0, self._item(str(row_idx)))
            table.setItem(row, 1, self._item(date))
            table.setItem(row, 2, self._item(formatted_phone))
            table.setItem(row, 3, self._item(points))
            table.setItem(row, 4, self._item(reason))

    # -------------------------------------------------
    # 테이블 아이템 생성 도우미
    # -------------------------------------------------
    def _item(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(132)  # 가운데 정렬
        return item
