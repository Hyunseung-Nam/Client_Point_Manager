# modules/storage.py

import json, os, shutil, logging
from pathlib import Path
from datetime import datetime
from .validator import validate_phone
from .calculator import normalize_phone
from .pathutils import data_base_dir

logger = logging.getLogger(__name__)
    
BASE = data_base_dir()
DATA_DIR = BASE / "data"
BACKUP_DIR = BASE / "backup"
USER_FILE = DATA_DIR / "users.json"
HISTORY_FILE = DATA_DIR / "history.json"
HISTORY_DIR = DATA_DIR / "history"

# 초기화 전용 함수
def init_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

def safe_write_json(path: Path, obj, *, backup_dir, ensure_ascii=False, indent=4):
    """
    1) 기존 파일이 있으면 .bak 1개 갱신
    2) 임시파일에 먼저 저장
    3) os.replace로 원본과 교체(가능하면 원자적으로)
    """
    tmp_path = None
    try:
        backup_dir.mkdir(exist_ok=True)
        
        bak_path = backup_dir / (path.name + ".bak")                 # backup/users.json.bak
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        
        # 1) 백업
        if path.exists():
            shutil.copy2(path, bak_path)

        # 2) 임시파일에 저장
        tmp_path.write_text(
            json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent),
            encoding="utf-8"
        )

        # 3) 교체
        os.replace(tmp_path, path)
    except Exception:
        logger.exception("safe_write_json 실패: path=%s tmp=%s bak_dir=%s", path, tmp_path, backup_dir)
        raise

def _load_json_file(path: Path, empty_value, *, not_found_msg: str, parse_error_msg: str, os_error_msg: str, log_path: Path):
    """
    JSON 파일을 읽어 파싱하고 실패 시 기본값을 반환한다.

    Args:
        path: 읽을 JSON 파일 경로
        empty_value: 실패 시 반환할 기본값
        not_found_msg: 파일 미존재 로그 메시지
        parse_error_msg: JSON 파싱 실패 로그 메시지
        os_error_msg: OS 읽기 실패 로그 메시지
        log_path: 로그에 출력할 경로

    Returns:
        object: 파싱된 JSON 또는 기본값
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logger.warning(not_found_msg, log_path)
        return empty_value
    except json.JSONDecodeError:
        logger.error(parse_error_msg, log_path)
        return empty_value
    except OSError:
        logger.exception(os_error_msg, log_path)
        return empty_value

def load_users():
    """사용자 데이터를 파일에서 로드 (예시: 항상 빈 dict 반환)"""
    return _load_json_file(
        USER_FILE,
        {},
        not_found_msg="users.json 없음 - 빈 데이터로 시작: %s",
        parse_error_msg="users.json JSON 파싱 실패(파일 손상 가능): %s",
        os_error_msg="users.json 읽기 실패(OS): %s",
        log_path=USER_FILE,
    )
    
def save_users(data):
    """사용자 데이터를 파일에 저장"""
    try:
        safe_write_json(USER_FILE, data, backup_dir=BACKUP_DIR, ensure_ascii=False, indent=4)
        logger.info("users 저장 성공: %s (%d명)", USER_FILE, len(data))
    except Exception:
        logger.exception("users 저장 실패: %s", USER_FILE)
        raise

def load_history():
    """로그 데이터를 파일에서 로드"""
    return _load_json_file(
        HISTORY_FILE,
        [],
        not_found_msg="history.json 없음 - 빈 데이터로 시작: %s",
        parse_error_msg="history.json JSON 파싱 실패(파일 손상 가능): %s",
        os_error_msg="history.json 읽기 실패(OS): %s",
        log_path=USER_FILE,
    )

def save_history(HISTORY_entry):
    """로그 데이터를 파일에 추가"""
    try:
        history = load_history()
        HISTORY_entry['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        history.append(HISTORY_entry)
        safe_write_json(HISTORY_FILE, history, backup_dir=BACKUP_DIR, ensure_ascii=False, indent=4)
        logger.debug("history.json append: phone=%s points=%s", HISTORY_entry.get("phone"), HISTORY_entry.get("points"))
    except Exception:
        logger.exception("history 저장 실패: %s", HISTORY_FILE)
        raise
        
def delete_users(phone_list):
    """데이터 딕셔너리에서 사용자을 삭제하고 저장합니다."""
    users = load_users()
    before = len(users)
    deleted = 0
    for phone in phone_list:
        if phone in users:
            del users[phone]
            deleted += 1
            
    save_users(users)
    logger.info("사용자 삭제: requested=%d deleted=%d total %d->%d",
                len(phone_list), deleted, before, len(users))
    
# def snapshot_deleted_users(users: dict, phones: list[str]) -> Path:
#     """삭제 직전 복구용 스냅샷 저장(원본 포함)"""
#     target = {p: users.get(p) for p in phones if p in users}
#     ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#     path = BACKUP_DIR / f"deleted_users_{ts}.json"
#     safe_write_json(path, target, backup_dir=BACKUP_DIR, ensure_ascii=False, indent=4)
#     logger.info("삭제 스냅샷 저장: %s (count=%d)", path, len(target))
#     return path

# ----------------------------
# 파일 존재 여부 체크 + 자동 생성
# ----------------------------
def ensure_files_exist():
    """데이터 폴더와 JSON 파일이 없으면 자동 생성"""
    if not USER_FILE.exists():
        USER_FILE.write_text(
            json.dumps({}, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info("users.json 생성: %s", USER_FILE)

    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(
            json.dumps([], indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info("users.json 생성: %s", HISTORY_FILE)
            
def get_total_points(phone):
    """특정 사용자의 누적 포인트를 계산 (Model/Storage의 책임)"""
    history = load_history()
    total_points = 0
    for HISTORY in history:
        if HISTORY.get("phone") == phone:
            total_points += HISTORY.get("points", 0)
    return total_points

# ----------------------------
# Migration (1회 실행)
# ----------------------------
MIGRATION_FLAG = DATA_DIR / ".migrated_phone_v1"

def migrate_users_phone_keys_once():
    logger.info("사용자 전화번호 마이그레이션 시작")
    if MIGRATION_FLAG.exists():
        logger.info("사용자 전화번호 마이그레이션 이미 완료됨 - 스킵")
        return

    DATA_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    users = load_users()
    migrated = {}
    conflicts = []
    invalids = []
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for phone, user_data in users.items():
        clean = normalize_phone(phone)

        if not validate_phone(clean):
            invalids.append({"raw": phone, "normalized": clean, "data": user_data, "migrated_at": now})
            continue

        if clean not in migrated:
            migrated[clean] = user_data
        else:
            migrated[clean] = merge_user_data(migrated[clean], user_data)
            conflicts.append({"raw": phone, "normalized": clean, "data": user_data, "migrated_at": now})
    logger.info(
    "사용자 전화번호 마이그레이션 완료: total=%d migrated=%d conflicts=%d invalids=%d",
    len(users),
    len(migrated),
    len(conflicts),
    len(invalids)
    )

    # 저장
    save_users(migrated)

    if conflicts:
        logger.warning(
        "마이그레이션 충돌 데이터 %d건 발생 - %s 저장",
        len(conflicts),
        BACKUP_DIR / "migration_conflicts_users.json"
        )
        (BACKUP_DIR / "migration_conflicts_users.json").write_text(
            json.dumps(conflicts, ensure_ascii=False, indent=4, default=str),
            encoding="utf-8"
        )

    if invalids:
        logger.warning(
        "유효하지 않은 전화번호 %d건 발생 - %s 저장",
        len(invalids),
        BACKUP_DIR / "migration_invalid_users_keys.json"
        )
        (BACKUP_DIR / "migration_invalid_users_keys.json").write_text(
            json.dumps(invalids, ensure_ascii=False, indent=4, default=str),
            encoding="utf-8"
        )

    MIGRATION_FLAG.write_text(datetime.now().strftime("%Y-%m-%d %H:%M"), encoding="utf-8")
    logger.info("마이그레이션 완료 플래그 기록: %s", MIGRATION_FLAG)
    
def merge_user_data(a: dict, b: dict) -> dict:
    """
    동일 사용자의 중복 데이터 병합
    - activity_1, activity_2: 합산
    - total_points: 로그가 진실이므로 보수적으로 유지
    """
    return {
        "activity_1": int(a.get("activity_1", 0)) + int(b.get("activity_1", 0)),
        "activity_2": int(a.get("activity_2", 0)) + int(b.get("activity_2", 0)),
        "total_points": max(
            int(a.get("total_points", 0)),
            int(b.get("total_points", 0)),
        ),
    }
    
# # ============================
# # 파일이 깨졌을 때 백업
# # ============================
# def backup_file(filename: str):
#     """깨진 JSON 파일 자동 백업"""
#     backup_name = f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
#     try:
#         os.rename(filename, backup_name)
#     except:
#         pass
