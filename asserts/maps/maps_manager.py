from typing import List, Tuple, Optional, Union

from pygame.math import Vector2

from asserts.sourse.csv_reader import CsvOpen

LEVELS = (
    "asserts/maps/level1.csv",
    "asserts/maps/level2.csv",
    "asserts/maps/level3.csv"
)

mapT = List[List[Union[int, float]]]


def load_csv(file_path) -> mapT:
    with CsvOpen(file_path, "r") as file:
        data = list(map(lambda e: list(map(int, e)), file))
    return data


def load_level(level: int) -> Optional[Tuple[Vector2, Vector2, mapT]]:
    str_l = f"asserts/maps/level{level}.csv"
    if str_l not in LEVELS:
        return None
    csv = load_csv(str_l)
    # noinspection PyTypeChecker
    info: Tuple[int, int, int, int] = tuple(csv[0])
    spawn = Vector2(float(info[0]), float(info[1]))
    win = Vector2(float(info[2]), float(info[3]))
    rest: mapT = csv[1:]
    return spawn, win, rest
