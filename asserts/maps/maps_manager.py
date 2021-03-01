from typing import List, Optional, Tuple

from asserts.sourse.csv_reader import CsvOpen

LEVELS = (
    "level1.csv",
    "level2.csv",
    "level3.csv"
)


def load_csv(file_path) -> Optional[List[List[int]]]:
    with CsvOpen(file_path, "r") as file:
        data = list(map(lambda e: list(map(int, e)), file))
    return data


def load_level(level: int):
    str_l = f"level{level}.csv"
    if str_l not in LEVELS:
        return
    csv = load_csv(str_l)
    # noinspection PyTypeChecker
    spawn: Tuple[int, int] = tuple(csv[0])
    rest = csv[1:]
    return spawn, rest
