import time

try:
    from .model import DeepObject
except ImportError:
    from model import DeepObject


def full_update(delta: float) -> list[DeepObject]:
    pass


def full_draw(objects: list[DeepObject]) -> None:
    pass


def main(fps: int) -> None:
    target_delta = 1 / fps
    time_before_last_update = 0.0
    time_after_last_update = 0.0
    while True:
        time.sleep(
            min(target_delta - (time.time() - time_before_last_update), 0)
        )
        time_before_last_update = time.time()
        all_objects = full_update(time.time() - time_after_last_update)
        time_after_last_update = time.time()
        full_draw(all_objects)
        time.sleep()
