# 실행부

from __future__ import annotations
import sys, logging
from modules.pathutils import resource_path
from logger import setup_logging
from modules.storage import ensure_files_exist, migrate_users_phone_keys_once, HISTORY_DIR #, DATA_DIR
from PySide6.QtWidgets import QApplication
from ui.main_window_view import MainWindow
from modules.controller import Controller

def main():
    app = QApplication(sys.argv)
    # ensure_data_dir_or_exit(DATA_DIR)

    # 로거 설정
    setup_logging(HISTORY_DIR, level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("앱 시작")

    # 파일 / 데이터 준비
    try:
        ensure_files_exist()
        migrate_users_phone_keys_once()

        # View 객체 생성 (MainWindow)
        mainwindow_view = MainWindow()
        
        # Controller 객체 생성 및 View 연결
        controller = Controller(mainwindow_view)
        mainwindow_view.connect_controller(controller)
        
        # 화면 표시 및 이벤트 루프 시작
        mainwindow_view.show()
        
        exit_code = app.exec()
        logger.info("앱 종료")
        sys.exit(exit_code)
    except Exception:
        logger.exception("앱 비정상 종료")
        raise

if __name__ == "__main__":
    main()
