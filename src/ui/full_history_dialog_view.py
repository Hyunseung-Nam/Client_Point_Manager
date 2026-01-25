# ui/full_history_dialog_view.py

import logging
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from PySide6.QtWidgets import QHeaderView
from .ui_full_history_dialog import Ui_FullHistoryDialog

logger = logging.getLogger(__name__)


class FullHistoryDialog(QDialog):
    """
    선택 고객의 전체 기록 다이얼로그.

    역할:
        선택 고객의 로그 테이블을 표시한다.

    책임:
        로그 렌더링 및 닫기 동작을 처리한다.

    외부 의존성:
        Ui_FullHistoryDialog.
    """

    def __init__(self, parent=None, phone: str = ""):
        super().__init__(parent)
        self.phone = phone
        self.ui = Ui_FullHistoryDialog()
        self.ui.setupUi(self)
        self.ui.tblFullHistory.verticalHeader().setVisible(False)
        self.ui.tblFullHistory.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnCloseHistory.clicked.connect(self.reject)
        self.apply_column_ratio()

    def apply_column_ratio(self):
        """
        열 비율을 적용한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            테이블 열 폭이 변경된다.

        Raises:
            없음
        """
        table = self.ui.tblFullHistory
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def load_history(self, logs: list):
        """
        로그 데이터를 테이블로 표시한다.

        Args:
            logs: 전체 로그 리스트.

        Returns:
            None

        Side Effects:
            테이블 행이 갱신된다.

        Raises:
            없음
        """
        try:
            table = self.ui.tblFullHistory
            table.setRowCount(0)
            for log in logs:
                if log.get("phone") != self.phone:
                    continue
                row = table.rowCount()
                table.insertRow(row)
                date = log.get("date", "")
                log_type = log.get("type", "")
                reason = log.get("reason", "")
                points = log.get("points", "")
                remain = log.get("points_remaining_after", "")
                table.setItem(row, 0, self._item(date))
                table.setItem(row, 1, self._item(f"{log_type} {reason}".strip()))
                table.setItem(row, 2, self._item(points))
                table.setItem(row, 3, self._item(remain))
            table.resizeColumnsToContents()
        except Exception:
            logger.exception("FullHistoryDialog render failed")

    def _item(self, text):
        """
        테이블 아이템을 생성한다.

        Args:
            text: 표시할 텍스트.

        Returns:
            QTableWidgetItem: 생성된 아이템.

        Side Effects:
            없음

        Raises:
            없음
        """
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(132)
        return item
