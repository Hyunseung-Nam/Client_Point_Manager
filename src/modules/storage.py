# modules/storage.py

import os
import json
from datetime import datetime

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def load_users():
    """사용자 데이터를 파일에서 로드 (없으면 빈 dict 반환)"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(data):
    """사용자 데이터를 파일에 저장"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_logs():
    """로그 데이터를 파일에서 로드 (없으면 빈 list 반환)"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_logs(log_entry):
    """로그 데이터를 파일에 추가"""
    logs = load_logs()
    log_entry['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    logs.append(log_entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)
        
def delete_users(phone_list):
    """데이터 딕셔너리에서 사용자를 삭제하고 저장함"""
    users = load_users()
    for phone in phone_list:
        if phone in users:
            del users[phone]
    save_users(users)


# ----------------------------
# 파일 존재 여부 체크 + 자동 생성
# ----------------------------
def ensure_files_exist():
    """데이터 폴더와 JSON 파일이 없으면 자동 생성"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


# ============================
# 파일이 깨졌을 때 백업
# ============================
def backup_file(filename: str):
    """깨진 JSON 파일 자동 백업"""
    backup_name = f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    try:
        os.rename(filename, backup_name)
    except:
        pass
