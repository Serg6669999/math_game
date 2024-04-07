import csv
import re
from typing import List


class File:
    def __init__(self, path: str, file_name: str):
        self.path = path
        self.file_name = file_name

    def close(self):
        return file.close()

    def open(self):
        self.file = open(self.path + self.file_name, "r")
        return self.file

    def create(self, name: str, data: List[dict]):
        with open(self.path + name, "w", newline='') as file:
            field_names_list = data[0].keys()
            dict_writer = csv.DictWriter(file, field_names_list)
            dict_writer.writeheader()
            dict_writer.writerows(data)


class DataFileModify:
    def __init__(self, file):
        self.file = file

    def remove_transcriptions(self, text: str) -> str:
        return re.search(r"\w+", text).group()

    def _format_dict_value(self, dict: dict, func) -> dict:
        d = {}
        i = 1
        for k, v in dict.items():
            if i == 1:
                d[k] = v
            else:
                d[k] = func(v)
            i += 1
        return d

    def modify_data(self, fun) -> List[dict]:
        dict_reader = csv.DictReader(self.file, delimiter=',')
        result = [self._format_dict_value(data_dict, fun)
                  for data_dict in dict_reader]
        return result


path = "/media/serg/ostree/serg/Документы/книги/english/"
file_name = "verb.csv"
new_file_name = "without_transcriptions_verb.csv"

file = File(path=path, file_name=file_name).open()
data_file = DataFileModify(file=file)
new_data = data_file.modify_data(data_file.remove_transcriptions)
new_file = File(path, new_file_name).create(name=new_file_name, data=new_data)
file.close()