"""
Базовые тесты игровой логики (без pygame-окна): боевые расчёты,
создание персонажа и переходы состояния партии.

Запуск (из папки game/):
    pytest tests/test_logic.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.combat import apply_damage, compute_attack, compute_heal
from logic.game_state import STATE_GAME_OVER, STATE_HUB, Game, stat_ru
from models.enemy import Enemy
from models.player import make_player


def test_make_player_applies_class_bonuses_and_health():
    p = make_player(0, "Тестовый Герой", "Воин")
    assert p.char_class == "Воин"
    assert p.stats["strength"] == 8 + 6       # база + бонус класса
    assert p.max_health == 100 + 30           # BASE_HEALTH + health_bonus Воина
    assert p.health == p.max_health


def test_compute_attack_returns_expected_shape():
    attacker = make_player(0, "Атакующий", "Воин")
    defender = Enemy("Тестовый враг", health=50, attack=5)

    result = compute_attack(attacker, defender, is_day=True)

    assert set(result.keys()) == {"dodged", "damage", "crit"}
    if not result["dodged"]:
        assert result["damage"] >= 1


def test_apply_damage_does_not_go_below_zero():
    target = Enemy("Цель", health=10, attack=1)
    apply_damage(target, 999)
    assert target.health == 0
    assert target.is_dead is True


def test_compute_heal_is_positive():
    healer = make_player(0, "Алхимик-тест", "Алхимик")
    assert compute_heal(healer) >= 1


def test_stat_ru_translates_known_keys_and_passes_through_unknown():
    assert stat_ru("strength") == "Сила"
    assert stat_ru("health") == "Здоровье"
    assert stat_ru(None) == ""
    assert stat_ru("unknown_key") == "unknown_key"


def test_game_check_game_over_on_single_survivor():
    g = Game()
    g.players = [make_player(0, "Игрок 1", "Воин"), make_player(1, "Игрок 2", "Лучник")]
    g.players[1].alive = False

    g.check_game_over()

    assert g.state == STATE_GAME_OVER
    assert g.winner is g.players[0]
    assert g.ending_type == "pvp"


def test_game_end_turn_moves_to_next_alive_player():
    g = Game()
    g.players = [make_player(0, "Игрок 1", "Воин"), make_player(1, "Игрок 2", "Лучник")]
    g.start_game()
    assert g.current_index == 0

    g.end_turn()

    assert g.current_index == 1
    assert g.state == STATE_HUB
