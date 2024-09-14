import importlib
import os
import platform
import sys
from pathlib import Path
from typing import Iterable

try:
    from .model import DeepObject
except ImportError:
    from model import DeepObject


def load_file(file: Path) -> list[type[DeepObject]]:
    classes: list[type[DeepObject]] = []
    try:
        module = importlib.import_module(str(file.absolute()))
    except ImportError:
        print(f"Invalid extension file at {file.absolute()}")
        sys.exit(1)
    for thing in dir(module):
        if issubclass(thing, DeepObject):
            classes.append(thing)
    return classes


def load_dir_recursive(dir: Path) -> list[type[DeepObject]]:
    classes: list[type[DeepObject]] = []
    for item in dir.iterdir():
        if item.is_file() and item.suffix == ".py":
            classes.extend(load_file(item))
        elif item.is_dir():
            classes.extend(load_dir_recursive(item))
    return classes


def load_extensions() -> list[type[DeepObject]]:
    classes: list[type[DeepObject]] = []
    str_paths = os.getenv("DEEPSEA_EXT_PATHS")
    if str_paths:
        paths: Iterable[Path] = map(Path, str_paths.split(":"))
    else:
        paths = []
    if platform.system() == "Linux":
        paths.append(Path(
            "~/.local/share/deepsea/extensions/").resolve().absolute())
    elif platform.system() == "Darwin":
        paths.append(Path(
            "~/Library/Application Support/deepsea/extensions/").resolve(
                ).absolute())
    elif platform.system() == "Windows":
        paths.append(Path(
            "%APPDATA%\\deepsea\\extensions\\").resolve().absolute())
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
        classes.extend((load_dir_recursive(path)))
    return classes
