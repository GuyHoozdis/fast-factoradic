import pytest
from hypothesis import given
from hypothesis import strategies as st

from fast_factoradic._validation import require_non_negative_int


def test_require_non_negative_int_returns_input_for_zero() -> None:
    assert require_non_negative_int(0) == 0


@given(st.integers(min_value=0))
def test_require_non_negative_int_round_trips_non_negative_values(value: int) -> None:
    assert require_non_negative_int(value) == value


def test_require_non_negative_int_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="value must be non-negative"):
        require_non_negative_int(-1)


def test_require_non_negative_int_rejects_non_integers() -> None:
    with pytest.raises(TypeError):
        require_non_negative_int(1.5)


def test_require_non_negative_int_rejects_boolean_values() -> None:
    with pytest.raises(TypeError):
        require_non_negative_int(True)
