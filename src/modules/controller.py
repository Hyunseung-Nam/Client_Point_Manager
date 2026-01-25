# modules/controller.py

# Model 및 Utility 임포트
import logging
from .storage import load_users, save_users, delete_users, save_history
from .calculator import add_usage, apply_reward, check_reward_needed, normalize_phone, split_eligible, get_remaining, COUNTS_FOR_REWARD
from .messages import CONFIRM_REWARD_PAYMENT, ERROR_SELECT_USER, USER_REGISTERED
from ui.input_dialog_view import InputDialog 
from ui.log_dialog_view import LogDialog
from ui.usage_dialog_view import UsageDialog

logger = logging.getLogger(__name__)

# [상수 정의] 모듈 레벨 상수
APP_VERSION = "v1.2"
POINTS_TO_GIVE = 2000

# [클래스 정의]
class Controller:
    """프로그램의 흐름을 제어하고 View와 Model 간의 중개자 역할을 수행"""
    
    def __init__(self, ui_view):
        self.view = ui_view
        self.users = load_users()
        
        # Controller가 View의 메서드를 호출하여 초기 상태 갱신 명령
        self.update_dashboard_command() 

    # -------------------------------------------------------------
    # 1. View Events Handling (이벤트 처리 및 흐름 제어)
    # -------------------------------------------------------------
    
    # ===================================
    # 사용자 삭제
    # ===================================
    def handle_delete_click(self):
        """삭제 버튼 클릭 시 흐름 제어"""
        
        # 1. View에게 선택된 사용자 목록 요청
        selected_phones = self.view.get_selected_phones()

        if not selected_phones:
            logger.warning("Delete blocked: no selection")
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return

        # 2. View에게 최종 확인 질문 명령
        confirm = self.view.ask_confirmation("삭제 확인", f"{len(selected_phones)}명의 사용자 정보를 정말로 삭제하시겠습니까?")
        
        if confirm is not True: # True/False 반환 여부에 따라 수정 필요
            logger.info("Delete canceled: selected=%d", len(selected_phones))
            return

        try:
            # 삭제 스냅샷 (복구용)
            # snapshot_path = snapshot_deleted_users(self.users, selected_phones)
            # 삭제 실행
            delete_users(selected_phones)
            save_history({
                "type": "delete_users",
                "deleted_count": len(selected_phones),
                # "phones_masked": [p[:3] + "****" + p[-4:] if len(p) >= 11 else p for p in selected_phones],
                # "snapshot": snapshot_path.name,   # 파일명만 남기면 깔끔
                "app_version": APP_VERSION,
            })
            logger.info("Delete success: requested=%d", len(selected_phones))
            # 4. View에게 최종 명령
            self.view.show_information("삭제 완료", f"{len(selected_phones)}명의 사용자 정보가 삭제되었습니다.")
            
            # 5. 메모리 데이터 갱신 및 View 갱신 명령
            self.users = load_users() # 메모리 데이터 갱신
            self.update_dashboard_command()
            
        except Exception as e:
            logger.exception("Delete failed: requested=%d", len(selected_phones))
            # I/O 오류 발생 시 View에게 경고 명령
            self.view.show_warning("오류 발생", f"삭제 중 오류가 발생했습니다: {e}")
            
            
    # ===================================
    # 사용자 추가 다이얼로그 (open_input_dialog 정의)
    # ===================================
    def open_input_dialog(self):
        """
        신규 사용자 등록 플로우를 제어합니다.
        (Dialog 실행 -> 성공 시 Model 호출 -> View 명령)
        """
        dialog_view = InputDialog(self.view)
        
        # 1. Dialog 실행: Dialog 내부에서 모든 검증과 확인이 처리됨
        if dialog_view.exec(): 
            # 2. Dialog가 성공적으로 닫혔으므로, Controller는 저장 로직을 실행
            phone, activity_1, activity_2 = dialog_view.get_data()
            try:
                # 3. Model 호출 (add_usage와 save_users)
                add_usage(self.users, phone, activity_1, activity_2)
                save_users(self.users)
                logger.info("user added: phone=%s activity_1=%d activity_2=%d", phone, activity_1, activity_2)
                # 4. View에게 최종 명령
                self.view.show_information("등록 완료", USER_REGISTERED) 
                self.update_dashboard_command()
            except Exception:
                logger.exception("user add failed: phone=%s", phone)
                return

    # ===================================
    # (기존 사용자) 이용 추가 다이얼로그 (open_usage_dialog 정의)
    # ===================================
    def open_usage_dialog(self):
        selected_phones = self.view.get_selected_phones()
        
        if not selected_phones:
            logger.warning("Usage add blocked: no user selected")
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
            
        if len(selected_phones) > 1:
            logger.warning(
            "Usage add blocked: multiple users selected (%d)",
            len(selected_phones)
            )
            self.view.show_warning("선택 오류", "하나의 사용자만 선택해주세요.")
            return

        phone = normalize_phone(selected_phones[0])
        dialog_view = UsageDialog(self.view)
        
        if dialog_view.exec():
            activity_1, activity_2 = dialog_view.get_data()
            
            # Model 호출 (Controller의 책임)
            add_usage(self.users, phone, activity_1, activity_2)
            save_users(self.users)
            logger.info("Usage added: phone=%s activity_1=%d activity_2=%d", phone, activity_1, activity_2)
            # View에게 완료 메시지 및 갱신 명령
            self.view.show_information("추가 완료", "추가되었습니다.")
            self.update_dashboard_command()
            
    # ===================================
    # 로그 보기 (open_log_dialog 정의)
    # ===================================
    def open_log_dialog(self):
        """로그 보기 다이얼로그를 열고 실행 플로우를 제어합니다."""
        
        # 1. View 계층의 Dialog 객체 생성 (Controller의 책임)
        #    self.view를 부모 위젯으로 전달하여 팝업 위치를 지정합니다.
        dialog_view = LogDialog(self.view)
        
        # 2. Dialog 실행 명령 (Controller의 책임)
        dialog_view.exec()
    
    # ===================================
    # 포인트 지급 처리 (handle_reward_click 정의)
    # ===================================
    def handle_reward_click(self):
        """선택된 사용자에게 포인트 지급을 처리하는 플로우를 제어합니다."""
        
        # 1. 🟢 View에게 선택된 전화번호 목록 요청 (View의 책임)
        selected_phones = self.view.get_selected_phones() 

        if not selected_phones:
            logger.warning("Reward blocked: no selection")
            # 2. View에게 경고 메시지 표시 명령
            self.view.show_warning("선택 오류", ERROR_SELECT_USER)
            return
        
        eligible, insufficient = split_eligible(self.users, selected_phones, counts_for_reward=COUNTS_FOR_REWARD)
        
        if insufficient:
            logger.info("Reward precheck: selected=%d eligible=%d insufficient=%d",
                len(selected_phones), len(eligible), len(insufficient))
            msg = f"선택된 사용자 중 {len(insufficient)}명은 누적 횟수가 부족하여 지급이 불가합니다.\n\n"
            msg += "해당 사용자을 제외하고 나머지만 지급을 진행할까요?"
            proceed = self.view.ask_confirmation("지급 대상 확인", msg)  # 진행/취소
            if not proceed:
                logger.info("Reward canceled at precheck: selected=%d", len(selected_phones))
                return
        
        if not eligible:
            logger.warning("Reward blocked: no eligible users (selected=%d)", len(selected_phones))
            self.view.show_warning("지급 불가", "지급 가능한 사용자이 없습니다.")
            return
        
        # 3. 🟢 View에게 확인 질문 명령 (Controller가 흐름을 제어)
        confirm = self.view.ask_confirmation("포인트 지급 확인", CONFIRM_REWARD_PAYMENT)
        
        # ❗️ QMessageBox.Yes와 비교하는 로직을 가정 (View가 True/False를 반환하도록 설계했다면 변경 필요)
        # 현재는 View가 ask_confirmation에서 QMessageBox.Yes 상수를 직접 반환한다고 가정합니다.
        if confirm != True:
            logger.info("Reward canceled at confirm: eligible=%d", len(eligible))
            return
        
        # 중복 클릭 방지
        self.view.set_reward_button_enabled(False)
        try:
            success = 0
            errors = 0
            # 4. 🟢 Model 호출: 비즈니스 로직 실행 및 데이터 저장
            for phone in eligible:
                # 사용자 데이터 업데이트 (Model/Calculator의 책임)
                result = apply_reward(self.users[phone], points=POINTS_TO_GIVE, counts_for_reward=COUNTS_FOR_REWARD)
                if not result["ok"]:
                    errors += 1
                    count_before = result.get("count_before", "?")
                    self.view.show_warning(
                        "처리 오류",
                        f"현재 누적 횟수는 {count_before}회입니다."
                    )
                    continue
                
                success += 1
                # 로그 기록 (Model/Storage의 책임)
                save_history({
                    "type": "reward",
                    "phone": phone, 
                    "points": POINTS_TO_GIVE,
                    "count_before": result['count_before'],
                    "count_after" : result['count_after'],
                    "counts_for_reward": COUNTS_FOR_REWARD,
                    "reason": f"누적 {COUNTS_FOR_REWARD}회 달성",
                    "app_version": APP_VERSION,
                })
            save_history({
                "type": "reward_batch",
                "selected":len(selected_phones),
                "eligible": len(eligible),
                "excluded": len(insufficient),
                "success": success,
                "errors" : errors,
                "counts_for_reward": COUNTS_FOR_REWARD,
                "app_version": APP_VERSION,
            })
            logger.info("Reward batch done: selected=%d eligible=%d excluded=%d success=%d errors=%d",
            len(selected_phones), len(eligible), len(insufficient), success, errors)
            
            
            # 사용자 데이터 파일에 저장 (Model/Storage의 책임)
            save_users(self.users)
            
            # 5. View에게 최종 명령
            self.view.show_information("지급 완료", f"{success}명 지급 완료")
            
            # 6. View에게 대시보드 갱신 명령
            self.update_dashboard_command()
        except Exception as e:
            logger.exception("Reward batch failed: selected=%d eligible=%d", len(selected_phones), len(eligible))
            self.view.show_warning("오류", f"처리 중 오류가 발생했습니다: {e}")
        finally:
            self.view.set_reward_button_enabled(True)
        
    # ===================================
    # 검색 (filter_table 정의)
    # ===================================
    def filter_table(self):
        """
        View로부터 검색 키워드를 받아 사용자 목록을 필터링하고 View에게 렌더링을 명령합니다.
        """
        # 1. View에게 검색 키워드 요청 (View가 input 필드 값을 읽어옴)
        keyword = self.view.get_search_keyword() 

        if not keyword:
            # 2. 키워드가 없으면 전체 목록 갱신 명령을 내립니다.
            self.update_dashboard_command()
            return
        
        # 3. Controller 내부에서 검색 로직 처리 및 데이터 준비
        # _prepare_display_data가 Model 데이터를 필터링하고 가공합니다.
        data_for_view = self._prepare_display_data(keyword)

        # 4. 🟢 View에게 렌더링 명령 (View의 render_user_list 메서드 호출)
        self.view.render_user_list(data_for_view)
    
    # -------------------------------------------------------------
    # 2. Data Preparation & Command (데이터 준비 및 갱신 명령)
    # -------------------------------------------------------------

    def update_dashboard_command(self):
        """View에게 화면 갱신을 명령하기 위한 데이터를 준비합니다."""
        
        data_for_view = self._prepare_display_data() 
        
        # View에게 렌더링 명령 (View가 테이블 조작을 담당)
        self.view.render_user_list(data_for_view)
        
        # 2. 🟢 View에게 검색창을 지우라고 명령 (UX 개선)
        self.view.clear_search_input()

    def _prepare_display_data(self, keyword=None):
        """실제 화면에 표시할 데이터를 Model로부터 조합하고 가공하여 리스트로 반환"""
        data_list = []
        for phone, data in self.users.items():
            if keyword and keyword not in phone:
                continue

            # 1. 🟢 Model로부터 원시 값 및 캐시 값 읽어오기
            activity_1 = data.get('activity_1', 0)
            activity_2 = data.get('activity_2', 0)
            
            # 🟢 [수정됨] 캐시된 total_points 값을 사용 (성능 최적화)
            # 데이터 파일에 해당 필드가 없을 경우를 대비해 기본값 0을 설정
            total_points = data.get('total_points', 0)
            
            # 2. View를 위한 최종 값 계산 (Controller의 책임)
            total_counts = activity_1 + activity_2
            reward_needed = check_reward_needed(total_counts)
            remaining = get_remaining(total_counts, COUNTS_FOR_REWARD)
            
            # 3. View가 렌더링할 최종 딕셔너리 포장
            data_list.append({
                'phone': phone,               
                'activity_1': activity_1,           
                'activity_2': activity_2,
                'total_counts': total_counts, 
                'reward_needed': reward_needed,
                'remaining': remaining,      
                'total_points': total_points # 캐시된 값 사용
            })
        return data_list