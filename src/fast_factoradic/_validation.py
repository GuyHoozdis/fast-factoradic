def require_non_negative_int(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be non-negative")
    return value
