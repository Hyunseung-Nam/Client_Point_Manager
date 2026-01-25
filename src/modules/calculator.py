# modules/calculator.py
import re, logging

logger = logging.getLogger(__name__)

COUNTS_FOR_REWARD = 10

def add_usage(users, phone, activity_1, activity_2):
    """사용자 데이터에 이용 횟수를 추가 (데이터 변경 로직)"""
    if phone not in users:
        users[phone] = {"activity_1": 0, "activity_2": 0, "total_points": 0}
    users[phone]["activity_1"] += activity_1
    users[phone]["activity_2"] += activity_2

def apply_reward(USER_data, points=2000, counts_for_reward=COUNTS_FOR_REWARD, consume_order=("activity_2", "activity_1")):
    """
    포인트 지급 및 누적 횟수 차감을 수행하고,
    상태 전이 결과를 반환합니다.
    
    consume_order: 차감 우선순위. 기본은 ("activity_2", "activity_1")
    """
    
    # 지급 전 상태
    activity_1_before = USER_data.get('activity_1', 0)
    activity_2_before = USER_data.get('activity_2', 0)
    count_before = activity_1_before + activity_2_before
    points_before = USER_data.get('total_points', 0)

    # 방어 로직: 지급 가능 여부
    if count_before < counts_for_reward:
        return {
            "ok": False,
            "reason": "INSUFFICIENT_COUNT",
            "count_before": count_before,
            "threshold": counts_for_reward,
        }
    
    # 차감 로직
    remaining_to_consume = counts_for_reward
    activity_1_after, activity_2_after = activity_1_before, activity_2_before

    def consume(field_name: str):
        nonlocal remaining_to_consume, activity_1_after, activity_2_after
        if remaining_to_consume <= 0:
            return
        if field_name == "activity_2":
            take = min(activity_2_after, remaining_to_consume)
            activity_2_after -= take
            remaining_to_consume -= take
        elif field_name == "activity_1":
            take = min(activity_1_after, remaining_to_consume)
            activity_1_after -= take
            remaining_to_consume -= take

    for field in consume_order:
        consume(field)
        
    # after
    count_after = activity_1_after + activity_2_after
    points_after = points_before + points

    USER_data["activity_1"] = activity_1_after
    USER_data["activity_2"] = activity_2_after
    USER_data["total_points"] = points_after
    
    return {
        "ok": True,
        "activity_1_before": activity_1_before,
        "activity_2_before": activity_2_before,
        "activity_1_after": activity_1_after,
        "activity_2_after": activity_2_after,
        "count_before": count_before,
        "count_after": count_after,
        "points_before": points_before,
        "points_after": points_after,
        "points_delta": points,
        "counts_for_reward": counts_for_reward,
        "consume_order": list(consume_order),
    }

def check_reward_needed(total_counts, counts_for_reward=COUNTS_FOR_REWARD):
    """포인트 지급 필요 여부 확인 (예: 10회 기준)"""
    return total_counts >= counts_for_reward

def format_phone(phone: str) -> str:
    """전화번호 형식 변환 """
    if len(phone) == 11:
        return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone

def normalize_phone(phone) -> str:
    """
    전화번호 정규화
    - 어떤 타입이 와도 문자열로 변환 후 처리
    - 하이픈, 공백 등 제거
    - 숫자만 반환
    """
    return re.sub(r"\D", "", str(phone or ""))

def get_total_count(USER):
    return int(USER.get("activity_1", 0)) + int(USER.get("activity_2", 0))

def get_remaining(total_counts, count_for_reward=COUNTS_FOR_REWARD):
    remaining = (count_for_reward - (total_counts % count_for_reward)) % count_for_reward
    return remaining

def split_eligible(users, phones, counts_for_reward):
    """
    전달받은 사용자 목록을
    - 보상(리워드) 지급 '가능' 사용자
    - 보상 기준 '미달' 사용자
    두 그룹으로 분리한다.

    :param users: 사용자 데이터 dict
        예) {
            "01099857784": {"activity_1": 3, "activity_2": 7},
            ...
        }

    :param phones: 판별할 전화번호 리스트
        예) ["01099857784", "01012345678"]

    :param counts_for_reward: 보상 기준 횟수
        예) 10

    :return:
        eligible: 보상 지급 가능한 전화번호 리스트
        insufficient: (전화번호, 현재 누적 횟수) 튜플 리스트
    """
    eligible = []
    insufficient = []
    for phone in phones:
        cnt = get_total_count(users[phone])
        if cnt >= counts_for_reward:
            eligible.append(phone)
        else:
            insufficient.append((phone, cnt))
    return eligible, insufficient