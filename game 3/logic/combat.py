"""
Боевая система (вдохновлено Baldur's Gate 3: бросок на попадание + бросок урона).
Все функции — чистые расчёты: принимают участников боя (Player/Enemy) и
возвращают числа, ничего не рисуют и не меняют состояние игры напрямую
(кроме apply_damage, которая просто списывает здоровье цели).
"""

import random

from config import FATIGUE_DAMAGE_MULT
from models.player import Player


def roll_percentage() -> float:
    return random.uniform(0.01, 1.0)


def evasion_chance(defender, is_day: bool = True) -> float:
    base = getattr(defender, "stats", {}).get("agility", 0) if isinstance(defender, Player) else 5
    chance = min(0.35, base / 200)
    if isinstance(defender, Player) and defender.char_class == "Плут":
        chance += 0.15
    if not is_day:
        chance += 0.05  # ночью труднее разглядеть атаку
    return min(0.6, chance)


def crit_chance(attacker, is_day: bool = True) -> float:
    if not isinstance(attacker, Player):
        return 0.05
    c = attacker.stats.get("stealth", 0) / 150 + attacker.stats.get("agility", 0) / 300
    if attacker.char_class == "Лучник":
        c += 0.15
        if not is_day:
            c -= 0.05  # в темноте сложнее целиться дальнобойным оружием
    if not is_day and attacker.char_class in ("Плут",):
        c += 0.10  # ночь — стихия скрытных убийц
    elif not is_day:
        c += attacker.stats.get("stealth", 0) / 300
    return max(0.0, min(0.5, c))


def crit_mult(attacker) -> float:
    if isinstance(attacker, Player) and attacker.char_class == "Плут":
        return 1.75
    return 1.5


def damage_reduction(defender) -> float:
    if isinstance(defender, Player) and defender.char_class == "Воин":
        return 0.10
    return 0.0


def compute_attack(attacker, defender, is_day: bool = True) -> dict:
    """Считает один обмен ударом. attacker/defender: Player или Enemy."""
    if isinstance(attacker, Player):
        power = attacker.attack_power
    else:
        power = attacker.attack
        if not is_day:
            power *= 1.1  # чудовища опаснее ночью

    if random.random() < evasion_chance(defender, is_day):
        return {"dodged": True, "damage": 0, "crit": False}

    roll = roll_percentage()
    dmg = power * roll

    is_crit = random.random() < crit_chance(attacker, is_day)
    if is_crit:
        dmg *= crit_mult(attacker)

    if isinstance(attacker, Player) and attacker.is_exhausted:
        dmg *= FATIGUE_DAMAGE_MULT

    dmg *= (1.0 - damage_reduction(defender))
    dmg = max(1, round(dmg))
    return {"dodged": False, "damage": dmg, "crit": is_crit}


def compute_heal(player: Player) -> int:
    power = player.stats.get("magic_affinity", 0) or player.stats.get("intellect", 0)
    roll = roll_percentage()
    heal = power * roll
    if player.char_class == "Алхимик":
        heal *= 1.4
    return max(1, round(heal))


def apply_damage(target, dmg: int):
    target.health = max(0, target.health - dmg)
