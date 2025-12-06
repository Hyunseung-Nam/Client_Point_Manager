# modules/calculator.py

COUNTS_FOR_REWARD = 10

def add_usage(users, phone, process1, process2):
    """사용자 데이터에 작업 횟수를 추가 (데이터 변경 로직)"""
    if phone not in users:
        users[phone] = {"process1": 0, "process2": 0, "total_points": 0}
    users[phone]["process1"] += process1
    users[phone]["process2"] += process2

def apply_reward(user_data, points:int):
    """
    사용자 데이터의 작업 횟수를 초기화하고 포인트를 업데이트
    """
    process1 = user_data.get('process1', 0)
    process2 = user_data.get('process2', 0)
    total_counts = process1 + process2
    
    current_points = user_data.get('total_points', 0) 
    user_data['total_points'] = current_points + points
    
    remaining_counts = total_counts % 10
    
    user_data['process1'] = remaining_counts
    user_data['process2'] = 0

def check_reward_needed(total_counts):
    """포인트 지급 필요 여부 확인 (10회 기준)"""
    return total_counts >= COUNTS_FOR_REWARD

def format_phone(phone: str) -> str:
    """전화번호 형식 변환 01012345678 -> 010-1234-5678"""
    if len(phone) == 11:
        return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone

def normalize_phone(phone: str) -> str:
    """전화번호 형식 변환 010-1234-5678 -> 01012345678"""
    return phone.replace("-", "")

# =======================================
# 백업을 위한 함수
# =======================================
def get_total_points(phone):
    """사용자의 누적 포인트를 계산 (Model/calculator 책임)"""
    from .storage import load_logs 
    logs = load_logs()
    total_points = 0
    for log in logs:
        if log.get("phone") == phone:
            total_points += log.get("points", 0)
    return total_points