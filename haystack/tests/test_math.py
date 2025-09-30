def add(x: int, y: int) -> int:
    return x + y


def subtract(x: int, y: int) -> int:
    return x - y


def test_add() -> None:
    assert add(2, 2) == 4
    assert add(-2, 3) == 1


def test_subtract() -> None:
    assert subtract(10, 4) == 6
    assert subtract(2, 7) == -5
