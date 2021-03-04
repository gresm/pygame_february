from typing import List, Tuple

from asserts.sourse.csv_reader import CsvOpen

LEVELS = (
    "level1.csv",
    "level2.csv",
    "level3.csv"
)


def load_csv(file_path) -> List[List[int]]:
    with CsvOpen(file_path, "r") as file:
        data = list(map(lambda e: list(map(int, e)), file))
    return data


def load_level(level: int):
    str_l = f"level{level}.csv"
    if str_l not in LEVELS:
        return
    csv = load_csv(str_l)
    # noinspection PyTypeChecker
    info: Tuple[int, int, int, int] = tuple(csv[0])
    spawn = info[0], info[1]
    win = info[2], info[2]
    rest = csv[1:]
    return spawn, win, rest
