# ui/input_dialog_view.py

from PySide6.QtWidgets import QDialog
from modules.validator import validate_phone, validate_not_empty
from modules.message_utils import show_information, ask_confirmation, show_warning
from .ui_input_dialog import Ui_InputDialog


class InputDialog(QDialog):
    """
    고객 등록 다이얼로그.

    역할:
        고객 이름/전화번호/메모 입력을 수집한다.

    책임:
        입력 검증과 확인 팝업을 수행한다.

    외부 의존성:
        Ui_InputDialog, message_utils, validator.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_InputDialog()
        self.ui.setupUi(self)
        
        self.setFixedSize(360, 280)
        self.setWindowTitle("고객 등록")

        # 버튼 연결
        self.ui.btnSubmit.clicked.connect(self.handle_submit)
        self.ui.btnCancel.clicked.connect(self.reject)
        

    def handle_submit(self):
        """
        '추가' 버튼 클릭 이벤트 처리.

        Args:
            없음

        Returns:
            None

        Side Effects:
            입력값 검증 후 다이얼로그가 닫힐 수 있다.

        Raises:
            없음
        """
        name = self.ui.leName.text().strip()
        phone = self.ui.lePhone.text().strip()

        if not validate_not_empty(phone):
            self.show_warning("필수 입력 오류", "전화번호를 입력해주세요.")
            return

        if not validate_phone(phone):
            confirm = ask_confirmation(
                self,
                "전화번호 확인",
                "전화번호 형식이 올바르지 않습니다.\n그래도 등록하시겠습니까?"
            )
            if confirm is False:
                return

        if not validate_not_empty(name):
            confirm = ask_confirmation(
                self,
                "이름 확인",
                "이름이 비어있습니다. 그대로 등록하시겠습니까?"
            )
            if confirm is False:
                return

        super().accept() # Dialog가 닫히면서 Controller의 exec()가 True를 반환
        
    # 입력한 데이터 가져오기
    def get_data(self):
        """
        입력한 데이터를 반환한다.

        Args:
            없음

        Returns:
            tuple[str, str, str]: (name, phone, memo)

        Side Effects:
            없음

        Raises:
            없음
        """
        name = self.ui.leName.text().strip()
        phone = self.ui.lePhone.text().strip()
        memo = self.ui.teMemo.toPlainText().strip()
        return name, phone, memo
    
    # -------------------------------------------
    # 메시지 팝업 실행 (view의 책임을 message_utils에 위임)
    # -------------------------------------------
    def show_information(self, title, message):
        """
        정보 메시지 팝업을 표시한다.

        Args:
            title: 제목 문자열.
            message: 본문 문자열.

        Returns:
            None

        Side Effects:
            QMessageBox가 표시된다.

        Raises:
            없음
        """
        show_information(self, title, message)
        
    def show_warning(self, title, message):
        """
        경고 메시지 팝업을 표시한다.

        Args:
            title: 제목 문자열.
            message: 본문 문자열.

        Returns:
            None

        Side Effects:
            QMessageBox가 표시된다.

        Raises:
            없음
        """
        show_warning(self, title, message)
        
    def ask_confirmation(self, title, question):
        """
        확인 질문을 띄우고 응답을 반환한다.

        Args:
            title: 제목 문자열.
            question: 질문 문자열.

        Returns:
            bool: 사용자 응답.

        Side Effects:
            QMessageBox가 표시된다.

        Raises:
            없음
        """
        return ask_confirmation(self, title, question)
