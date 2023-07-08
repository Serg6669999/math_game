import dataclasses

from Storage import Storage, StorageEntities
from arithmetic_game import ArithmeticGame
from user_interface.console import ConsoleInterface

play = True
while play:
    arithmetic_game = ArithmeticGame(ConsoleInterface)
    delta_time, end_time = arithmetic_game.start()

    storage_entities = StorageEntities(
        date=end_time,
        time=delta_time,
        incorrect_answers=arithmetic_game.incorrect_answers,
        arithmetic_data=(arithmetic_game.First_range_of_numbers,
                         arithmetic_game.Second_range_of_numbers)
       )
    Storage(storage_entities).save_to_csv_file("stats.csv")
    print(dataclasses.asdict(storage_entities))
    play = input("is continue?")