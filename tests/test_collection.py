import pytest

from entities.player import Player


class TestPlayerCollection:
    @pytest.fixture
    def collection(self):
        from usecases.list_collections import PlayerCollection

        return PlayerCollection()

    def test_init_empty(self, collection):
        assert len(collection) == 0

    def test_append(self, collection, capsys):
        player = Player("Player", 100)
        collection.append(player)
        assert len(collection) == 1
        assert collection[0] == player
        captured = capsys.readouterr()
        assert "Добавлен" in captured.out

    def test_remove(self, collection, capsys):
        player = Player("Player", 100)
        collection.append(player)
        collection.remove(player)
        assert len(collection) == 0
        captured = capsys.readouterr()
        assert "Удалён" in captured.out

    def test_getitem(self, collection):
        player1 = Player("Player1", 100)
        player2 = Player("Player2", 50)
        collection.append(player1)
        collection.append(player2)
        assert collection[0] == player1
        assert collection[1] == player2

    def test_iter(self, collection):
        player1 = Player("Player1", 100)
        player2 = Player("Player2", 50)
        collection.append(player1)
        collection.append(player2)
        players = list(collection)
        assert len(players) == 2

    def test_len(self, collection):
        collection.append(Player("Player1", 100))
        collection.append(Player("Player2", 50))
        assert len(collection) == 2
