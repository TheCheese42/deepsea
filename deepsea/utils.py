try:
    from .custom_types import P
except ImportError:
    from custom_types import P


def check_overlap(pos1: P, size1: P, pos2: P, size2: P) -> bool:
    x1, y1 = pos1.x, pos1.y
    x2, y2 = pos2.x, pos2.y
    w1, h1 = size1.x, size1.y
    w2, h2 = size2.x, size2.y

    return not (
        x1 >= x2 + w2 or x2 >= x1 + w1 or y1 >= y2 + h2 or y2 >= y1 + h1
    )
