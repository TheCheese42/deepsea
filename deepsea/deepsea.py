import os
import sys
import time

try:
    from .custom_types import P
    from .model import DeepObject
except ImportError:
    from custom_types import P
    from model import DeepObject


class Deepsea:
    def __init__(
        self,
        fps: int,
        spawn_rate: float,
        color: bool = True,
    ) -> None:
        self.reset()
        self.fps = fps

    def run(self) -> None:
        target_delta = 1 / self.fps
        time_before_last_update = 0.0
        time_after_last_update = 0.0
        while True:
            time.sleep(
                min(target_delta - (time.time() - time_before_last_update), 0)
            )
            time_before_last_update = time.time()
            all_objects = self.update(time.time() - time_after_last_update)
            time_after_last_update = time.time()
            self.draw(all_objects)
            time.sleep()

    def reset(self) -> None:
        self.terminal_size = self._fetch_term_size()
        self.objects: list[DeepObject] = []
        self.batch = ""

    @staticmethod
    def _fetch_term_size() -> P:
        t_size = os.get_terminal_size()
        return P(t_size.columns, t_size.lines)

    def update(self, delta: float) -> list[DeepObject]:
        new_term_size = self._fetch_term_size()
        if self.terminal_size != new_term_size:
            self.reset()
        for obj in self.objects:
            obj.update(delta)

    def prepare_batch(self) -> None:
        batch = [[" "] * self.terminal_size.x] * self.terminal_size.y
        for obj in sorted(self.objects, key=lambda x: x.layer):
            mt = obj.calc_matrix(self.terminal_size)  # matrix
            ul: P = obj.position  # upper-left
            width = len(mt[0])
            height = len(mt)
            lr = ul + (width, height)  # lower-right
            for i, row in enumerate(batch):
                if ul.y <= i <= lr.y:
                    texture_row = mt[ul.y - i]
                    row[ul.x:lr.x + 1] = texture_row
        self.batch = batch
        raw_rows = ["".join(row) for row in batch]
        self.raw_batch = "\n".join(raw_rows)

    def draw(self) -> None:
        sys.stdout.write("\r" * self.terminal_size.y + self.raw_batch)
        sys.stdout.flush()
