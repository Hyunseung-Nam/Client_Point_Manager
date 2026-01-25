# modules/calculator.py
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

COUNTS_FOR_REWARD = 10
LOYAL_VISITS_THRESHOLD = 5

def recalc_customer_fields(customer: dict) -> dict:
    """
    고객 데이터의 파생 필드를 재계산한다.

    Args:
        customer: 고객 데이터(dict). laundry/dry/total/points_remaining 등을 포함.

    Returns:
        dict: 재계산 결과가 반영된 고객 데이터.

    Side Effects:
        customer 딕셔너리의 필드를 갱신한다.

    Raises:
        ValueError: 숫자 필드 변환에 실패한 경우.
    """
    try:
        laundry = int(customer.get("laundry", 0))
        dry = int(customer.get("dry", 0))
        points_remaining = int(customer.get("points_remaining", 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("고객 데이터 숫자 필드 변환 실패") from exc

    total = laundry + dry
    customer["laundry"] = max(0, laundry)
    customer["dry"] = max(0, dry)
    customer["total"] = max(0, total)
    customer["points_remaining"] = max(0, points_remaining)
    customer["reward_needed"] = compute_reward_needed(customer["total"])
    if "month_count" not in customer:
        customer["month_count"] = 0
    return customer

def compute_reward_needed(total: int, threshold: int = COUNTS_FOR_REWARD) -> bool:
    """
    지급 필요 여부를 계산한다.

    Args:
        total: 누적 방문 총합.
        threshold: 지급 기준 횟수.

    Returns:
        bool: 지급 필요 여부.

    Side Effects:
        없음

    Raises:
        ValueError: total 또는 threshold가 음수인 경우.
    """
    if total < 0 or threshold < 0:
        raise ValueError("total/threshold는 음수가 될 수 없습니다.")
    return total >= threshold

def remaining_until_reward(total: int, threshold: int = COUNTS_FOR_REWARD) -> int:
    """
    지급까지 남은 횟수를 계산한다.

    Args:
        total: 누적 방문 총합.
        threshold: 지급 기준 횟수.

    Returns:
        int: 남은 횟수.

    Side Effects:
        없음

    Raises:
        ValueError: total 또는 threshold가 음수인 경우.
    """
    if total < 0 or threshold <= 0:
        raise ValueError("total/threshold는 음수가 될 수 없습니다.")
    remaining = (threshold - (total % threshold)) % threshold
    return remaining

def add_usage(users, phone, activity_1, activity_2):
    """
    사용자 데이터에 이용 횟수를 추가한다.

    Args:
        users: 사용자 데이터 dict.
        phone: 전화번호.
        activity_1: 활동 A 횟수.
        activity_2: 활동 B 횟수.

    Returns:
        None

    Side Effects:
        users 딕셔너리의 해당 사용자 레코드를 갱신한다.

    Raises:
        ValueError: activity 입력이 음수인 경우.
    """
    if activity_1 < 0 or activity_2 < 0:
        raise ValueError("활동 횟수는 음수일 수 없습니다.")
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
    """
    포인트 지급 필요 여부 확인.

    Args:
        total_counts: 누적 방문 총합.
        counts_for_reward: 지급 기준 횟수.

    Returns:
        bool: 지급 필요 여부.

    Side Effects:
        없음

    Raises:
        ValueError: total_counts 또는 counts_for_reward가 음수인 경우.
    """
    if total_counts < 0 or counts_for_reward < 0:
        raise ValueError("total_counts/counts_for_reward는 음수일 수 없습니다.")
    return total_counts >= counts_for_reward

def format_phone(phone: str) -> str:
    """
    전화번호를 표시용 형식으로 변환한다.

    Args:
        phone: 원본 전화번호 문자열.

    Returns:
        str: 하이픈 포함 형식.

    Side Effects:
        없음

    Raises:
        없음
    """
    if len(phone) == 11:
        return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone

def normalize_phone(phone) -> str:
    """
    전화번호 정규화 (숫자만 반환).

    Args:
        phone: 어떤 타입이든 허용.

    Returns:
        str: 숫자만 남긴 전화번호.

    Side Effects:
        없음

    Raises:
        없음
    """
    return re.sub(r"\D", "", str(phone or ""))

def get_total_count(USER):
    """
    activity_1/activity_2 합계를 반환한다.

    Args:
        USER: 사용자 데이터 dict.

    Returns:
        int: 합계.

    Side Effects:
        없음

    Raises:
        ValueError: 숫자 변환 실패 시.
    """
    try:
        return int(USER.get("activity_1", 0)) + int(USER.get("activity_2", 0))
    except (TypeError, ValueError) as exc:
        raise ValueError("activity 합계 계산 실패") from exc

def get_remaining(total_counts, count_for_reward=COUNTS_FOR_REWARD):
    """
    지급까지 남은 횟수를 계산한다.

    Args:
        total_counts: 누적 방문 총합.
        count_for_reward: 지급 기준 횟수.

    Returns:
        int: 남은 횟수.

    Side Effects:
        없음

    Raises:
        ValueError: total_counts 또는 count_for_reward가 음수인 경우.
    """
    if total_counts < 0 or count_for_reward <= 0:
        raise ValueError("total_counts/count_for_reward는 음수일 수 없습니다.")
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

def create_default_customer(phone: str, name: str = "", memo: str = "") -> dict:
    """
    기본 고객 레코드를 생성한다.

    Args:
        phone: 전화번호(숫자만).
        name: 고객 이름.
        memo: 메모.

    Returns:
        dict: 기본 고객 데이터.

    Side Effects:
        없음

    Raises:
        ValueError: phone이 비어있는 경우.
    """
    if not phone:
        raise ValueError("phone이 비어있습니다.")
    now = datetime.now().isoformat(timespec="seconds")
    return {
        "name": name or "신규 고객",
        "memo": memo or "",
        "created_at": now,
        "last_visit_at": "",
        "laundry": 0,
        "dry": 0,
        "total": 0,
        "points_remaining": 0,
        "reward_needed": False,
        "month_count": 0,
    }

def build_monthly_report(customers: dict, history: list, month_key: str) -> dict:
    """
    월 통계 요약을 계산한다.

    Args:
        customers: 고객 데이터 dict.
        history: 전체 로그 리스트.
        month_key: "YYYY-MM" 형식의 월 키.

    Returns:
        dict: 월 통계 요약 데이터.

    Side Effects:
        없음

    Raises:
        ValueError: month_key 형식이 잘못된 경우.
    """
    if not re.match(r"^\d{4}-\d{2}$", month_key or ""):
        raise ValueError("month_key 형식이 올바르지 않습니다.")

    stats = {
        "month_key": month_key,
        "total_visits": 0,
        "reward_granted": 0,
        "point_used": 0,
        "loyal_ratio": 0.0,
        "top5": [],
        "per_customer_visits": {},
    }

    per_customer_visits = {}
    for log in history:
        date = str(log.get("date", ""))
        if not date.startswith(month_key):
            continue
        log_type = log.get("type", "")
        phone = log.get("phone", "")
        if log_type in ("VISIT_LAUNDRY", "VISIT_DRY", "VISIT_BUNDLE"):
            count = int(log.get("count", 1))
            stats["total_visits"] += count
            per_customer_visits[phone] = per_customer_visits.get(phone, 0) + count
        elif log_type in ("REWARD_GRANTED", "MANUAL_GRANT"):
            stats["reward_granted"] += 1
        elif log_type == "POINT_USE":
            stats["point_used"] += 1

    loyal = 0
    visited_customers = len(per_customer_visits)
    for visit_count in per_customer_visits.values():
        if visit_count >= LOYAL_VISITS_THRESHOLD:
            loyal += 1
    stats["loyal_ratio"] = (loyal / visited_customers) if visited_customers else 0.0

    top_sorted = sorted(per_customer_visits.items(), key=lambda x: x[1], reverse=True)
    stats["top5"] = top_sorted[:5]
    stats["per_customer_visits"] = per_customer_visits

    return stats

def compare_month_over_month(customers: dict, history: list, month_key: str) -> dict:
    """
    전월 대비 증감을 계산한다.

    Args:
        customers: 고객 데이터 dict.
        history: 전체 로그 리스트.
        month_key: "YYYY-MM" 형식의 월 키.

    Returns:
        dict: 전월 대비 비교 데이터.

    Side Effects:
        없음

    Raises:
        ValueError: month_key 형식이 잘못된 경우.
    """
    if not re.match(r"^\d{4}-\d{2}$", month_key or ""):
        raise ValueError("month_key 형식이 올바르지 않습니다.")

    year, month = map(int, month_key.split("-"))
    if month == 1:
        prev_key = f"{year - 1}-12"
    else:
        prev_key = f"{year}-{month - 1:02d}"

    current = build_monthly_report(customers, history, month_key)
    previous = build_monthly_report(customers, history, prev_key)
    diff = {
        "total_visits": current["total_visits"] - previous["total_visits"],
        "reward_granted": current["reward_granted"] - previous["reward_granted"],
        "point_used": current["point_used"] - previous["point_used"],
        "loyal_ratio": current["loyal_ratio"] - previous["loyal_ratio"],
    }
    return {
        "current": current,
        "previous": previous,
        "diff": diff,
        "month_key": month_key,
        "prev_key": prev_key,
    }