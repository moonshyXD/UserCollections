import random
import time
from collections.abc import Sequence
from typing import Iterator

from src.entities.chip import Chip
from src.entities.errors import EntitiesError
from src.entities.goose import Goose, HonkGoose, WarGoose
from src.entities.logger import Logger
from src.entities.player import Player
from src.usecases.dict_collection import CasinoBalance
from src.usecases.list_collections import (
    ChipCollection,
    GooseCollection,
    PlayerCollection,
)


class Casino:
    def __init__(self) -> None:
        """Инициализировать казино с пустыми коллекциями"""
        Logger.setup_logging()
        self._goose_collection = GooseCollection()
        self._players_balance = CasinoBalance()
        self._geese_balance = CasinoBalance()
        self._player_collection = PlayerCollection()
        self._chips_history = ChipCollection()

    def _set_seed(self, seed: int | None = None) -> None:
        """
        Установить seed для генератора случайных чисел
        :param seed: Значение seed или None для случайного поведения
        """
        if seed is not None:
            random.seed(seed)
            Logger.start_execution(f"Установлен seed: {seed}")

    def _check_players_collection(self, action: str) -> None:
        """
        Проверить наличие игроков в коллекции
        :param action: Название действия для сообщения об ошибке
        :raises EntitiesError: Если коллекция игроков пуста
        """
        if len(self._player_collection) == 0:
            raise EntitiesError(f"Нет игроков для события {action}")

    def _check_goose_collection(
        self, collection: Sequence[Goose] | GooseCollection, action: str
    ) -> None:
        """
        Проверить наличие гусей в коллекции
        :param collection: Коллекция гусей для проверки
        :param action: Название действия для сообщения об ошибке
        :raises EntitiesError: Если коллекция гусей пуста
        """
        if len(collection) == 0:
            raise EntitiesError(f"Нет гусей для события {action}")

    def register_goose(self, value: Goose) -> None:
        """
        Зарегистрировать гуся в казино
        :param value: Гусь для регистрации
        """
        self._goose_collection.append(value)
        self._geese_balance[value.name] = Chip(0)
        Logger.success_execution(f"Зарегистрирован гусь: {value.name}")

    def register_player(self, value: Player) -> None:
        """
        Зарегистрировать игрока в казино
        :param value: Игрок для регистрации
        """
        self._player_collection.append(value)
        self._players_balance[value.name] = value.balance
        Logger.success_execution(
            f"Зарегистрирован игрок {value.name} баланс: {value.balance.value}"
        )

    def __iter__(self) -> Iterator[Player]:
        """
        Получить итератор по игрокам казино
        :return: Итератор по коллекции игроков
        """
        return iter(self._player_collection)

    def attack(self) -> None:
        """
        Выполнить событие атаки военного гуся на игрока
        :raises EntitiesError: Если нет игроков или военных гусей
        """
        action = "[ATTACK]"
        Logger.event_start(action)

        war_geese = [
            g for g in self._goose_collection if isinstance(g, WarGoose)
        ]

        self._check_players_collection(action)
        self._check_goose_collection(war_geese, action)

        goose = random.choice(war_geese)
        player = random.choice(self._player_collection)
        damage = random.randint(1, 100)

        cur_chip = self._players_balance[player.name]
        old_balance = cur_chip.value
        new_value = max(0, old_balance - damage)
        damage_chip = Chip(damage)

        self._players_balance[player.name] = new_value
        Logger.balance_change(player.name, old_balance, new_value)

        self._chips_history.append(
            damage_chip, f"{goose.name} атаковал {player.name}"
        )
        Logger.chip_added(damage, f"{goose.name} атаковал {player.name}")

        print(f"{goose.name} атакует {player.name}! Урон: {damage}")

    def honk(self) -> None:
        """
        Выполнить событие крика гуся
        :raises EntitiesError: Если нет игроков или кричащих гусей
        """
        action = "[HONK]"
        Logger.event_start(action)

        honk_geese = [
            g for g in self._goose_collection if isinstance(g, HonkGoose)
        ]

        self._check_goose_collection(honk_geese, action)
        self._check_players_collection(action)

        goose = random.choice(honk_geese)
        honk_volume = goose.honk_volume
        stun_chip = Chip(10)

        if honk_volume <= 50:
            player = random.choice(self._player_collection)
            old_balance = self._players_balance[player.name].value
            new_balance = old_balance - 10

            self._players_balance[player.name] = new_balance
            Logger.balance_change(player.name, old_balance, new_balance)

            self._chips_history.append(
                stun_chip, f"{goose.name} оглушил {player.name}"
            )
            Logger.chip_added(10, f"{goose.name} оглушил {player.name}")

            print(f"Гусь кричит! {player.name} оглушился и потерял 10 фишек")
        else:
            random_goose = random.choice(self._goose_collection)
            old_balance = self._geese_balance[random_goose.name].value
            new_balance = old_balance - 10

            self._geese_balance[random_goose.name] = new_balance
            Logger.balance_change(random_goose.name, old_balance, new_balance)

            self._chips_history.append(
                stun_chip, f"{goose.name} оглушил {random_goose.name}"
            )
            Logger.chip_added(10, f"{goose.name} оглушил {random_goose.name}")

            print(f"Гусь кричит слишком громко! {random_goose.name} оглушён")
            print(f"Гусь {goose.name} сломал голос и выходит из игры")

            self._goose_collection.remove(goose)
            Logger.entity_removed(
                "Гусь", goose.name, f"Громкость: {goose.honk_volume}"
            )

    def steal(self) -> None:
        """
        Выполнить событие кражи фишек гусем у игрока
        :raises EntitiesError: Если нет игроков или гусей
        """
        action = "[STEAL]"
        Logger.event_start(action)

        self._check_players_collection(action)
        self._check_goose_collection(self._goose_collection, action)

        goose = random.choice(self._goose_collection)
        player = random.choice(self._player_collection)

        stolen = min(
            random.randint(1, 100), self._players_balance[player.name].value
        )
        stolen_chip = Chip(stolen)

        old_player = self._players_balance[player.name].value
        self._players_balance[player.name] = old_player - stolen
        Logger.balance_change(player.name, old_player, old_player - stolen)

        old_goose = self._geese_balance[goose.name].value
        self._geese_balance[goose.name] = old_goose + stolen
        Logger.balance_change(goose.name, old_goose, old_goose + stolen)

        self._chips_history.append(
            stolen_chip, f"{goose.name} украл у {player.name}"
        )
        Logger.chip_added(stolen, f"{goose.name} украл у {player.name}")

        print(f"{goose.name} крадёт у {player.name}! Украдено: {stolen}")

    def bet(self) -> None:
        """
        Выполнить событие ставки игрока в казино
        :raises EntitiesError: Если нет игроков
        """
        action = "[BET]"
        Logger.event_start(action)

        self._check_players_collection(action)

        player = random.choice(self._player_collection)
        casino_x = [0, 0.5, 1, 2, 3, 10]
        casino_procent = [30, 40, 10, 10, 5, 5]
        x = random.choices(casino_x, weights=casino_procent)[0]

        current_chip = self._players_balance[player.name]
        old_value = current_chip.value
        new_value = int(old_value * x)
        bet_chip = Chip(old_value)

        self._players_balance[player.name] = new_value
        Logger.balance_change(player.name, old_value, new_value)

        self._chips_history.append(bet_chip, f"Ставка {player.name} х{x}")
        Logger.chip_added(old_value, f"Ставка {player.name} х{x}")

        match x:
            case 0:
                print(f"{player.name} проиграл всё в казино! Множитель: х{x}")
            case 0.5:
                print(
                    f"{player.name} получил обидный проигрыш! Множитель: х{x}"
                )
            case 1:
                print(f"Ставка {player.name} не засчиталась! Множитель: х{x}")
            case 2:
                print(f"{player.name} победил! Множитель: х{x}")
            case 3:
                print(f"{player.name} получил крупную победу! Множитель: х{x}")
            case 10:
                print(f"{player.name} выиграл джекпот!!! Множитель: х{x}")

    def sabotage(self) -> None:
        """
        Выполнить событие саботажа с перемешиванием балансов
        :raises EntitiesError: Если нет игроков или гусей
        """
        action = "[SABOTAGE]"
        Logger.event_start(action)

        self._check_players_collection(action)
        self._check_goose_collection(self._goose_collection, action)

        players = self._player_collection
        player_balances = [self._players_balance[p.name] for p in players]
        random.shuffle(player_balances)

        for i in range(len(players)):
            old_balance = self._players_balance[players[i].name].value
            new_balance = player_balances[i].value
            self._players_balance[players[i].name] = player_balances[i]
            Logger.balance_change(players[i].name, old_balance, new_balance)

        geese = self._goose_collection
        goose_balances = [self._geese_balance[g.name] for g in geese]
        random.shuffle(goose_balances)

        for i in range(len(geese)):
            old_balance = self._geese_balance[geese[i].name].value
            new_balance = goose_balances[i].value
            self._geese_balance[geese[i].name] = goose_balances[i]
            Logger.balance_change(geese[i].name, old_balance, new_balance)

        print("Балансы игроков и гусей перемешаны!")

    def freebet(self) -> None:
        """
        Выполнить событие фрибета для случайного игрока
        :raises EntitiesError: Если нет игроков
        """
        action = "[FREEBET]"
        Logger.event_start(action)

        self._check_players_collection(action)

        player = random.choice(self._player_collection)
        old_balance = self._players_balance[player.name].value
        new_balance = old_balance + 50

        self._players_balance[player.name] = new_balance
        Logger.balance_change(player.name, old_balance, new_balance)

        freebet_chip = Chip(50)
        self._chips_history.append(freebet_chip, f"Фрибет для {player.name}")
        Logger.chip_added(50, f"Фрибет для {player.name}")

        print(f"{player.name} получил фрибет 50 фишек!")

    def fruit_party(self) -> None:
        """
        Выполнить событие проигрыша всех фишек в слоте Fruit Party
        :raises EntitiesError: Если нет игроков
        """
        action = "[FRUIT-PARTY]"
        Logger.event_start(action)

        self._check_players_collection(action)

        player = random.choice(self._player_collection)
        lost_chips = self._players_balance[player.name]
        old_balance = lost_chips.value

        self._players_balance[player.name] = 0
        Logger.balance_change(player.name, old_balance, 0)

        self._chips_history.append(
            lost_chips, f"{player.name} проиграл всё в Fruit Party"
        )
        Logger.chip_added(
            old_balance, f"{player.name} проиграл всё в Fruit Party"
        )

        print(f"{player.name} проиграл всё в слоте Fruit Party!")

    def flock_steal(self) -> None:
        """
        Выполнить событие кражи фишек стаей военных гусей
        :raises EntitiesError: Если нет игроков или военных гусей
        """
        action = "[FLOCK_STEAL]"
        Logger.event_start(action)

        war_geese = [
            g for g in self._goose_collection if isinstance(g, WarGoose)
        ]

        self._check_players_collection(action)
        self._check_goose_collection(war_geese, action)

        geese_count = random.randint(1, len(war_geese))
        player = random.choice(self._player_collection)
        player_chip = self._players_balance[player.name]

        if player_chip.value == 0:
            Logger.event_start(f"{action} - У игрока {player.name} нет фишек")
            print(f"У {player.name} нет фишек для кражи")
            return

        amount = random.randint(1, player_chip.value)
        stolen_chip = Chip(amount)

        old_balance = player_chip.value
        self._players_balance[player.name] = old_balance - amount
        Logger.balance_change(player.name, old_balance, old_balance - amount)

        self._chips_history.append(
            stolen_chip, f"Стая гусей украла у {player.name}"
        )
        Logger.chip_added(amount, f"Стая гусей украла у {player.name}")

        per_goose = amount // geese_count
        goose_share = Chip(per_goose)

        for _ in range(geese_count):
            goose = random.choice(war_geese)
            old_goose = self._geese_balance[goose.name].value
            new_goose = old_goose + per_goose

            self._geese_balance[goose.name] = new_goose
            Logger.balance_change(goose.name, old_goose, new_goose)

            self._chips_history.append(
                goose_share, f"Flock steal: {goose.name}"
            )
            Logger.chip_added(per_goose, f"Flock steal: {goose.name}")

        print(
            f"Стая из {geese_count} гусей украла",
            f"{amount} фишек у {player.name}!",
        )

    def bonus_rain(self) -> None:
        """
        Выполнить событие дождя бонусов для игроков
        :raises EntitiesError: Если нет игроков
        """
        action = "[BONUS-RAIN]"
        Logger.event_start(action)

        self._check_players_collection(action)

        lucky_count = random.randint(1, len(self._player_collection))
        lucky_players = random.sample(self._player_collection, lucky_count)

        print(f"Дождь бонусов! {lucky_count} игрок(ов) получат фишки!")

        for player in lucky_players:
            bonus_amount = random.randint(10, 100)
            bonus_chip = Chip(bonus_amount)

            old_balance = self._players_balance[player.name].value
            new_balance = old_balance + bonus_amount

            self._players_balance[player.name] = new_balance
            Logger.balance_change(player.name, old_balance, new_balance)

            self._chips_history.append(
                bonus_chip, f"Бонус дождь для {player.name}"
            )
            Logger.chip_added(bonus_amount, f"Бонус дождь для {player.name}")

            print(f"{player.name} получил {bonus_amount} фишек!")

    def run_simulation(self, steps: int = 20, seed: int | None = None) -> None:
        """
        Запустить симуляцию событий казино
        :param steps: Количество событий для симуляции
        :param seed: Seed для генератора случайных чисел или None
        """
        self._set_seed(seed)
        Logger.start_execution(f"Симуляция на {steps} шагов")

        actions = [
            self.attack,
            self.bet,
            self.honk,
            self.steal,
            self.sabotage,
            self.freebet,
            self.fruit_party,
            self.flock_steal,
            self.bonus_rain,
        ]

        for step in range(1, steps + 1):
            action = random.choice(actions)
            try:
                print(f"\nСобытие {step}/{steps}")
                action()
            except EntitiesError as e:
                Logger.failure_execution(e)
                print(f"Ошибка: {e}")

        random.seed(time.time())
        Logger.success_execution("Симуляция завершена")
