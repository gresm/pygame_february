from asserts.sourse.csv_reader import CsvOpen


def load_csv(file_path):
    with CsvOpen(file_path, "r") as file:
        data = list(map(lambda e: list(map(int, e)), file))
    return data
