import dataclasses
from dataclasses import dataclass
from typing import List


@dataclass
class StorageEntities:
    date: str = None
    time: str = None
    incorrect_answers: int = None
    arithmetic_data: tuple = None

    @classmethod
    def get_field_names(cls) -> List[str]:
        fields = dataclasses.fields(cls)
        return [field.name for field in fields]


class Storage:
    def __init__(self, data: StorageEntities):
        self.data = data

    def save_to_csv_file(self, file_name: str):
        import csv
        with open(file_name, mode="a+", encoding='utf-8') as w_file:
            title = StorageEntities.get_field_names()
            file_writer = csv.DictWriter(w_file, delimiter=",",
                                         lineterminator="\r",
                                         fieldnames=title)
            file_writer.writerow(self.data.__dict__)
            # file_reader = csv.DictReader(w_file, fieldnames=title)