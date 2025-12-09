import pytest

from controllers.casino import Casino
from entities.errors import EntitiesError
from entities.goose import HonkGoose, WarGoose
from entities.player import Player


class TestCasino:
    @pytest.fixture
    def casino(self):
        return Casino()

    def test_init(self, casino):
        assert len(casino._player_collection) == 0
        assert len(casino._goose_collection) == 0

    def test_register_player(self, casino, capsys):
        player = Player("Player", 100)
        casino.register_player(player)
        assert len(casino._player_collection) == 1
        assert casino._players_balance["Player"].value == 100

    def test_register_goose(self, casino, capsys):
        goose = WarGoose("Wargoose", 50)
        casino.register_goose(goose)
        assert len(casino._goose_collection) == 1
        assert casino._geese_balance["Wargoose"].value == 0

    def test_iter(self, casino):
        player1 = Player("Player1", 100)
        player2 = Player("Player2", 50)
        casino.register_player(player1)
        casino.register_player(player2)
        players = list(casino)
        assert len(players) == 2

    def test_attack_no_players_raises_error(self, casino):
        goose = WarGoose("Wargoose", 50)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError, match="Нет игроков"):
            casino.attack()

    def test_attack_no_war_geese_raises_error(self, casino):
        player = Player("Player", 100)
        casino.register_player(player)
        goose = HonkGoose("Honkgoose", 50)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError, match="Нет гусей"):
            casino.attack()

    def test_attack_success(self, casino, capsys):
        player = Player("Player", 100)
        goose = WarGoose("Wargoose", 50)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(42)
        casino.attack()
        captured = capsys.readouterr()
        assert "[ATTACK]" in captured.out
        assert "атакует" in captured.out

    def test_honk_low_volume_damages_player(self, casino, capsys):
        player = Player("Player", 100)
        goose = HonkGoose("Honkgoose", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        casino.honk()
        assert len(casino._goose_collection) == 0
        captured = capsys.readouterr()
        assert "[HONK]" in captured.out

    def test_honk_high_volume_damages_goose(self, casino, capsys):
        player = Player("Player", 100)
        goose1 = HonkGoose("Honkgoose", 80)
        goose2 = WarGoose("Wargoose", 50)
        casino.register_player(player)
        casino.register_goose(goose1)
        casino.register_goose(goose2)
        casino.honk()
        assert len(casino._goose_collection) == 1

    def test_steal(self, casino, capsys):
        player = Player("Player", 100)
        goose = WarGoose("Wargoose", 50)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(42)
        casino.steal()
        captured = capsys.readouterr()
        assert "[STEAL]" in captured.out

    def test_bet_all_multipliers(self, casino, capsys):
        player = Player("Player", 100)
        casino.register_player(player)
        for _ in [0, 0.5, 1, 2, 3, 10]:
            casino._set_seed(42)
            casino.bet()
            captured = capsys.readouterr()
            assert "[BET]" in captured.out

    def test_sabotage_shuffles_balances(self, casino):
        player1 = Player("Player1", 100)
        player2 = Player("Player2", 50)
        goose1 = WarGoose("Wargoose1", 50)
        goose2 = WarGoose("Wargoose2", 50)
        casino.register_player(player1)
        casino.register_player(player2)
        casino.register_goose(goose1)
        casino.register_goose(goose2)

        casino._set_seed(42)
        casino.sabotage()

    def test_freebet(self, casino, capsys):
        player = Player("Player", 100)
        casino.register_player(player)
        initial = casino._players_balance["Player"].value
        casino.freebet()
        assert casino._players_balance["Player"].value == initial + 50

    def test_fruit_party(self, casino, capsys):
        player = Player("Player", 100)
        casino.register_player(player)
        casino.fruit_party()
        assert casino._players_balance["Player"].value == 0

    def test_flock_steal_zero_balance(self, casino, capsys):
        player = Player("Player", 0)
        goose = WarGoose("Wargoose", 50)
        casino.register_player(player)
        casino.register_goose(goose)
        casino.flock_steal()
        captured = capsys.readouterr()
        assert "нет фишек" in captured.out

    def test_flock_steal_success(self, casino):
        player = Player("Player", 100)
        goose1 = WarGoose("Wargoose1", 50)
        goose2 = WarGoose("Wargoose2", 50)
        casino.register_player(player)
        casino.register_goose(goose1)
        casino.register_goose(goose2)
        casino._set_seed(42)
        initial = casino._players_balance["Player"].value
        casino.flock_steal()
        assert casino._players_balance["Player"].value < initial

    def test_run_simulation_with_seed(self, casino, capsys):
        player = Player("Player", 100)
        goose = WarGoose("Wargoose", 50)
        casino.register_player(player)
        casino.register_goose(goose)
        casino.run_simulation(steps=5, seed=42)
        captured = capsys.readouterr()
        assert "Симуляция событий закончена" in captured.out

    def test_run_simulation_handles_errors(self, casino, capsys):
        casino.run_simulation(steps=3, seed=42)
        captured = capsys.readouterr()
        assert "Ошибка:" in captured.out
