# ui/input_dialog_view.py

from PySide6.QtWidgets import QDialog
from modules.validator import validate_phone
from modules.message_utils import show_information, ask_confirmation, show_warning
from .ui_input_dialog import Ui_InputDialog


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_InputDialog()
        self.ui.setupUi(self)
        
        self.setFixedSize(339, 277)
        
        self.setWindowTitle("사용자 이용 정보 입력")

        # 버튼 연결
        self.ui.btnSubmit.clicked.connect(self.handle_submit)
        self.ui.btnCancel.clicked.connect(self.reject)
        

    def handle_submit(self):
        """
        '추가' 버튼 클릭 이벤트 처리. View가 검증과 확인을 주도하여 창 닫힘을 결정
        """
        phone = self.ui.inputPhone.text().strip()
        
        # 1. View 레벨의 필수 입력 검사
        if not phone:
            self.show_warning("필수 입력 오류", "전화번호와 이용 횟수를 모두 입력해주세요.")
            return # 다이얼로그를 닫지 않고 유지
            
        # 2. 비즈니스 로직 검증 (View가 Validator를 직접 호출 - trade-off)
        if not validate_phone(phone):
            
            # 3. 확인 질문 실행
            confirm = ask_confirmation(
                self, # 부모 위젯으로 Dialog 자체(self)를 사용
                "전화번호 확인", 
                "전화번호 형식이 올바르지 않습니다.\n그래도 등록하시겠습니까?"
            )
            
            # 4. '아니오' 응답 시 Dialog 유지
            if confirm is False: 
                return # 다이얼로그를 닫지 않고 함수 종료

        # 5. 모든 검증 및 확인 통과 시, Controller 로직 실행을 위해 Dialog를 닫음
        super().accept() # Dialog가 닫히면서 Controller의 exec()가 True를 반환
        
    # 입력한 데이터 가져오기
    def get_data(self):
        phone = self.ui.inputPhone.text().strip()
        laundry = self.ui.spinLaundry.value()
        dry = self.ui.spinDry.value()

        return phone, laundry, dry
    
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
