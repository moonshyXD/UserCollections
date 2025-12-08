import random
import time
from collections.abc import Sequence
from typing import Iterator

from entities.chip import Chip
from entities.errors import EntitiesError
from entities.goose import Goose, HonkGoose, WarGoose
from entities.player import Player
from usecases.dict_collection import CasinoBalance
from usecases.list_collections import GooseCollection, PlayerCollection


class Casino:
    def __init__(self) -> None:
        self._goose_collection = GooseCollection()
        self._players_balance = CasinoBalance()
        self._geese_balance = CasinoBalance()
        self._player_collection = PlayerCollection()

    def _set_seed(self, seed: int | None = None) -> None:
        if seed is not None:
            random.seed(seed)

    def _check_players_collection(self, action: str) -> None:
        if len(self._player_collection) == 0:
            raise EntitiesError(f"Нет игроков для события {action}")

    def _check_goose_collection(
        self, collection: Sequence[Goose] | GooseCollection, action: str
    ) -> None:
        if len(collection) == 0:
            raise EntitiesError(f"Нет гусей для события {action}")

    def register_goose(self, value: Goose) -> None:
        self._goose_collection.append(value)
        self._geese_balance[value.name] = Chip(0)

    def register_player(self, value: Player) -> None:
        self._player_collection.append(value)
        self._players_balance[value.name] = value.balance

    def __iter__(self) -> Iterator[Player]:
        return iter(self._player_collection)

    def attack(self) -> None:
        action = "[ATTACK]"
        print(f"Начинается событие {action}")
        war_geese = [
            g for g in self._goose_collection if isinstance(g, WarGoose)
        ]

        self._check_players_collection(action)
        self._check_goose_collection(war_geese, action)

        goose = random.choice(war_geese)
        player = random.choice(self._player_collection.collection)
        damage = random.randint(1, 100)

        cur_chip = self._players_balance[player.name]
        new_value = max(0, cur_chip.value - damage)
        self._players_balance[player.name] = Chip(new_value)

        print(f"[ATTACK] {goose.name} атакует {player.name}! Урон: {damage}")

    def honk(self) -> None:
        action = "[HONK]"
        print(f"Начинается событие {action}")
        honk_geese = [
            g for g in self._goose_collection if isinstance(g, HonkGoose)
        ]
        self._check_goose_collection(honk_geese, action)
        self._check_players_collection(action)

        goose = random.choice(honk_geese)
        honk_volume = goose.honk_volume

        if honk_volume <= 50:
            print(
                "[HONK] Гусь кричит!",
                "Случайный игрок оглушился и потерял 10 фишек",
            )
            player = random.choice(self._player_collection.collection)
            current = self._players_balance[player.name]
            self._players_balance[player.name] = current - 10
        else:
            print(
                "[HONK] Гусь кричит! Крик был слишком громким,",
                "он оглушил случайного гуся и тот потерял 10 фишек",
            )
            random_goose = random.choice(self._goose_collection.collection)
            current = self._geese_balance[random_goose.name]
            self._geese_balance[random_goose.name] = current - 10

        print(
            "[HONK] Гусь сломал свой голос!",
            "Он больше не может кричать и выходит из игры =(",
        )
        self._goose_collection.remove(goose)

    def steal(self) -> None:
        action = "[STEAL]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)
        self._check_goose_collection(self._goose_collection, action)

        goose = random.choice(self._goose_collection)
        player = random.choice(self._player_collection.collection)
        stolen = random.randint(1, 100)

        player_chip = self._players_balance[player.name]
        new_player_value = max(0, player_chip.value - stolen)
        self._players_balance[player.name] = Chip(new_player_value)

        goose_chip = self._geese_balance[goose.name]
        self._geese_balance[goose.name] = (
            goose_chip + player_chip - new_player_value
        )

        print(f"[STEAL] {goose.name} крадёт {player.name}! Украдено: {stolen}")

    def bet(self) -> None:
        action = "[BET]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)

        player = random.choice(self._player_collection.collection)
        casino_x = [0, 0.5, 1, 2, 3, 10]
        casino_procent = [30, 40, 10, 10, 5, 5]
        x = random.choices(casino_x, weights=casino_procent)[0]

        current_chip = self._players_balance[player.name]
        old_value = current_chip.value
        new_value = int(old_value * x)
        self._players_balance[player.name] = Chip(new_value)

        match x:
            case 0:
                print("[BET] Игрок проиграл хату в казино!", end=" ")
            case 0.5:
                print("[BET] Обидный проигрыш игрока!", end=" ")
            case 1:
                print("[BET] Ставка игрока не засчиталась!", end=" ")
            case 2:
                print("[BET] Победа игрока!", end=" ")
            case 3:
                print("[BET] Крупная победа игрока!", end=" ")
            case 10:
                print("[BET] Игрок выиграл у казино!!!", end=" ")

        print(f"Ему выпал х{x}")

    def sabotage(self) -> None:
        action = "[SABOTAGE]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)
        self._check_goose_collection(self._goose_collection, action)

        players = list(self._player_collection.collection)
        player_balances = [self._players_balance[p.name] for p in players]
        random.shuffle(player_balances)

        for i in range(len(players)):
            self._players_balance[players[i].name] = player_balances[i]

        geese = list(self._goose_collection.collection)
        goose_balances = [self._geese_balance[g.name] for g in geese]
        random.shuffle(goose_balances)

        for i in range(len(geese)):
            self._geese_balance[geese[i].name] = goose_balances[i]

        print(
            "[SABOTAGE] Событие прошло успешно!",
            "Балансы игроков и гусей были перемешаны друг с другом!",
        )

    def freebet(self) -> None:
        action = "[FREEBET]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)

        player = random.choice(self._player_collection.collection)
        current = self._players_balance[player.name]
        self._players_balance[player.name] = current + 50

        print(
            "[FREEBET] Случайный игрок берёт аккаунт",
            "своего друга и регистрирует фрибет для него",
        )

    def fruit_party(self) -> None:
        action = "[FRUIT-PARTY]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)

        player = random.choice(self._player_collection.collection)
        self._players_balance[player.name] = Chip(0)

        print(
            "[FRUIT-PARTY] Случайный игрок зашел в невезучий слот",
            "fruit-party и проиграл всё",
        )

    def flock_steal(self) -> None:
        action = "[FLOCK_STEAL]"
        print(f"Начинается событие {action}")
        war_geese = [
            g for g in self._goose_collection if isinstance(g, WarGoose)
        ]
        self._check_players_collection(action)
        self._check_goose_collection(war_geese, action)

        geese_count = random.randint(1, len(war_geese))
        player = random.choice(self._player_collection.collection)
        player_chip = self._players_balance[player.name]
        if player_chip.value == 0:
            print("[FLOCK_STEAL] У игрока нет фишек для кражи!")
            return
        amount = random.randint(1, player_chip.value)
        self._players_balance[player.name] = player_chip - amount

        per_goose = amount // geese_count
        for _ in range(geese_count):
            goose = random.choice(war_geese)
            current = self._geese_balance[goose.name]
            self._geese_balance[goose.name] = current + per_goose

        print(
            "[FLOCK-STEAL] Гуси собрались в стаю и украли у",
            "случайного игрока часть денег. Они распределили деньги",
            "игрока по целым частям, а остатки потеряли",
        )

    def run_simulation(self, steps: int = 20, seed: int | None = None) -> None:
        self._set_seed(seed)

        actions = [
            self.attack,
            self.bet,
            self.honk,
            self.steal,
            self.sabotage,
            self.freebet,
            self.fruit_party,
            self.flock_steal,
        ]
        for _ in range(steps):
            action = random.choice(actions)
            try:
                action()
                time.sleep(1)
            except EntitiesError as e:
                print(f"Ошибка: {e}")

        print("Симуляция событий закончена! Спасибо за игру!")
