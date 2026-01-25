# modules/validator.py
# 검증 로직

# --------------------------------------------------
# 1) 전화번호 검증
# --------------------------------------------------
def validate_phone(phone: str) -> bool:
    """
    전화번호 형식 검증.

    Args:
        phone: 입력 전화번호.

    Returns:
        bool: 유효 여부.

    Side Effects:
        없음

    Raises:
        없음
    """
    if not phone:
        return False

    # '-'가 포함된 경우 제거
    cleaned = phone.replace("-", "")

    # 숫자만 / 10~11자리 허용
    if not cleaned.isdigit():
        return False

    if len(cleaned) not in (10, 11):
        return False

    # 선택적으로 01X 로 시작하는지 체크
    if not cleaned.startswith("01"):
        return False

    return True


# --------------------------------------------------
# 2) 숫자 입력 검증
# --------------------------------------------------
def validate_count(value: str) -> bool:
    """
    숫자 입력 검증.

    Args:
        value: 입력 문자열.

    Returns:
        bool: 유효 여부.

    Side Effects:
        없음

    Raises:
        없음
    """
    if not value:
        return False

    if not value.isdigit():
        return False

    number = int(value)

    if number < 0:
        return False

    if number > 50:  # saftey guard
        return False

    return True


# --------------------------------------------------
# 3) 공백/빈 문자열 검증
# --------------------------------------------------
def validate_not_empty(value: str) -> bool:
    """
    공백/빈 문자열 검증.

    Args:
        value: 입력 문자열.

    Returns:
        bool: 유효 여부.

    Side Effects:
        없음

    Raises:
        없음
    """
    if not value or value.strip() == "":
        return False
    return True

def valid_phone(phone: str) -> bool:
    """
    전화번호 유효성 검사(별칭).

    Args:
        phone: 입력 전화번호.

    Returns:
        bool: 유효 여부.

    Side Effects:
        없음

    Raises:
        없음
    """
    return validate_phone(phone)

def parse_int(value, default: int = 0) -> int:
    """
    안전하게 정수로 변환한다.

    Args:
        value: 변환할 값.
        default: 변환 실패 시 기본값.

    Returns:
        int: 변환된 정수.

    Side Effects:
        없음

    Raises:
        ValueError: 변환 실패 시.
    """
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("정수 변환 실패") from exc

def non_negative(value: int) -> bool:
    """
    음수 여부를 판단한다.

    Args:
        value: 검사할 값.

    Returns:
        bool: 0 이상 여부.

    Side Effects:
        없음

    Raises:
        없음
    """
    return value >= 0
