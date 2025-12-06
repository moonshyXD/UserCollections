import questionary

from controllers.casino import Casino
from entities.errors import CasinoError


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
                        "Выход"
                    ]
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
        
        casino.register_player()

    @staticmethod
    def add_goose(casino: Casino):
        pass

    @staticmethod
    def run_simulation(casino: Casino):
        # ДОБАВИТЬ ВАЛИДАЦИЮ ТОЛЬКО ПОЛОЖИТЕЛЬНЫХ
        steps = questionary.text("Сколько событий будет в программе?", default="20").ask()
        seed_choice = questionary.select("Хотите установить seed?", choices=["Да", "Нет"]).ask()
        seed = None
        if seed_choice:
            seed = questionary.text("какой seed хотите установить?", default="None").ask()

        print(seed)
        casino.run_simulation(steps, seed)
