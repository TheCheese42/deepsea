from functools import cache

try:
    from .custom_types import P
except ImportError:
    from custom_types import P


class DeepObject:
    def __init__(self, texture: str) -> None:
        self.texture = texture
        self.position = P(0, 0)

    @cache
    def calc_matrix(self) -> list[list[str]]:
        return [list(row) for row in self.texture.splitlines()]

    def update(self, delta: float) -> None:
        pass
