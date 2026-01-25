# modules/controller.py

import logging
from datetime import datetime
from .storage import (
    load_customers,
    save_customers,
    delete_customers,
    load_history,
    append_history,
    pop_last_load_warning,
)
from .calculator import (
    recalc_customer_fields,
    compute_reward_needed,
    remaining_until_reward,
    normalize_phone,
    format_phone,
    create_default_customer,
    build_monthly_report,
    compare_month_over_month,
    COUNTS_FOR_REWARD,
)
from .validator import validate_phone
from .messages import (
    ERROR_SELECT_USER,
    USER_REGISTERED,
    ERROR_INVALID_PHONE,
    ERROR_POINT_INSUFFICIENT,
)
from ui.input_dialog_view import InputDialog
from ui.admin_dialog_view import AdminDialog
from ui.full_history_dialog_view import FullHistoryDialog

logger = logging.getLogger(__name__)

APP_VERSION = "v2.0"
REWARD_GRANT_POINTS = 1
RESET_COUNTS_ON_REWARD = True
AUTO_GRANT_ON_THRESHOLD = True

class Controller:
    """
    프로그램의 흐름을 제어하고 View와 Model 간의 중개자 역할을 수행한다.

    역할:
        UI 이벤트를 처리하고 데이터 갱신 흐름을 관리한다.

    책임:
        화면 업데이트 명령과 저장/로깅 호출을 조율한다.

    외부 의존성:
        storage, calculator, validator, ui dialogs.
    """
    
    def __init__(self, ui_view):
        """
        Controller 초기화.

        Args:
            ui_view: MainWindow 인스턴스.

        Returns:
            None

        Side Effects:
            데이터 로드 및 초기 렌더링을 수행한다.

        Raises:
            Exception: 초기화 중 예외 발생 시 재전파.
        """
        self.view = ui_view
        self.customers = {}
        self.history = []
        self.selected_phone = None
        self.connect_events()
        self.load_initial_data()

    # -------------------------------------------------------------
    # 1. View Events Handling (이벤트 처리 및 흐름 제어)
    # -------------------------------------------------------------
    def connect_events(self):
        """
        UI 이벤트를 연결한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            UI 시그널 연결을 수행한다.

        Raises:
            없음
        """
        ui = self.view.ui
        ui.btnAddCustomer.clicked.connect(self.open_input_dialog)
        ui.btnRefresh.clicked.connect(self.load_initial_data)
        ui.leSearch.textChanged.connect(self.filter_table)
        ui.leSearch.returnPressed.connect(self.quick_add_from_search)
        ui.tblCustomers.itemSelectionChanged.connect(self.handle_table_selection)
        ui.btnLaundryPlus.clicked.connect(self.record_laundry)
        ui.btnDryPlus.clicked.connect(self.record_dry)
        ui.btnBundlePlus.clicked.connect(self.record_bundle)
        ui.btnPointUse.clicked.connect(self.consume_point)
        ui.btnGrantReward.clicked.connect(self.grant_reward)
        ui.btnOpenFullHistory.clicked.connect(self.open_full_log_dialog)
        ui.btnUndo.clicked.connect(self.undo_last_action)
        ui.btnAdmin.clicked.connect(self.open_admin_dialog)

    def load_initial_data(self):
        """
        초기 데이터를 로드하고 화면을 갱신한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            데이터 로드 및 테이블/패널 갱신을 수행한다.

        Raises:
            Exception: 로드 실패 시 재전파.
        """
        try:
            self.customers = load_customers()
            self.history = load_history()
            warning = pop_last_load_warning()
            if warning:
                self.view.show_warning("데이터 복구", warning)
            self._rebuild_month_counts(datetime.now().strftime("%Y-%m"))
            self.refresh_customer_table()
            self.select_customer(None)
        except Exception as exc:
            logger.exception("초기 데이터 로드 실패")
            self.view.show_warning("오류", f"데이터 로드 중 오류가 발생했습니다: {exc}")

    def handle_table_selection(self):
        """
        테이블 선택 변경 시 선택 고객을 갱신한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            선택 고객 패널을 갱신한다.

        Raises:
            없음
        """
        phone = self.view.get_selected_phone()
        self.select_customer(phone)

    def open_input_dialog(self):
        """
        신규 고객 등록 플로우를 제어한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            신규 고객을 저장하고 테이블을 갱신한다.

        Raises:
            없음
        """
        dialog_view = InputDialog(self.view)
        if dialog_view.exec():
            name, phone, memo = dialog_view.get_data()
            phone = normalize_phone(phone)
            if not validate_phone(phone):
                self.view.show_warning("입력 오류", ERROR_INVALID_PHONE)
                return
            if phone not in self.customers:
                self.customers[phone] = create_default_customer(phone, name=name, memo=memo)
            else:
                self.customers[phone]["name"] = name or self.customers[phone].get("name", "")
                self.customers[phone]["memo"] = memo or self.customers[phone].get("memo", "")
            try:
                save_customers(self.customers)
                self.view.show_information("등록 완료", USER_REGISTERED)
                self.refresh_customer_table()
                self.select_customer(phone)
            except Exception:
                logger.exception("고객 등록 저장 실패: phone=%s", phone)

    def quick_add_from_search(self):
        """
        검색창에서 전화번호 입력 후 Enter 시 자동 생성한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            신규 고객이 추가될 수 있다.

        Raises:
            없음
        """
        keyword = normalize_phone(self.view.get_search_keyword())
        if not keyword:
            return
        if not validate_phone(keyword):
            self.view.show_warning("입력 오류", ERROR_INVALID_PHONE)
            return
        if keyword in self.customers:
            self.select_customer(keyword)
            return
        self.customers[keyword] = create_default_customer(keyword)
        try:
            save_customers(self.customers)
            self.refresh_customer_table()
            self.select_customer(keyword)
            self.view.show_status("신규 고객을 자동 등록했습니다.")
        except Exception:
            logger.exception("자동 등록 실패: phone=%s", keyword)

    def record_laundry(self):
        """
        빨래 +1 기록을 추가한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            고객 데이터 및 로그가 갱신된다.

        Raises:
            없음
        """
        self._record_visit("VISIT_LAUNDRY", laundry_inc=1, dry_inc=0, count=1)

    def record_dry(self):
        """
        건조 +1 기록을 추가한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            고객 데이터 및 로그가 갱신된다.

        Raises:
            없음
        """
        self._record_visit("VISIT_DRY", laundry_inc=0, dry_inc=1, count=1)

    def record_bundle(self):
        """
        빨래+건조 +1 기록을 추가한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            고객 데이터 및 로그가 갱신된다.

        Raises:
            없음
        """
        self._record_visit("VISIT_BUNDLE", laundry_inc=1, dry_inc=1, count=2)

    def consume_point(self):
        """
        포인트 사용을 처리한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            고객 포인트 및 로그가 갱신된다.

        Raises:
            없음
        """
        if not self.selected_phone:
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
        customer = self.customers[self.selected_phone]
        if customer.get("points_remaining", 0) <= 0:
            self.view.show_warning("포인트 부족", ERROR_POINT_INSUFFICIENT)
            return
        customer["points_remaining"] -= 1
        recalc_customer_fields(customer)
        self._append_history({
            "type": "POINT_USE",
            "phone": self.selected_phone,
            "points": -1,
            "reason": "포인트 사용",
            "points_remaining_after": customer.get("points_remaining", 0),
        })
        self._save_and_refresh(self.selected_phone, "포인트를 사용했습니다.")

    def grant_reward(self):
        """
        지급 완료 버튼 동작을 처리한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            고객 포인트 및 카운트가 갱신된다.

        Raises:
            없음
        """
        self.view.show_warning("지급 방식", "자동 지급만 가능합니다.")
        return
        if not self.selected_phone:
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
        customer = self.customers[self.selected_phone]
        if not customer.get("reward_needed", False):
            self.view.show_warning("지급 불가", "지급 필요 상태가 아닙니다.")
            return
        self.view.set_reward_button_enabled(False)
        try:
            self._apply_reward_grant(self.selected_phone, reason="누적 10회 달성")
            self._save_and_refresh(self.selected_phone, "지급 완료 처리했습니다.")
        except Exception:
            logger.exception("지급 완료 처리 실패: phone=%s", self.selected_phone)
            self.view.show_warning("오류", "지급 처리 중 오류가 발생했습니다.")
        finally:
            self.view.set_reward_button_enabled(True)

    def manual_grant(self, phone: str, points: int, reason: str):
        """
        관리자 수동 포인트 지급 처리.

        Args:
            phone: 전화번호.
            points: 지급 포인트.
            reason: 지급 사유.

        Returns:
            None

        Side Effects:
            고객 포인트 및 로그가 갱신된다.

        Raises:
            ValueError: 유효하지 않은 입력일 경우.
        """
        if not validate_phone(phone) or points <= 0 or not reason:
            raise ValueError("수동 지급 입력이 올바르지 않습니다.")
        if phone not in self.customers:
            self.customers[phone] = create_default_customer(phone)
        customer = self.customers[phone]
        customer["points_remaining"] = int(customer.get("points_remaining", 0)) + int(points)
        recalc_customer_fields(customer)
        self._append_history({
            "type": "MANUAL_GRANT",
            "phone": phone,
            "points": points,
            "reason": reason,
            "points_remaining_after": customer.get("points_remaining", 0),
        })
        self._save_and_refresh(phone, "수동 지급 완료")

    def undo_last_action(self):
        """
        최근 1회 행동을 되돌린다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            고객 데이터가 변경되고 undo 로그가 기록된다.

        Raises:
            없음
        """
        if not self.selected_phone:
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
        latest = self._find_latest_undoable_log(self.selected_phone)
        if not latest:
            self.view.show_warning("되돌리기 불가", "되돌릴 기록이 없습니다.")
            return
        customer = self.customers[self.selected_phone]
        log_type = latest.get("type")
        if log_type in ("VISIT_LAUNDRY", "VISIT_DRY", "VISIT_BUNDLE"):
            customer["laundry"] = max(0, int(customer.get("laundry", 0)) - int(latest.get("laundry_inc", 0)))
            customer["dry"] = max(0, int(customer.get("dry", 0)) - int(latest.get("dry_inc", 0)))
        elif log_type == "POINT_USE":
            customer["points_remaining"] = int(customer.get("points_remaining", 0)) + abs(int(latest.get("points", -1)))
        else:
            self.view.show_warning("되돌리기 제한", "이 기록은 되돌릴 수 없습니다.")
            return
        recalc_customer_fields(customer)
        self._append_history({
            "type": "UNDO",
            "phone": self.selected_phone,
            "reason": f"{log_type} 되돌리기",
        })
        self._save_and_refresh(self.selected_phone, "최근 동작을 되돌렸습니다.")

    def open_admin_dialog(self):
        """
        관리자 다이얼로그를 연다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            관리자 다이얼로그가 표시된다.

        Raises:
            없음
        """
        dialog = AdminDialog(self.view)
        dialog.connect_month_changed(self.on_month_changed)
        month_keys, current_month = self._get_month_keys()
        dialog.set_month_options(month_keys, current_month)
        dialog.set_delete_handler(self.delete_customer)
        self.admin_dialog = dialog
        self.refresh_admin_dashboard(current_month)
        dialog.exec()

    def open_full_log_dialog(self):
        """
        전체 기록 보기 다이얼로그를 연다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            전체 기록 다이얼로그가 표시된다.

        Raises:
            없음
        """
        if not self.selected_phone:
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
        dialog = FullHistoryDialog(self.view, phone=self.selected_phone)
        dialog.load_history(self.history)
        dialog.exec()

    def delete_customer(self, phone: str):
        """
        관리자에서 고객을 삭제한다.

        Args:
            phone: 삭제할 전화번호.

        Returns:
            None

        Side Effects:
            고객 데이터와 로그가 갱신된다.

        Raises:
            ValueError: 유효하지 않은 전화번호 또는 미존재 고객.
        """
        if not validate_phone(phone):
            raise ValueError("전화번호가 올바르지 않습니다.")
        if phone not in self.customers:
            raise ValueError("해당 고객이 존재하지 않습니다.")
        name = self.customers.get(phone, {}).get("name", "")
        del self.customers[phone]
        self._append_history({
            "type": "CUSTOMER_DELETE",
            "phone": phone,
            "reason": "관리자 삭제",
            "name": name,
        })
        save_customers(self.customers)
        if self.selected_phone == phone:
            self.select_customer(None)
        self.refresh_customer_table()

    def refresh_admin_dashboard(self, month_key: str):
        """
        관리자 대시보드를 갱신한다.

        Args:
            month_key: "YYYY-MM" 형식의 월 키.

        Returns:
            None

        Side Effects:
            관리자 화면 통계가 갱신된다.

        Raises:
            없음
        """
        if not getattr(self, "admin_dialog", None):
            return
        try:
            report = build_monthly_report(self.customers, self.history, month_key)
            compare = compare_month_over_month(self.customers, self.history, month_key)
            mom = compare.get("diff", {})
            top5_display = self._format_top5(report.get("top5", []))
            self.admin_dialog.update_dashboard(report, mom, top5_display)
        except Exception as exc:
            logger.exception("관리자 대시보드 갱신 실패: month=%s", month_key)
            self.view.show_warning("오류", f"통계 갱신 중 오류가 발생했습니다: {exc}")

    def on_month_changed(self, month_key: str):
        """
        관리자 월 선택 변경 이벤트 처리.

        Args:
            month_key: "YYYY-MM" 형식의 월 키.

        Returns:
            None

        Side Effects:
            관리자 대시보드 통계를 갱신한다.

        Raises:
            없음
        """
        self.refresh_admin_dashboard(month_key)

    # -------------------------------------------------------------
    # 2. Data Preparation & Command (데이터 준비 및 갱신 명령)
    # -------------------------------------------------------------
    def refresh_customer_table(self):
        """
        고객 테이블을 갱신한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            테이블 UI가 갱신된다.

        Raises:
            없음
        """
        data_for_view = self._prepare_display_data()
        self.view.render_customer_table(data_for_view)

    def filter_table(self):
        """
        검색 키워드로 고객 테이블을 필터링한다.

        Args:
            없음

        Returns:
            None

        Side Effects:
            테이블 UI가 갱신된다.

        Raises:
            없음
        """
        keyword = self.view.get_search_keyword()
        data_for_view = self._prepare_display_data(keyword)
        self.view.render_customer_table(data_for_view)

    def select_customer(self, phone):
        """
        선택 고객을 설정하고 패널을 갱신한다.

        Args:
            phone: 선택된 전화번호.

        Returns:
            None

        Side Effects:
            고객 상세 패널 및 버튼 상태가 변경된다.

        Raises:
            없음
        """
        self.selected_phone = phone if phone in self.customers else None
        if self.selected_phone:
            self.view.select_row_by_phone(self.selected_phone)
        self.update_customer_panel(self.selected_phone)

    def update_customer_panel(self, phone):
        """
        고객 상세 패널을 업데이트한다.

        Args:
            phone: 선택된 전화번호.

        Returns:
            None

        Side Effects:
            상세 패널 UI가 갱신된다.

        Raises:
            없음
        """
        if not phone or phone not in self.customers:
            self.view.clear_customer_panel()
            self.view.set_action_buttons_enabled(False)
            return
        customer = dict(self.customers[phone])
        customer["phone"] = phone
        self.view.update_customer_panel(customer)
        self.view.set_action_buttons_enabled(True)
        self.view.set_reward_button_enabled(customer.get("reward_needed", False))
        recent = self._get_recent_history(phone, limit=5)
        self.view.update_recent_history(recent)

    # -------------------------------------------------------------
    # 내부 헬퍼
    # -------------------------------------------------------------
    def _prepare_display_data(self, keyword=None):
        """
        테이블 렌더링용 데이터를 조합한다.

        Args:
            keyword: 검색 키워드.

        Returns:
            list: 테이블 표시용 dict 리스트.

        Side Effects:
            없음

        Raises:
            없음
        """
        data_list = []
        for phone, data in self.customers.items():
            name = data.get("name", "")
            if keyword:
                if keyword not in phone and keyword not in name:
                    continue
            total = int(data.get("total", 0))
            reward_needed = compute_reward_needed(total)
            remaining = remaining_until_reward(total)
            data_list.append({
                "name": name,
                "phone": phone,
                "points_remaining": data.get("points_remaining", 0),
                "month_count": data.get("month_count", 0),
                "last_visit_at": data.get("last_visit_at", ""),
                "reward_needed": reward_needed,
            })
        return data_list

    def _record_visit(self, log_type: str, laundry_inc: int, dry_inc: int, count: int):
        if not self.selected_phone:
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
        customer = self.customers[self.selected_phone]
        customer["laundry"] = int(customer.get("laundry", 0)) + laundry_inc
        customer["dry"] = int(customer.get("dry", 0)) + dry_inc
        customer["last_visit_at"] = datetime.now().isoformat(timespec="seconds")
        customer["month_count"] = int(customer.get("month_count", 0)) + count
        recalc_customer_fields(customer)
        self._append_history({
            "type": log_type,
            "phone": self.selected_phone,
            "laundry_inc": laundry_inc,
            "dry_inc": dry_inc,
            "count": count,
            "laundry_before": customer.get("laundry", 0) - laundry_inc,
            "dry_before": customer.get("dry", 0) - dry_inc,
            "total_before": customer.get("total", 0) - (laundry_inc + dry_inc),
            "points_remaining_after": customer.get("points_remaining", 0),
        })
        auto_granted = False
        if AUTO_GRANT_ON_THRESHOLD and customer.get("reward_needed", False):
            self.view.set_action_buttons_enabled(False)
            try:
                self._apply_reward_grant(self.selected_phone, reason="누적 10회 달성")
                auto_granted = True
            finally:
                self.view.set_action_buttons_enabled(True)
        status = "기록이 추가되었습니다."
        if auto_granted:
            status = "기록 추가 및 자동 지급 완료"
        self._save_and_refresh(self.selected_phone, status)

    def _apply_reward_grant(self, phone: str, reason: str):
        customer = self.customers[phone]
        before_laundry = int(customer.get("laundry", 0))
        before_dry = int(customer.get("dry", 0))
        before_total = int(customer.get("total", 0))
        customer["points_remaining"] = int(customer.get("points_remaining", 0)) + REWARD_GRANT_POINTS
        if RESET_COUNTS_ON_REWARD:
            customer["laundry"] = 0
            customer["dry"] = 0
        recalc_customer_fields(customer)
        self._append_history({
            "type": "REWARD_GRANTED",
            "phone": phone,
            "points": REWARD_GRANT_POINTS,
            "reason": reason,
            "laundry_before": before_laundry,
            "dry_before": before_dry,
            "total_before": before_total,
            "points_remaining_after": customer.get("points_remaining", 0),
        })

    def _save_and_refresh(self, phone: str, status_message: str):
        try:
            save_customers(self.customers)
            self.refresh_customer_table()
            self.select_customer(phone)
            self.view.show_status(status_message)
        except Exception:
            logger.exception("저장 실패: phone=%s", phone)
            self.view.show_warning("오류", "저장 중 오류가 발생했습니다.")

    def _get_recent_history(self, phone: str, limit: int = 5):
        logs = [log for log in self.history if log.get("phone") == phone]
        logs.sort(key=lambda x: x.get("date", ""), reverse=True)
        return logs[:limit]

    def _append_history(self, entry: dict):
        try:
            entry_local = dict(entry)
            append_history(entry_local)
            entry_local.setdefault("date", datetime.now().isoformat(timespec="seconds"))
            self.history.append(entry_local)
        except Exception:
            logger.exception("history append 실패")

    def _find_latest_undoable_log(self, phone: str):
        for log in sorted(self.history, key=lambda x: x.get("date", ""), reverse=True):
            if log.get("phone") != phone:
                continue
            if log.get("type") in ("VISIT_LAUNDRY", "VISIT_DRY", "VISIT_BUNDLE", "POINT_USE"):
                return log
        return None

    def _build_admin_reports(self):
        current_month = datetime.now().strftime("%Y-%m")
        report = build_monthly_report(self.customers, self.history, current_month)
        prev_month = self._previous_month_key(current_month)
        prev_report = build_monthly_report(self.customers, self.history, prev_month)
        mom_compare = {
            "total_visits": report["total_visits"] - prev_report["total_visits"],
            "reward_granted": report["reward_granted"] - prev_report["reward_granted"],
            "point_used": report["point_used"] - prev_report["point_used"],
            "loyal_ratio": report["loyal_ratio"] - prev_report["loyal_ratio"],
        }
        return {
            "month_keys": [current_month, prev_month],
            "reports": {
                current_month: report,
                prev_month: prev_report,
            },
            "mom_compare": mom_compare,
            "current_month": current_month,
        }

    def _format_top5(self, top5: list[tuple[str, int]]) -> list[str]:
        lines = []
        for phone, count in top5:
            name = self.customers.get(phone, {}).get("name", "")
            label = name if name else phone
            lines.append(f"{label} ({count})")
        if not lines:
            lines.append("기록 없음")
        return lines

    def _get_month_keys(self):
        month_keys = sorted(
            {str(log.get("date", ""))[:7] for log in self.history if str(log.get("date", "")).startswith("20")},
            reverse=True,
        )
        current_month = datetime.now().strftime("%Y-%m")
        if current_month not in month_keys:
            month_keys.insert(0, current_month)
        prev_month = self._previous_month_key(current_month)
        if prev_month not in month_keys:
            month_keys.append(prev_month)
        return month_keys, current_month

    def _rebuild_month_counts(self, month_key: str):
        for customer in self.customers.values():
            customer["month_count"] = 0
        for log in self.history:
            date = str(log.get("date", ""))
            if not date.startswith(month_key):
                continue
            phone = log.get("phone")
            if phone not in self.customers:
                continue
            if log.get("type") in ("VISIT_LAUNDRY", "VISIT_DRY", "VISIT_BUNDLE"):
                count = int(log.get("count", 1))
                self.customers[phone]["month_count"] += count

    def _previous_month_key(self, month_key: str) -> str:
        year, month = map(int, month_key.split("-"))
        if month == 1:
            return f"{year - 1}-12"
        return f"{year}-{month - 1:02d}"