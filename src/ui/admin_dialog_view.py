# ui/admin_dialog_view.py

from PySide6.QtWidgets import QDialog
from modules.message_utils import show_warning, show_information, ask_confirmation
from modules.validator import validate_phone
from .ui_admin_dialog import Ui_AdminDialog


class AdminDialog(QDialog):
    """
    관리자 기능 다이얼로그.

    역할:
        월 통계 표시 및 수동 지급 입력을 제공한다.

    책임:
        UI 표시와 입력 검증을 수행한다.

    외부 의존성:
        Ui_AdminDialog, message_utils, validator.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AdminDialog()
        self.ui.setupUi(self)

        self._disable_manual_grant()
        self.ui.btnCloseAdmin.clicked.connect(self.reject)
        self.ui.btnManualGrant.clicked.connect(self._handle_manual_grant)
        self.ui.btnDeleteCustomer.clicked.connect(self._handle_delete_customer)
        self._delete_handler = None

    def set_month_options(self, month_keys: list[str], current_month: str):
        """
        월 선택 콤보박스를 설정한다.

        Args:
            month_keys: 월 키 리스트.
            current_month: 현재 선택할 월.

        Returns:
            None

        Side Effects:
            콤보박스 항목이 갱신된다.

        Raises:
            없음
        """
        self.ui.cmbMonth.clear()
        self.ui.cmbMonth.addItems(month_keys)
        if current_month:
            self.ui.cmbMonth.setCurrentText(current_month)

    def update_dashboard(self, report: dict, mom_compare: dict, top5_display: list[str]):
        """
        월 통계 대시보드를 갱신한다.

        Args:
            report: 월 통계 dict.
            mom_compare: 전월 대비 dict.
            top5_display: Top5 표시 문자열 리스트.

        Returns:
            None

        Side Effects:
            통계 라벨 및 리스트가 갱신된다.

        Raises:
            없음
        """
        self.ui.lblStatTotalVisits.setText(str(report.get("total_visits", 0)))
        self.ui.lblStatRewardGranted.setText(str(report.get("reward_granted", 0)))
        self.ui.lblStatPointUsed.setText(str(report.get("point_used", 0)))
        loyal_ratio = report.get("loyal_ratio", 0.0)
        self.ui.lblStatLoyalRatio.setText(f"{loyal_ratio:.0%}")
        self.ui.listTop5Customers.clear()
        for line in top5_display:
            self.ui.listTop5Customers.addItem(line)
        if mom_compare:
            self.ui.lblStatMoMCompare.setText(
                f"입력 {mom_compare.get('total_visits', 0)}, 지급 {mom_compare.get('reward_granted', 0)}, 사용 {mom_compare.get('point_used', 0)}"
            )
        else:
            self.ui.lblStatMoMCompare.setText("-")

    def get_selected_month(self) -> str:
        """
        선택된 월 키를 반환한다.

        Args:
            없음

        Returns:
            str: 선택된 월 키.

        Side Effects:
            없음

        Raises:
            없음
        """
        return self.ui.cmbMonth.currentText()

    def connect_month_changed(self, handler):
        """
        월 변경 이벤트 핸들러를 연결한다.

        Args:
            handler: 호출 가능한 핸들러.

        Returns:
            None

        Side Effects:
            콤보박스 이벤트가 연결된다.

        Raises:
            없음
        """
        self.ui.cmbMonth.currentTextChanged.connect(handler)

    def set_delete_handler(self, handler):
        """
        고객 삭제 핸들러를 설정한다.

        Args:
            handler: 호출 가능한 핸들러.

        Returns:
            None

        Side Effects:
            내부 핸들러 참조가 갱신된다.

        Raises:
            없음
        """
        self._delete_handler = handler

    def _handle_delete_customer(self):
        phone = self.ui.leDeletePhone.text().strip()
        if not validate_phone(phone):
            show_warning(self, "입력 오류", "전화번호가 올바르지 않습니다.")
            return
        confirm = ask_confirmation(self, "삭제 확인", "해당 고객을 삭제하시겠습니까?")
        if not confirm:
            return
        if not self._delete_handler:
            show_warning(self, "오류", "삭제 처리기가 연결되지 않았습니다.")
            return
        try:
            self._delete_handler(phone)
            show_information(self, "삭제 완료", "고객이 삭제되었습니다.")
        except Exception:
            show_warning(self, "오류", "고객 삭제 중 오류가 발생했습니다.")

    def _handle_manual_grant(self):
        show_warning(self, "지급 방식", "자동 지급만 가능합니다.")

    def _disable_manual_grant(self):
        self.ui.leManualPhone.setEnabled(False)
        self.ui.spnManualPoints.setEnabled(False)
        self.ui.leManualReason.setEnabled(False)
        self.ui.btnManualGrant.setEnabled(False)
