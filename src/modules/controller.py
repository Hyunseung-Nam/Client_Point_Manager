# modules/controller.py

# Model, View 및 Utility 임포트
from .storage import load_users, save_users, delete_users, save_logs
from .calculator import add_usage, apply_reward, check_reward_needed, normalize_phone, COUNTS_FOR_REWARD
from ui.input_dialog_view import InputDialog 
from ui.log_dialog_view import LogDialog 
from ui.usage_dialog_view import UsageDialog

# [상수 정의]
POINTS_TO_GIVE = 2000
COUNTS_FOR_REWARD = COUNTS_FOR_REWARD

# [클래스 정의]
class Controller:
    """
    프로그램의 흐름을 제어하고 View와 Model 간의 중개자 역할을 수행
    Controller는 개별 기능을 직접 구현하지 않음
    """
    
    def __init__(self, ui_view):
        self.view = ui_view
        self.users = load_users()
        
        # 초기 화면 구성을 위해 화면 갱신 지시 메서드 실행
        self.update_dashboard_command() 

    # =============================================================
    # 이벤트 처리 및 흐름 제어
    # =============================================================
    
    # --------------------------------------
    # 사용자 삭제
    # --------------------------------------
    def handle_delete_click(self):
        """삭제 버튼 클릭 시 흐름 제어"""
        
        # 1. View에게 선택된 고객 목록 요청
        selected_phones = self.view.get_selected_phones()

        if not selected_phones:
            self.view.show_warning("선택 오류", "사용자를 한 명 이상 선택해주세요.")
            return

        # 2. View에게 최종 확인 질문 명령
        confirm = self.view.ask_confirmation("삭제 확인", f"{len(selected_phones)}명의 사용자 정보를 정말로 삭제하시겠습니까?")
        
        if not confirm:
            return

        try:
            # 3. Model에게 삭제 명령 (Storage 호출)
            delete_users(selected_phones)
            
            # 4. View에게 최종 명령
            self.view.show_information("삭제 완료", f"{len(selected_phones)}명의 사용자 정보가 삭제되었습니다.")
            
            # 5. 메모리 데이터 갱신 및 View 갱신 명령
            self.users = load_users() # 메모리 데이터 갱신
            self.update_dashboard_command()
            
        except Exception as e:
            # 오류 발생 시 View에게 경고 명령
            self.view.show_warning("오류 발생", f"삭제 중 오류가 발생했습니다: {e}")
            
            
    # ------------------------------------------
    # 사용자 추가 다이얼로그 (open_input_dialog 정의)
    # ------------------------------------------
    def open_input_dialog(self):
        """
        신규 사용자 등록 흐름을 제어
        (Dialog 실행 -> 성공 시 Model 호출 -> View 명령)
        """
        dialog_view = InputDialog(self.view)
        
        # 1. Dialog 실행: Dialog 내부에서 모든 검증과 확인이 처리됨
        if dialog_view.exec(): 
            # 2. Dialog가 성공적으로 닫혔으므로, Controller는 저장 로직을 실행
            phone, process1, process2 = dialog_view.get_data()
            
            # 3. Model 호출 (add_usage와 save_users)
            add_usage(self.users, phone, process1, process2)
            save_users(self.users)
            
            # 4. View에게 최종 명령
            self.view.show_information("등록 완료", "등록이 완료되었습니다.") 
            self.update_dashboard_command()

    # ----------------------------------------------
    # (기존 사용자) 작업 횟수 추가 다이얼로그 (open_usage_dialog 정의)
    # ----------------------------------------------
    def open_usage_dialog(self):
        selected_phones = self.view.get_selected_phones()
        
        if not selected_phones:
            self.view.show_warning("선택 오류", "사용자를 선택해주세요.")
            return
            
        if len(selected_phones) > 1:
            self.view.show_warning("선택 오류", "하나의 사용자만 선택해주세요.")
            return

        phone = normalize_phone(selected_phones[0])
        dialog_view = UsageDialog(self.view)
        
        if dialog_view.exec():
            laundry, dry = dialog_view.get_data()
            
            # Model 호출 (Controller의 책임)
            add_usage(self.users, phone, laundry, dry)
            save_users(self.users)
            
            # View에게 완료 메시지 및 갱신 명령
            self.view.show_information("등록 완료", "등록이 완료되었습니다.")
            self.update_dashboard_command()
            
    # ----------------------------------------
    # 로그 보기 (open_log_dialog 정의)
    # ----------------------------------------
    def open_log_dialog(self):
        """로그 보기 다이얼로그를 열고 실행 흐름을 제어"""
        
        # 1. View 계층의 Dialog 객체 생성 (Controller의 책임)
        # self.view를 부모 위젯으로 전달하여 팝업 위치를 지정
        dialog_view = LogDialog(self.view)
        
        # 2. Dialog 실행 명령 (Controller의 책임)
        dialog_view.exec()
    
    # --------------------------------------------------------
    # 포인트 지급 처리 (handle_reward_click 정의)
    # --------------------------------------------------------
    def handle_reward_click(self):
        """선택된 사용자에게 포인트 지급을 처리하는 흐름을 제어"""
        
        # 1. View에게 선택된 전화번호 목록 요청 (View의 책임)
        selected_phones = self.view.get_selected_phones() 

        if not selected_phones:
            # 2. View에게 경고 메시지 표시 명령
            self.view.show_warning("선택 오류", "사용자를 한 명 이상 선택해주세요.")
            return
        
        # 3. View에게 확인 질문 명령 (Controller가 흐름을 제어)
        confirm = self.view.ask_confirmation("포인트 지급 확인", "선택하신 사용자에게 리워드를 지급하시겠습니까?")
        if confirm != True:
            return

        # 4. Model 호출: 비즈니스 로직 실행 및 데이터 저장
        for phone in selected_phones:
            # 고객 데이터 업데이트 (Model/Calculator의 책임)
            apply_reward(self.users[phone], POINTS_TO_GIVE) 
            
            # 로그 기록 (Model/Storage의 책임)
            save_logs({
                "phone": phone, 
                "points": POINTS_TO_GIVE, 
                "reason": "누적 10회 달성"
            })
        
        # 고객 데이터 파일에 저장 (Model/Storage의 책임)
        save_users(self.users)
        
        # 5. View에게 최종 명령
        self.view.show_information("지급 완료", "선택된 사용자에게 포인트 지급이 완료되었습니다.")
        
        # 6. View에게 대시보드 갱신 명령
        self.update_dashboard_command()
        
    # -------------------------------------------------------------
    # 검색 (filter_table 정의)
    # -------------------------------------------------------------
    def filter_table(self):
        """
        View로부터 검색 키워드를 받아 고객 목록을 필터링하고 View에게 렌더링을 명령
        """
        # View에게 검색 키워드 요청 (View가 input 필드 값을 읽어옴)
        keyword = self.view.get_search_keyword() 

        # 키워드가 없으면 전체 목록 갱신 명령을 내립니다.
        if not keyword:
            self.update_dashboard_command()
            return
        
        # Controller 내부에서 검색 로직 처리 및 데이터 준비
        # _prepare_display_data가 Model 데이터를 필터링하고 가공
        data_for_view = self._prepare_display_data(keyword)

        # View에게 렌더링 명령 (View의 render_customer_list 메서드 호출)
        self.view.render_customer_list(data_for_view)
    
    # -------------------------------------------------------------------
    # 데이터 준비 및 갱신 명령
    # -------------------------------------------------------------------

    def update_dashboard_command(self):
        """
        Model으로부터 필요한 데이터를 수집/가공한 후,
        View에게 최종적으로 화면을 그리도록 명령
        (중앙 지시부 역할)
        """
        
        data_for_view = self._prepare_display_data() 
        
        # View에게 렌더링 명령 (View가 테이블 조작을 담당)
        self.view.render_customer_list(data_for_view)
        
        # 2. View에게 검색창을 지우라고 명령 (UX 개선)
        self.view.clear_search_input()

    def _prepare_display_data(self, keyword=None):
        """실제 화면에 표시할 데이터를 Model로부터 조합하고 가공하여 리스트로 반환"""
        data_list = []
        for phone, data in self.users.items():
            if keyword and keyword not in phone:
                continue

            # Model로부터 원시 값 및 캐시 값 읽어오기
            process1 = data.get('process1', 0)
            process2 = data.get('process2', 0)
            
            # 캐시된 total_points 값을 사용 (성능 최적화)
            # 데이터 파일에 해당 필드가 없을 경우를 대비해 기본값 0 설정
            total_points = data.get('total_points', 0)
            
            # 2. View를 위한 최종 값 계산 (Controller의 책임)
            total_counts = process1 + process2
            reward_needed = check_reward_needed(total_counts)
            remaining = COUNTS_FOR_REWARD - total_counts
            
            # 3. View가 렌더링할 최종 딕셔너리 포장
            data_list.append({
                'phone': phone,               
                'process1': process1,           
                'process2': process2,
                'total_counts': total_counts, 
                'reward_needed': reward_needed,
                'remaining': remaining,      
                'total_points': total_points
            })
        return data_list