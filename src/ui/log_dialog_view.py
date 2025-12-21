# ui/log_dialog_view.py

import logging
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHeaderView
from .ui_log_dialog import Ui_LogDialog
from modules.storage import load_history
from modules.calculator import format_phone

logger = logging.getLogger(__name__)

class LogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        self.ui.tableLogs.verticalHeader().setVisible(False)
        
        self.setFixedSize(860, 399)
        
        self.setWindowTitle("포인트 지급 내역")
        
        # 셀 편집 불가 설정
        self.ui.tableLogs.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 닫기 버튼 이벤트
        self.ui.btnClose.clicked.connect(self.reject)

        # 로그 데이터 로딩
        self.load_log_table()
        
        # 열 비율 조정
        self.apply_column_ratio()
        
    # # -------------------------------------------------
    # # 창 크기 조절 → 열 비율 자동 재조정
    # # -------------------------------------------------
    # def resizeEvent(self, event):
    #     self.apply_column_ratio()
    #     super().resizeEvent(event)
        
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

    # =================================================
    # 로그 테이블 채우기
    # =================================================
    def load_log_table(self):
        try:
            logs = load_history()

            table = self.ui.tableLogs
            table.setRowCount(0)

            for log in logs:
                log_type = log.get("type", "reward")
                # reward 로그만 표시
                if log_type != "reward":
                    continue
                
                row = table.rowCount()
                table.insertRow(row)

                # log 데이터 필드
                date = log.get("date", "")
                phone = log.get("phone", "")
                points = log.get("points","")
                reason = log.get("reason", "")
                row_idx = row + 1
                formatted_phone = format_phone(phone)
                
                count_before = log.get("count_before","")
                count_after = log.get("count_after","")
                
                if count_before is None or count_after is None:
                    transition = ""
                else:
                    transition = f"{count_before} → {count_after}"

                # 테이블에 삽입
                table.setItem(row, 0, self._item(str(row_idx)))
                table.setItem(row, 1, self._item(date))
                table.setItem(row, 2, self._item(formatted_phone))
                table.setItem(row, 3, self._item(points))
                table.setItem(row, 4, self._item(transition))
                table.setItem(row, 5, self._item(reason))

            table.resizeColumnsToContents()
        except:
            logger.exception("LogDialog render failed")
            raise

    # -------------------------------------------------
    # 테이블 아이템 생성 도우미
    # -------------------------------------------------
    def _item(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(132)  # 가운데 정렬
        return item
