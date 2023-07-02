class Storage:
    def __init__(self, data: dict):
        self.data = data

    def save_to_csv_file(self, file_name: str):
        import csv
        with open(file_name, mode="a+", encoding='utf-8') as w_file:
            title = ["date", "time", "incorrect_answers"]
            file_writer = csv.DictWriter(w_file, delimiter=",",
                                         lineterminator="\r", fieldnames=title)
            file_writer.writerow(self.data)
            # file_reader = csv.DictReader(r_file, fieldnames=title)