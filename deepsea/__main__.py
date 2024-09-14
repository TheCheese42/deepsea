#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

# Extensions have to import the script
sys.path.insert(0, str(Path(__file__).parent))

try:
    from .deepsea import Deepsea
except ImportError:
    from deepsea import Deepsea

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="deepsea",
        description="Fish inside your Terminal.",
    )

    parser.add_argument(
        "-f", "--fps",
        action="store",
        default=10,
        type=int,
        dest="fps",
        help="The FPS of the animation."
    )
    parser.add_argument(
        "-s", "--spawn-rate",
        action="store",
        default=1.0,
        type=float,
        dest="spawn_rate",
        help="How many common objects should spawn per second?",
    )
    parser.add_argument(
        "-C", "--no-color",
        action="store",
        default=False,
        type=bool,
        dest="no_color",
        help="Disable colored output.",
    )

    args = parser.parse_args()

    if not (1 <= args.fps <= 60):
        print("FPS should be between 1 and 60.")
        sys.exit(1)

    deepsea = Deepsea(
        fps=args.fps,
        spawn_rate=args.spawn_rate,
        colored=not args.no_color,
    )
    try:
        sys.exit(deepsea.run())
    except KeyboardInterrupt:
        sys.exit(0)
