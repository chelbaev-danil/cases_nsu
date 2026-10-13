"""Класс Enemy: противник в бою (квестовый враг или финальный босс)."""

from dataclasses import dataclass, field


@dataclass
class Enemy:
    name: str
    health: int
    attack: int
    max_health: int = field(init=False)

    def __post_init__(self):
        self.max_health = self.health

    @property
    def is_dead(self) -> bool:
        return self.health <= 0
