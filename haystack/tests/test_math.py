def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y


def subtract(x: int, y: int) -> int:
    """Subtract two numbers."""
    return x - y


def test_add() -> None:
    """Test addition."""
    assert add(2, 2) == 4
    assert add(-2, 3) == 1


def test_subtract() -> None:
    """Test subtraction."""
    assert subtract(10, 4) == 6
    assert subtract(2, 7) == -5
