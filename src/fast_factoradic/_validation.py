"""Validation helpers for fast_factoradic inputs."""


def require_non_negative_int(value: int) -> int:
    """Return `value` when it is a non-negative integer.

    Args:
        value: Candidate integer input.

    Raises:
        TypeError: If `value` is not an integer or is a boolean.
        ValueError: If `value` is negative.

    Returns:
        The validated integer input.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be non-negative")
    return value
