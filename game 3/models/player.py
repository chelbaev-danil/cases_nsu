"""Класс Player: состояние персонажа (характеристики, здоровье, голод,
усталость, прогресс по квестам) и фабрика make_player для его создания."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from config import (
    ACTION_FATIGUE_GAIN,
    ACTION_HUNGER_COST,
    BASE_FATIGUE,
    BASE_HEALTH,
    BASE_HUNGER,
    BASE_STATS,
    CLASS_DATA,
    COLORS,
    FATIGUE_PENALTY_THRESHOLD,
    STARVATION_DAMAGE,
)


@dataclass
class Player:
    index: int
    name: str
    char_class: str
    stats: dict = field(default_factory=dict)
    health: int = BASE_HEALTH
    max_health: int = BASE_HEALTH
    hunger: int = BASE_HUNGER
    fatigue: int = BASE_FATIGUE
    gold: int = 15
    kingdom: int = 1
    completed_quests: set = field(default_factory=set)
    purchased_items: set = field(default_factory=set)
    alive: bool = True
    ending: Optional[str] = None  # "hero" | "pvp"

    @property
    def color(self):
        return COLORS["player"][self.index % 4]

    @property
    def privilege(self) -> str:
        return CLASS_DATA[self.char_class]["privilege"]

    @property
    def attack_weights(self) -> dict:
        return CLASS_DATA[self.char_class]["attack_weights"]

    @property
    def attack_power(self) -> float:
        """Сила атаки — взвешенная сумма реальных, текущих характеристик
        персонажа (см. attack_weights в CLASS_DATA), а не одно случайное
        или фиксированное число."""
        return sum(self.stats.get(stat, 0) * w for stat, w in self.attack_weights.items())

    @property
    def is_starving(self) -> bool:
        return self.hunger <= 0

    @property
    def is_exhausted(self) -> bool:
        return self.fatigue >= FATIGUE_PENALTY_THRESHOLD

    def spend_action(self):
        self.hunger = max(0, self.hunger - ACTION_HUNGER_COST)
        self.fatigue = min(100, self.fatigue + ACTION_FATIGUE_GAIN)

    def rest(self):
        self.hunger = min(BASE_HUNGER, self.hunger + 30)
        self.fatigue = max(0, self.fatigue - 20)

    def apply_end_of_turn(self) -> Optional[str]:
        """Возвращает строку лога, если что-то произошло (голод и т.п.)."""
        if self.is_starving:
            self.health = max(0, self.health - STARVATION_DAMAGE)
            if self.health <= 0:
                self.alive = False
                return f"{self.name} умирает от голода!"
            return f"{self.name} страдает от голода (-{STARVATION_DAMAGE} HP)."
        return None


def make_player(index: int, name: str, char_class: str) -> Player:
    data = CLASS_DATA[char_class]
    stats = dict(BASE_STATS)
    for k, v in data["bonus"].items():
        stats[k] = stats.get(k, 0) + v
    max_hp = BASE_HEALTH + data["health_bonus"]
    return Player(
        index=index, name=name, char_class=char_class, stats=stats,
        health=max_hp, max_health=max_hp,
    )
