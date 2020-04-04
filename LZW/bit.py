from enum import IntEnum


class Bit(IntEnum):
    ZERO = 0
    ONE = 1

    def __repr__(self) -> str:
        # Enum's default __repr__ can't ensure the invariant "eval(repr(x)) == x"
        # So we override its default __repr__ with __str__
        return str(self)
