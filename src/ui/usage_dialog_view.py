from PySide6.QtWidgets import QDialog
from .ui_usage_dialog import Ui_UsageDialog
from modules.message_utils import ask_confirmation, show_information, show_warning

class UsageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_UsageDialog()
        self.ui.setupUi(self)
        
        self.setFixedSize(236, 227)
        
        self.setWindowTitle("활동 횟수 추가")
        
        # 버튼 연결
        self.ui.btnSubmit.clicked.connect(self.handle_submit)
        self.ui.btnCancel.clicked.connect(self.reject)
        
    
    def handle_submit(self):
        """
        '추가' 버튼 클릭 이벤트 처리. View가 검증과 확인을 주도하여 창 닫힘을 결정
        """
        # 1. View 레벨의 필수 입력 검사
        if not self.ui.spinLaundry.value() and not self.ui.spinDry.value():
            self.show_warning("필수 입력 오류", "이용 횟수를 입력해주세요.")
            return # 다이얼로그를 닫지 않고 유지

        # 모든 검증 및 확인 통과 시, Controller 로직 실행을 위해 Dialog를 닫음
        super().accept() # Dialog가 닫히면서 Controller의 exec()가 True를 반환

    def get_data(self):
        laundry = self.ui.spinLaundry.value()
        dry = self.ui.spinDry.value()
        return laundry, dry
    
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
