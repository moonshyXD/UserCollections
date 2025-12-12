from typing import Any

import pytest

from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.goose import HonkGoose, WarGoose
from src.entities.player import Player


class TestCasino:
    def test_init(self) -> None:
        """
        Проверяет создание пустого казино
        """
        casino = Casino()
        assert len(casino._player_collection) == 0
        assert len(casino._goose_collection) == 0

    def test_register_player(self) -> None:
        """
        Проверяет регистрацию игрока в казино
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        assert len(casino._player_collection) == 1
        assert casino._players_balance["PeterZhabin"].value == 100

    def test_register_goose(self) -> None:
        """
        Проверяет регистрацию гуся в казино
        """
        casino = Casino()
        goose = HonkGoose("PeterZhabin", 50)
        casino.register_goose(goose)
        assert len(casino._goose_collection) == 1
        assert casino._geese_balance["PeterZhabin"].value == 0

    def test_iter_players(self) -> None:
        """
        Проверяет итерацию по игрокам казино
        """
        casino = Casino()
        p1 = Player("PeterZhabin", 50)
        p2 = Player("SamirAhmed", 100)
        casino.register_player(p1)
        casino.register_player(p2)
        players = list(casino)
        assert players == [p1, p2]

    def test_set_seed(self) -> None:
        """
        Проверяет установку seed для генератора случайных чисел
        """
        casino = Casino()
        casino._set_seed(42)


class TestCasinoAttack:
    def test_attack_no_players_raises(self) -> None:
        """
        Проверяет ошибку при атаке без игроков
        """
        casino = Casino()
        goose = WarGoose("PeterZhabin", 30)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.attack()

    def test_attack_no_war_geese_raises(self) -> None:
        """
        Проверяет ошибку при атаке без боевых гусей
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 20)
        casino.register_player(player)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.attack()

    def test_attack_success(self, capsys: Any) -> None:
        """
        Проверяет успешную атаку
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        goose = WarGoose("SamirAhmed", 50)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(42)
        casino.attack()
        assert len(casino._chips_history) == 1
        assert casino._players_balance["PeterZhabin"].value <= 100


class TestCasinoHonk:
    def test_honk_no_geese_raises(self) -> None:
        """
        Проверяет ошибку при крике без гусей
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        with pytest.raises(EntitiesError):
            casino.honk()

    def test_honk_no_players_raises(self) -> None:
        """
        Проверяет ошибку при крике без игроков
        """
        casino = Casino()
        goose = HonkGoose("PeterZhabin", 30)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.honk()

    def test_honk_low_volume(self, capsys: Any) -> None:
        """
        Проверяет крик гуся с низкой громкостью
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 10)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(1)
        casino.honk()
        assert len(casino._chips_history) == 1

    def test_honk_high_volume(self, capsys: Any) -> None:
        """
        Проверяет крик гуся с высокой громкостью
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        g1 = HonkGoose("SamirAhmed1", 80)
        g2 = HonkGoose("SamirAhmed2", 20)
        casino.register_player(player)
        casino.register_goose(g1)
        casino.register_goose(g2)
        casino._set_seed(5)
        initial_count = len(casino._goose_collection)
        casino.honk()
        assert len(casino._goose_collection) <= initial_count


class TestCasinoSteal:
    def test_steal_no_players_raises(self) -> None:
        """
        Проверяет ошибку при краже без игроков
        """
        casino = Casino()
        goose = HonkGoose("PeterZhabin", 20)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.steal()

    def test_steal_no_geese_raises(self) -> None:
        """
        Проверяет ошибку при краже без гусей
        """
        casino = Casino()
        player = Player("SamirAhmed", 100)
        casino.register_player(player)
        with pytest.raises(EntitiesError):
            casino.steal()

    def test_steal_success(self, capsys: Any) -> None:
        """
        Проверяет успешную кражу фишек
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(5)
        casino.steal()
        assert len(casino._chips_history) == 1


class TestCasinoBet:
    def test_bet_no_players_raises(self) -> None:
        """
        Проверяет ошибку при ставке без игроков
        """
        casino = Casino()
        with pytest.raises(EntitiesError):
            casino.bet()

    def test_bet_success(self, capsys: Any) -> None:
        """
        Проверяет успешную ставку
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        casino._set_seed(10)
        casino.bet()
        assert len(casino._chips_history) == 1


class TestCasinoSabotage:
    def test_sabotage_no_players_raises(self) -> None:
        """
        Проверяет ошибку при саботаже без игроков
        """
        casino = Casino()
        goose = HonkGoose("SamirAhmed", 20)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.sabotage()

    def test_sabotage_no_geese_raises(self) -> None:
        """
        Проверяет ошибку при саботаже без гусей
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        with pytest.raises(EntitiesError):
            casino.sabotage()

    def test_sabotage_success(self, capsys: Any) -> None:
        """
        Проверяет успешный саботаж
        """
        casino = Casino()
        p1 = Player("PeterZhabin1", 100)
        p2 = Player("PeterZhabin2", 200)
        goose = HonkGoose("SamirAhmed", 30)
        casino.register_player(p1)
        casino.register_player(p2)
        casino.register_goose(goose)
        casino._set_seed(15)
        casino.sabotage()
        assert len(casino._player_collection) == 2


class TestCasinoFreeBet:
    def test_freebet_no_players_raises(self) -> None:
        """
        Проверяет ошибку при бесплатной ставке без игроков
        """
        casino = Casino()
        with pytest.raises(EntitiesError):
            casino.freebet()

    def test_freebet_success(self, capsys: Any) -> None:
        """
        Проверяет успешную бесплатную ставку
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        casino._set_seed(20)
        casino.freebet()
        assert casino._players_balance["PeterZhabin"].value == 150
        assert len(casino._chips_history) == 1


class TestCasinoFruitParty:
    def test_fruit_party_no_players_raises(self) -> None:
        """
        Проверяет ошибку при Fruit Party без игроков
        """
        casino = Casino()
        with pytest.raises(EntitiesError):
            casino.fruit_party()

    def test_fruit_party_success(self, capsys: Any) -> None:
        """
        Проверяет успешный Fruit Party
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        casino._set_seed(25)
        casino.fruit_party()
        assert casino._players_balance["PeterZhabin"].value == 0
        assert len(casino._chips_history) == 1


class TestCasinoFlockSteal:
    def test_flock_steal_no_players_raises(self) -> None:
        """
        Проверяет ошибку при краже стаей без игроков
        """
        casino = Casino()
        goose = WarGoose("PeterZhabin", 30)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.flock_steal()

    def test_flock_steal_no_war_geese_raises(self) -> None:
        """
        Проверяет ошибку при краже стаей без боевых гусей
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            casino.flock_steal()

    def test_flock_steal_success(self, capsys: Any) -> None:
        """
        Проверяет успешную кражу стаей
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        g1 = WarGoose("SamirAhmed1", 30)
        g2 = WarGoose("SamirAhmed2", 40)
        casino.register_player(player)
        casino.register_goose(g1)
        casino.register_goose(g2)
        casino._set_seed(30)
        casino.flock_steal()
        assert casino._players_balance["PeterZhabin"].value <= 100

    def test_flock_steal_player_has_zero_balance(self, capsys: Any) -> None:
        """
        Проверяет кражу стаей когда у игрока нет фишек
        """
        casino = Casino()
        player = Player("PeterZhabin", 0)
        goose = WarGoose("SamirAhmed", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(35)
        casino.flock_steal()
        assert casino._players_balance["PeterZhabin"].value == 0


class TestCasinoBonusRain:
    def test_bonus_rain_no_players_raises(self) -> None:
        """
        Проверяет ошибку при бонусном дожде без игроков
        """
        casino = Casino()
        with pytest.raises(EntitiesError):
            casino.bonus_rain()

    def test_bonus_rain_success(self, capsys: Any) -> None:
        """
        Проверяет успешный бонусный дождь
        """
        casino = Casino()
        p1 = Player("PeterZhabin", 100)
        p2 = Player("PeterZhabin2", 200)
        casino.register_player(p1)
        casino.register_player(p2)
        casino._set_seed(40)
        casino.bonus_rain()
        assert len(casino._chips_history) >= 1


class TestCasinoRunSimulation:
    def test_run_simulation_with_seed(self, capsys: Any) -> None:
        """
        Проверяет запуск симуляции с заданным seed
        """
        casino = Casino()
        p = Player("PeterZhabin", 100)
        g = WarGoose("SamirAhmed", 30)
        casino.register_player(p)
        casino.register_goose(g)
        casino.run_simulation(steps=3, seed=50)

    def test_run_simulation_without_seed(self, capsys: Any) -> None:
        """
        Проверяет запуск симуляции без seed
        """
        casino = Casino()
        p = Player("PeterZhabin", 100)
        g = HonkGoose("SamirAhmed", 30)
        casino.register_player(p)
        casino.register_goose(g)
        casino.run_simulation(steps=2)

    def test_run_simulation_handles_errors(self, capsys: Any) -> None:
        """
        Проверяет обработку ошибок в симуляции
        """
        casino = Casino()
        casino.run_simulation(steps=2, seed=60)
