import questionary

from src.controllers.casino import Casino
from src.entities.errors import CasinoError
from src.entities.goose import Goose, HonkGoose, WarGoose
from src.entities.player import Player


class CLI:
    @staticmethod
    def hello() -> None:
        print(
            "Приветствуем вас в интерактивном казино с",
            "непредвиденными событиями!\nСоздайте игроков и гусей",
            "и запускайте свою уникальную симуляцию!",
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
                    "Удалить игрока",
                    "Удалить гуся",
                    "Очистить коллекции",
                    "Посмотреть коллекцию",
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
                    case "Удалить игрока":
                        CLI.remove_player(casino)
                    case "Удалить гуся":
                        CLI.remove_goose(casino)
                    case "Очистить коллекции":
                        CLI.clear_collections(casino)
                    case "Посмотреть коллекцию":
                        CLI.get_collection(casino)
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
    def remove_player(casino: Casino) -> None:
        if len(casino._player_collection) == 0:
            print("Нет игроков для удаления!")
            return

        players = [p.name for p in casino._player_collection]
        player_name = questionary.select(
            "Выберите игрока для удаления:", choices=players
        ).ask()

        for player in casino._player_collection:
            if player.name == player_name:
                casino._player_collection.remove(player)
                del casino._players_balance._balance[player_name]
                print(f"Игрок {player_name} удален!")
                break

    @staticmethod
    def remove_goose(casino: Casino) -> None:
        if len(casino._goose_collection) == 0:
            print("Нет гусей для удаления!")
            return

        geese = [g.name for g in casino._goose_collection]
        goose_name = questionary.select(
            "Выберите гуся для удаления:", choices=geese
        ).ask()

        for goose in casino._goose_collection:
            if goose.name == goose_name:
                casino._goose_collection.remove(goose)
                del casino._geese_balance._balance[goose_name]
                print(f"Гусь {goose_name} удален!")
                break

    @staticmethod
    def clear_collections(casino: Casino) -> None:
        clear_choice = questionary.select(
            "Что вы хотите очистить?",
            choices=[
                "Всё",
                "Только игроков",
                "Только гусей",
                "Историю фишек",
            ],
        ).ask()

        match clear_choice:
            case "Всё":
                casino._player_collection._collection.clear()
                casino._goose_collection._collection.clear()
                casino._players_balance._balance.clear()
                casino._geese_balance._balance.clear()
                casino._chips_history._collection.clear()
                print("Все коллекции очищены!")
            case "Только игроков":
                casino._player_collection._collection.clear()
                casino._players_balance._balance.clear()
                print("Коллекция игроков очищена!")
            case "Только гусей":
                casino._goose_collection._collection.clear()
                casino._geese_balance._balance.clear()
                print("Коллекция гусей очищена!")
            case "Историю фишек":
                casino._chips_history._collection.clear()
                print("История фишек очищена!")

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
            seed = int(
                questionary.text(
                    "Какой seed хотите установить?", default="42"
                ).ask()
            )

        casino.run_simulation(int(steps), seed)

    @staticmethod
    def get_collection(casino: Casino) -> None:
        collection = questionary.select(
            "Какую коллекцию вы хотите выбрать?",
            choices=["Списковая", "Словарная"],
        ).ask()

        if collection == "Списковая":
            list_collection = questionary.select(
                "Какую списковую коллекцию вы хотите выбрать?",
                choices=[
                    "Коллекция игроков",
                    "Коллекция гусей",
                    "Коллекция фишек",
                ],
            ).ask()

            match list_collection:
                case "Коллекция игроков":
                    for index, player in enumerate(casino._player_collection):
                        print(f"{index + 1}: {player}")
                case "Коллекция гусей":
                    for index, goose in enumerate(casino._goose_collection):
                        print(f"{index + 1}: {goose}")
                case "Коллекция фишек":
                    for index, transaction in enumerate(casino._chips_history):
                        print(f"{index + 1}: {transaction}")
        else:
            dict_collection = questionary.select(
                "Какую словарную коллекцию вы хотите выбрать?",
                choices=["Балансы игроков", "Балансы гусей"],
            ).ask()

            match dict_collection:
                case "Балансы игроков":
                    for name, balance in casino._players_balance:
                        print(f"{name}: {balance}")
                case "Балансы гусей":
                    for name, balance in casino._geese_balance:
                        print(f"{name}: {balance}")
