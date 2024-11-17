def validate_age(age: str) -> int | None:
    if not age.isdigit():
        return None
    return int(age)
