from typing import Optional

try:
    from .custom_types import P
except ImportError:
    from custom_types import P


class DeepObject:
    def __init__(self, texture: str) -> None:
        self._texture = texture
        self.position = P(0, 0)
        self._cached_matrix: Optional[list[list[str]]] = None

    @property
    def texture(self) -> str:
        return self._texture

    @texture.setter
    def texture(self, value: str) -> None:
        self._cached_matrix = None
        self._texture = value

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
