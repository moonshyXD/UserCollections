from usecases.dict_collection import CasinoBalance
from usecases.list_collections import PlayerCollection, GooseCollection
from entities.goose import Goose, WarGoose, HonkGoose
from entities.player import Player

import random


class Casino:
    def __init__(self) -> None:
        self._goose_collection = GooseCollection()
        self._players_balance = CasinoBalance()
        self._geese_balance = CasinoBalance()
        self._player_collection = PlayerCollection()

    def register_entity(self, value: Goose | Player) -> None:
        if isinstance(value, Goose):
            self._goose_collection.append(value)
            self._geese_balance[value.name] = 0
        elif isinstance(value, Player):
            self._player_collection.append(value)
            self._players_balance[value.name] = value.balance

    def __iter__(self):
        return iter(self._player_collection)

    def attack(self):
        war_geese = [
            goose for goose in self._goose_collection if isinstance(goose, WarGoose)
        ]
        if len(war_geese) == 0:
            print("[ATTACK] Гусей для атаки нет")
            return
        elif len(self._player_collection) == 0:
            print("[ATTACK] Игроков для атаки нет")
            return

        goose = random.choice(war_geese)
        player = random.choice(self._player_collection.collection)
        damage = random.randint(1, 100)

        balance = max(0, self._players_balance[player.name] - damage)
        self._players_balance[player.name] = balance

        print(f"[ATTACK] {goose.name} атакует {player.name}! Урон: {damage}")

    def honk(self):
        honk_geese = [
            goose for goose in self._goose_collection if isinstance(goose, HonkGoose)
        ]
        if len(honk_geese) == 0:
            print("[HONK] Гусей для крика нет")
            return

        goose = random.choice(honk_geese)
        honk_volume = random.choice(1, 100)

        if honk_volume <= 50:
            print("[HONK] Гусь кричит! Вызвано событие [ATTACK]")
            self.attack()
        else:
            print("[HONK] Гусь кричит! Вызвано событие [STEAL]")
            self.steal()

        print(
            "[HONK] Гусь сломал свой голос! Он больше не может кричать и выходит из игры =("
        )
        self._goose_collection.remove(goose)

    def steal(self):
        goose = random.choice(self._goose_collection)
        player = random.choice(self._player_collection.collection)
        stolen = random.randint(1, 100)

        old_balance = self._players_balance[player.name]
        new_balance = max(0, old_balance - stolen)
        self._players_balance[player.name] = new_balance
        self._geese_balance[goose.name] += stolen

        print(f"[STEAL] {goose.name} крадет {player.name}! Украдено: {stolen}")

    def bet(self):
        if len(self._player_collection) == 0:
            print("[BET] нет игроков для ставки")
            return

        player = random.choice(self._player_collection.collection)
        casino_x = [0, 0.5, 1, 2, 3, 10]
        casino_procent = [30, 40, 10, 10, 5, 5]
        x = random.choices(casino_x, weights=casino_procent)[0]
        self._players_balance[player.name] *= x
        balance = self._players_balance[player.name]
        match x:
            case 0:
                print("[BET] Игрок проиграл хату в казино!", end=" ")
            case 0.5:
                print("[BET] Обидный проигрыш игрока!", end=" ")
            case 1:
                print("[BET] Ставка игрока не засчиталась!", end=" ")
            case 2:
                print("[BET] Победа игрока!", end=" ")
            case 5:
                print("[BET] Крупная победа игрока!", end=" ")
            case 10:
                print("[BET] Игрок выиграл у казино!!!", end=" ")

        print(f"Ему выпал х: {x}\nЕго баланс: {balance}")
