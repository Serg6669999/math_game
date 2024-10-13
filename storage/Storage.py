import os
import csv
import dataclasses
import datetime
from dataclasses import dataclass
from typing import List

from domen.entity import GameName


@dataclass
class GameStatsEntities:
    game_name: GameName
    level: int
    time: str
    incorrect_answers: int
    math_action: str
    date: str = None

    def __post_init__(self):
        self.date = datetime.datetime.now().strftime("%d-%m-%y %H:%M")

    @classmethod
    def get_field_names(cls) -> List[str]:
        fields = dataclasses.fields(cls)
        return [field.name for field in fields]


class Storage:
    def __init__(self, data: GameStatsEntities):
        self.data = data

    def save_to_csv_file(self, file_name: str):
        import csv
        with open(file_name, mode="a+", encoding='utf-8') as w_file:
            title = GameStatsEntities.get_field_names()
            file_writer = csv.DictWriter(w_file, delimiter=",",
                                         lineterminator="\r",
                                         fieldnames=title)
            file_writer.writerow(self.data.__dict__)
            # file_reader = csv.DictReader(w_file, fieldnames=title)


class File:
    def __init__(self, path: str, file_name: str):
        self.path = path
        self.file_name = file_name

    def open(self):
        self.file = open(self.path + self.file_name, "r")
        return self.file

    def read(self) -> List[dict]:
        return list(csv.DictReader(self.file))

    def close(self):
        return self.file.close()

    def create(self, name: str, data: List[dict]):
        with open(self.path + name, "w", newline='') as file:
            field_names_list = data[0].keys()
            dict_writer = csv.DictWriter(file, field_names_list)
            dict_writer.writeheader()
            dict_writer.writerows(data)


class FileP(File):
    def __init__(self, path_with_file_name: str):
        path, self.file_name = os.path.split(path_with_file_name)
        self.path = path + '/'
