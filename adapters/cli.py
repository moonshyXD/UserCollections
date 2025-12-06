import questionary

from controllers.casino import Casino
from entities.errors import CasinoError
from entities.player import Player
from entities.goose import WarGoose, HonkGoose


class CLI:
    @staticmethod
    def hello():
        hello_text = """
Приветствуем вас в интерактивном казино с непредвиденными событиями!
Создайте игроков и гусей и запускайте свою уникальную симуляцию!
"""
        print(hello_text)
        questionary.press_any_key_to_continue("Нажмите Enter...").ask()
        CLI.run()

    @staticmethod
    def run():
        casino = Casino()
        choice: str = None
        while choice != "Выход":
            try:
                choice = questionary.select(
                    "Выберите действие:",
                    choices=[
                        "Запустить симуляцию",
                        "Добавить игрока",
                        "Добавить гуся",
                        "Выход",
                    ],
                ).ask()

                match choice:
                    case "Запустить симуляцию":
                        CLI.run_simulation(casino)
                    case "Добавить игрока":
                        CLI.add_player(casino)
                    case "Добавить гуся":
                        CLI.add_goose(casino)

                print(choice)
            except CasinoError as message:
                print(f"{type(message).__name__}: {message}")

    @staticmethod
    def add_player(casino: Casino):
        name = questionary.text("Имя игрока:").ask()
        balance = int(questionary.text("Баланс:", default="100").ask())
        player = Player(name, balance)
        casino.register_player(player)

    @staticmethod
    def add_goose(casino: Casino):
        goose_type = questionary.select(
            "Выберите тип гуся:", choices=["WarGoose", "HonkGoose"]
        ).ask()

        name = questionary.text("Имя гуся:").ask()
        volume = int(questionary.text("Громкость (1-100):", default="50").ask())

        if "War" in goose_type:
            goose = WarGoose(name, volume)
        else:
            goose = HonkGoose(name, volume)

        casino.register_goose(goose)

    @staticmethod
    def run_simulation(casino: Casino):
        steps = questionary.text(
            "Сколько событий будет в программе?", default="20"
        ).ask()
        seed_choice = questionary.select(
            "Хотите установить seed?", choices=["Да", "Нет"]
        ).ask()
        seed = None
        if seed_choice == "Да":
            seed = questionary.text(
                "Какой seed хотите установить?", default="None"
            ).ask()

        casino.run_simulation(steps, seed)
