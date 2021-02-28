import csv
from typing import TextIO, Union, AnyStr as PathLike, Literal


class CsvOpen:
    modes = Literal["r", "w", "a"]

    def __init__(self, file: Union[TextIO, PathLike], mode: modes):
        self.__mode = mode
        self.file = file

    def __enter__(self):
        if self.__mode == "r":
            if type(self.file) == TextIO:
                return csv.reader(self.file)
            else:
                return csv.reader(open(self.file, mode="r"))
        elif self.__mode == "w":
            if type(self.file) == TextIO:
                return csv.writer(self.file)
            else:
                return csv.writer(open(self.file, mode="w"))
        elif self.__mode == "w+":
            if type(self.file) == TextIO:
                return csv.writer(self.file)
            else:
                return csv.writer(open(self.file, mode="a"))
        else:
            msg = f"Invalid mode {self.__mode}," \
                  " it can be r - read," \
                  " w - write (clean file)," \
                  " a - write (do not clean file, cursor end)"
            raise ValueError(msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
