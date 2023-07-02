from Storage import Storage
from arithmetic_game import ArithmeticGame
from user_interface.console import ConsoleInterface

play = True
while play:
    arithmetic_game = ArithmeticGame(ConsoleInterface)
    delta_time, end_time = arithmetic_game.start()

    save_data = {"date": end_time, "time": delta_time,
                         "incorrect_answers": arithmetic_game.incorrect_answers}
    Storage(save_data).save_to_csv_file("stats.csv")
    print(save_data)
    play = input("is continue?")