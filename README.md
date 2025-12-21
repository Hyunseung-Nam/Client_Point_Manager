# ClientPointManager

사용자 활동 내역을 기록하고 누적 기준을 충족하면 포인트를 자동 지급하는 **PySide6 기반 데스크톱 애플리케이션**입니다.  
SRP/OOP 원칙과 MVC 구조를 적용하여 **역할을 명확히 분리**하고, **안전한 확장성과 유지보수성**을 확보했습니다.

---

## 주요 기능

- 사용자 등록 및 활동 A/B 횟수 입력·수정  
- 누적 **10회 달성 시 자동 포인트 지급(기본 1,000pt)** 및 지급 로그 기록  
- 사용자 목록 검색·필터링 및 **다중 선택 후 일괄 포인트 지급**  
- 포인트 지급 내역 확인을 위한 **로그 뷰 제공**  
- 실행 시 JSON 데이터 파일 자동 생성 및 저장/백업  

---

## 기술 스택

- **Python 3.10+**
- **PySide6 (Qt 기반 GUI)**
- 표준 라이브러리: `json`, `datetime`, `os`

---

## 설치 및 실행
```bash
1. 레포지토리 복사
git clone https://github.com/Hyunseung-Nam/Client_Point_Manager.git
cd Client_Point_Manager

2. 가상환경 설정(선택사항이지만 권장)
python -m venv .venv
source .venv/bin/activate    # Mac/Linux
.venv\Scripts\activate       # Windows

3. 라이브러리 설치
pip install -r requirements.txt

4. 실행
python src/main.py
```

실행 후 `data/users.json`, `data/history.json` 파일이 자동 생성되며 데이터 저장소로 사용됩니다.

---

## 폴더 구조

```bash
src/
 ├─ main.py                  # 앱 진입점, Qt 이벤트 루프 시작
 ├─ modules/
 │   ├─ controller.py        # UI 이벤트 처리 + Model 호출 + View 갱신
 │   ├─ calculator.py        # 활동 누적 및 포인트 계산 로직
 │   ├─ storage.py           # JSON 로드/저장, 초기화, 백업
 │   ├─ validator.py         # 입력값 검증 (전화번호, 횟수 등)
 │   ├─ message_utils.py     # 메시지 출력 헬퍼
 │   └─ messages.py          # 메시지 상수 모음
 └─ ui/
     ├─ main_window_view.py      # 메인 대시보드 View
     ├─ input_dialog_view.py     # 사용자 입력 Dialog
     ├─ usage_dialog_view.py     # 활동 추가 Dialog
     ├─ log_dialog_view.py       # 포인트 지급 로그 Dialog
     ├─ ui_*.py                  # Qt Designer 자동 생성 코드
     └─ *.ui                     # Qt Designer 원본 UI 파일
```

---

## 업데이트 내역

- **v0.1.0**
  - 사용자 등록/수정 기능 추가  
  - 활동 A/B 누적 관리  
  - 포인트 자동 지급 및 로그 기록  
  - 로그 조회 Dialog 추가  

---

## 설계 메모

- **SRP / OOP 준수**  
  검증, 저장, 계산, 메시지 출력 등을 모듈별로 분리하여 **단일 책임 원칙**을 유지했습니다.

- **MVC 구조 적용**  
  - `controller.py` → 앱 전체 흐름 제어  
  - `modules/*` → Model (비즈니스 로직 + 데이터 처리)  
  - `ui/*` → View (화면 구성 및 입력 처리)  
  모듈 간 결합도를 낮추어 유지보수성을 확보했습니다.

- **View 레이어 이중 분리**  
  Qt Designer 생성 코드(`ui_*.py`)와 실제 동작을 구현하는 View 레이어(`*_view.py`)를 분리하여  
  **UI 교체 또는 확장 시 리스크를 최소화**했습니다.
