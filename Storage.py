import dataclasses
from dataclasses import dataclass


@dataclass
class StorageEntities:
    date: str = None
    time: str = None
    incorrect_answers: int = None
    arithmetic_data: tuple = None


class Storage:
    def __init__(self, data: StorageEntities):
        self.data = data

    def save_to_csv_file(self, file_name: str):
        import csv
        with open(file_name, mode="a+", encoding='utf-8') as w_file:
            fields = dataclasses.fields(self.data)
            title = [field.name for field in fields]
            file_writer = csv.DictWriter(w_file, delimiter=",",
                                         lineterminator="\r", fieldnames=title)
            file_writer.writerow(dataclasses.asdict(self.data))
            # file_reader = csv.DictReader(w_file, fieldnames=title)