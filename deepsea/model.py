from typing import Optional
from enum import Enum
import random

try:
    from .custom_types import P
except ImportError:
    from custom_types import P


REGULAR_MAX_Y = 8
REGULAR_MIN_Y_FROM_BOTTOM = 4


class DeepType(Enum):
    GENERIC = 0
    REGULAR = 1
    SELF_CONTROLLED = 2
    ABOVE_WATER = 3
    SPECIAL_EFFECT = 4
    STATIC_OBJECT = 5


class DeepObject:
    type = DeepType.GENERIC
    layer = 0

    def __init__(self, texture: str, terminal_size: P) -> None:
        self._texture = texture
        self._term_size = terminal_size
        self._precise_position = [0.0, 0.0]
        self._cached_matrix: Optional[list[list[str]]] = None

    @property
    def texture(self) -> str:
        return self._texture

    @texture.setter
    def texture(self, value: str) -> None:
        self._cached_matrix = None
        self._texture = value

    @property
    def size(self) -> P:
        m = self.calc_matrix()
        return P(len(m[0]), len(m))

    @property
    def position(self) -> P:
        return P(
            round(self._precise_position[0]),
            round(self._precise_position[1]),
        )

    def calc_matrix(self) -> list[list[str]]:
        """
        Calculate a 2D nested list of the current texture. Cached by default.

        :return: 2D list of the string texture.
        :rtype: list[list[str]]
        """
        if self._cached_matrix:
            return self._cached_matrix
        return [list(row) for row in self.texture.splitlines()]

    def get_hitbox(self) -> list[list[str]]:
        """
        Return the objects collision hitbox. By default, this is the texture
        matrix.

        :return: 2D of the object hitbox.
        :rtype: list[list[str]]
        """
        return self.calc_matrix()

    def get_hitbox_size(self) -> P:
        hb = self.get_hitbox()
        return P(len(hb[0]), len(hb))

    def update(self, delta: float) -> None:
        """
        Override to be called every frame. Delta should be used to make the
        animation FPS-independent.

        :param delta: Time between calls.
        :type delta: float
        """
        pass

    def on_collision(self, other: "DeepObject") -> None:
        """
        Override to add special collision handling.

        :param other: The DeepObject we collided with.
        :type other: DeepObject
        """
        pass


class RegularObject(DeepObject):
    type = DeepType.REGULAR
    layer = 1

    def __init__(self, texture: str, terminal_size: P) -> None:
        super().__init__(texture, terminal_size)
        if random.choice((0, 1)):
            self.position.x = -self.size.x
            self.speed = random.randint(3, 10)
        else:
            self.position.x = self._term_size
            self.speed = random.randint(-10, -3)
        self._precise_position[0] = random.randint(self.max_y, self.min_y)

    def update(self, delta: float) -> None:
        super().update(delta)
        self._precise_position[0] += self.speed * delta

    @property
    def max_y(self) -> int:
        return REGULAR_MAX_Y

    @property
    def min_y(self) -> int:
        return self._term_size.y - REGULAR_MIN_Y_FROM_BOTTOM - self.size.y
