import questionary

from controllers.casino import Casino
from entities.errors import CasinoError
from entities.goose import Goose, HonkGoose, WarGoose
from entities.player import Player


class CLI:
    @staticmethod
    def hello() -> None:
        print(
            "Приветствуем вас в интерактивном казино с",
            "непредвиденными событиями!\nСоздайте игроков и гусей",
            " и запускайте свою уникальную симуляцию!",
        )
        questionary.press_any_key_to_continue("Нажмите Enter...").ask()
        CLI.run()

    @staticmethod
    def run() -> None:
        casino = Casino()
        while (
            choice := questionary.select(
                "Выберите действие:",
                choices=[
                    "Запустить симуляцию",
                    "Добавить игрока",
                    "Добавить гуся",
                    "Выход",
                ],
            ).ask()
        ) != "Выход":
            try:
                match choice:
                    case "Запустить симуляцию":
                        CLI.run_simulation(casino)
                    case "Добавить игрока":
                        CLI.add_player(casino)
                    case "Добавить гуся":
                        CLI.add_goose(casino)

            except CasinoError as message:
                print(f"{type(message).__name__}: {message}")

    @staticmethod
    def add_player(casino: Casino) -> None:
        name = questionary.text("Имя игрока:").ask()
        balance = int(questionary.text("Баланс:", default="100").ask())
        player = Player(name, balance)
        casino.register_player(player)

    @staticmethod
    def add_goose(casino: Casino) -> None:
        goose_type = questionary.select(
            "Выберите тип гуся:", choices=["WarGoose", "HonkGoose"]
        ).ask()

        name = questionary.text("Имя гуся:").ask()
        volume = int(
            questionary.text("Громкость (1-100):", default="50").ask()
        )

        goose: Goose
        if goose_type == "WarGoose":
            goose = WarGoose(name, volume)
        else:
            goose = HonkGoose(name, volume)

        casino.register_goose(goose)

    @staticmethod
    def run_simulation(casino: Casino) -> None:
        steps = questionary.text(
            "Сколько событий будет в программе?", default="20"
        ).ask()
        seed_choice = questionary.select(
            "Хотите установить seed?", choices=["Да", "Нет"]
        ).ask()

        seed: int | None = None
        if seed_choice == "Да":
            seed = questionary.text(
                "Какой seed хотите установить?", default="42"
            ).ask()

        casino.run_simulation(int(steps), seed)
