# 실행부

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window_view import MainWindow
from modules.controller import Controller

def main():
    app = QApplication(sys.argv)
    
    # View 객체 생성 (MainWindow)
    mainwindow_view = MainWindow()
    
    # Controller 객체 생성 및 View 연결
    controller = Controller(mainwindow_view)
    mainwindow_view.connect_controller(controller)
    
    # 화면 표시 및 이벤트 루프 시작
    mainwindow_view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
