from usecases.dict_collection import CasinoBalance
from usecases.list_collections import PlayerCollection, GooseCollection
from entities.goose import Goose, WarGoose, HonkGoose
from entities.player import Player
from entities.chip import Chip
from entities.errors import EntitiesError

import random


class Casino:
    def __init__(self) -> None:
        self._goose_collection = GooseCollection()
        self._players_balance = CasinoBalance()
        self._geese_balance = CasinoBalance()
        self._player_collection = PlayerCollection()

    def _set_seed(self, seed: int | None = None):
        if seed is not None:
            random.seed(seed)

    def _check_players_collection(self, action: str):
        if len(self._player_collection) == 0:
            raise EntitiesError(f"Нет игроков для события {action}")

    def _check_goose_collection(
        self, collection: list[Goose] | GooseCollection, action: str
    ):
        if len(collection) == 0:
            raise EntitiesError(f"Нет игроков для события {action}")

    def register_goose(self, value: Goose) -> None:
        self._goose_collection.append(value)
        self._geese_balance[value.name] = 0

    def register_player(self, value: Player) -> None:
        self._player_collection.append(value)
        self._players_balance[value.name] = value.balance

    def __iter__(self):
        return iter(self._player_collection)

    def attack(self, seed: int | None = None):
        action = "[ATTACK]"
        print(f"Начинается событие {action}")
        war_geese = [
            goose for goose in self._goose_collection if isinstance(goose, WarGoose)
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

    def honk(self, seed: int | None = None):
        action = "[HONK]"
        print(f"Начинается событие {action}")
        honk_geese = [
            goose for goose in self._goose_collection if isinstance(goose, HonkGoose)
        ]
        self._check_goose_collection(honk_geese, action)

        goose = random.choice(honk_geese)
        honk_volume = random.randint(1, 100) # БРАТЬ ГРОМКОСТЬ ИЗ ГУСЯ

        if honk_volume <= 50:
            print("[HONK] Гусь кричит! Случайный игрок оглушился и потерял 10 фишек")
            player = random.choice(self._player_collection.collection)
            self._player_collection[player.name] -= 10
        else:
            print(
                "[HONK] Гусь кричит! Крик был слишком громким, он оглушил случайного гуся и тот потерял 10 фишек"
            )
            random_goose = random.choice(self._goose_collection.collection)
            self._geese_balance[random_goose.name] -= 10

        print(
            "[HONK] Гусь сломал свой голос! Он больше не может кричать и выходит из игры =("
        )
        self._goose_collection.remove(goose)

    def steal(self, seed: int | None = None):
        action = "[STEAL]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)
        self._check_goose_collection(self._check_goose_collection, action)

        goose = random.choice(self._goose_collection)
        player = random.choice(self._player_collection.collection)
        stolen = random.randint(1, 100)

        player_chip = self._players_balance[player.name]
        new_player_value = max(0, player_chip.value - stolen)
        self._players_balance[player.name] = Chip(new_player_value)

        goose_chip = self._geese_balance[goose.name]
        self._geese_balance[goose.name] = goose_chip + stolen

        print(f"[STEAL] {goose.name} крадет {player.name}! Украдено: {stolen}")

    def bet(self, seed: int | None = None):
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

        print(f"Ему выпал х{x}\nБаланс: {old_value} → {new_value}")

    def sabotage(self, seed: int | None = None):
        action = "[SABOTAGE]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)
        self._check_goose_collection(self._goose_collection, action)

        for player in self._player_collection.collection:
            switched_player = random.choice(
                self._player_collection.collection
            )
            (
                self._players_balance[player.name],
                self._players_balance[switched_player.name],
            ) = (
                self._players_balance[switched_player.name],
                self._players_balance[player.name],
            )

        for goose in self._goose_collection.collection:
            switched_goose = random.choice(self._goose_collection.collection)
            (
                self._geese_balance[goose.name],
                self._geese_balance[switched_goose.name],
            ) = (
                self._geese_balance[switched_goose.name],
                self._geese_balance[goose.name],
            )

        print(
            "[SABOTAGE] Событие прошло успешно! Балансы игроков и гусей были перемешаны друг с другом!"
        )

    def freebet(self, seed: int | None = None):
        action = "[FREEBET]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)

        player = random.choice(self._player_collection.collection)
        self._players_balance[player.name] += 50

        print(
            "[FREEBET] Случайный игрок берёт аккаунт своего друга и регистрирует фрибет для него"
        )

    def fruit_party(self, seed: int | None = None):
        action = "[FRUIT-PARTY]"
        print(f"Начинается событие {action}")
        self._check_players_collection(action)

        player = random.choice(self._player_collection.collection)
        self._players_balance[player.name] = 0

        print(
            "[FRUIT-PARTY] Случайный игрок зашел в невезучий слот fruit-party и проиграл всё"
        )

    def flock_steal(self, seed: int | None = None):
        action = "[FLOCK_STEAL]"
        print(f"Начинается событие {action}")
        war_geese = [
            goose for goose in self._goose_collection if isinstance(goose, WarGoose)
        ]
        self._check_players_collection(action)
        self._check_goose_collection(war_geese, action)

        geese_count = random.randint(1, len(war_geese))
        player = random.choice(self._player_collection.collection)
        old_balance = self._players_balance[player.name]
        amount = random.randint(1, old_balance)
        new_balance = old_balance - amount
        self._players_balance[player.name] = new_balance
        for _ in range(geese_count):
            goose = random.choice(war_geese)
            self._geese_balance[goose] += int(amount / geese_count)

        print(
            "[FLOCK-STEAL] Гуси собрались в стаю и украли у случайного игрока часть денег. Они распределили деньги игрока по целым частям, а остатки потеряли"
        )

    def run_simulation(self, steps: int = 20, seed: int | None = None):
        self._set_seed(seed)

        actions = {
            1: self.attack(seed),
            2: self.bet(seed),
            3: self.honk(seed),
            4: self.steal(seed),
            5: self.sabotage(seed),
            6: self.freebet(seed),
            7: self.fruit_party(seed),
            8: self.flock_steal(seed),
        }
        for _ in range(steps):
            action = random.randint(1, 7)
            actions[action]

        print("Симуляция событий закончена! Спасибо за игру!")
