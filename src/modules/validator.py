# modules/validator.py
# 검증 로직

# --------------------------------------------------
# 1) 전화번호 검증
# --------------------------------------------------
def validate_phone(phone: str) -> bool:
    """
    전화번호 형식 검증
    - 01012345678
    - 010-1234-5678
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
    - 비어있지 않음
    - 숫자 문자열
    - 음수 불가
    - 너무 큰 수 제한 (ex: 1회 입력인데 999 입력하는 실수 방지)
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
    if not value or value.strip() == "":
        return False
    return True
