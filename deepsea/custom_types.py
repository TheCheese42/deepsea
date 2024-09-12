from typing import Sequence, Union


class P:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Union[Sequence, "P"]) -> "P":
        if isinstance(other, P):
            return P(self.x + other.x, self.y + other.y)
        else:
            return P(self.x + other[0], self.y + other[1])
