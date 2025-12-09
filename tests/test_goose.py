import pytest

from entities.goose import Goose, HonkGoose, WarGoose


class TestGoose:
    def test_cannot_instantiate_abstract_goose(self):
        with pytest.raises(TypeError):
            Goose("Гусь", 50)

    def test_war_goose_init(self):
        goose = WarGoose("Wargoose", 80)
        assert goose.name == "Wargoose"
        assert goose.honk_volume == 80

    def test_war_goose_execute(self):
        goose = WarGoose("Wargoose", 80)
        assert goose.execute() == "Wargoose атакует! Атака: 80"

    def test_war_goose_repr(self):
        goose = WarGoose("Wargoose", 80)
        assert repr(goose) == "Гусь(имя=Wargoose, громкость=80)"

    def test_honk_goose_init(self):
        goose = HonkGoose("Honkgoose", 30)
        assert goose.name == "Honkgoose"
        assert goose.honk_volume == 30

    def test_honk_goose_execute(self):
        goose = HonkGoose("Honkgoose", 30)
        assert goose.execute() == "Honkgoose кричит! Громкость: 30"
