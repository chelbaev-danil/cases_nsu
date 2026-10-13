"""
Состояние партии в целом: список игроков, чей сейчас ход, в каком королевстве
кто находится, лог событий и проверка условий окончания игры.
Экраны интерфейса (ui/screens/...) читают и меняют объект Game, но сами
правила здесь, в одном месте.
"""

from __future__ import annotations

from typing import Optional

from config import ACTIONS_PER_TURN, QUESTS, STATS
from models.player import Player

STATE_PLAYER_COUNT = "player_count"
STATE_SETUP = "setup"
STATE_HUB = "hub"
STATE_TRAIN = "train"
STATE_QUESTS = "quests"
STATE_TARGET_SELECT = "target_select"
STATE_COMBAT = "combat"
STATE_SHOP = "shop"
STATE_GAME_OVER = "game_over"


class Game:
    def __init__(self):
        self.players: list[Player] = []
        self.total_players: Optional[int] = None
        self.setup_index = 0
        self.setup_name = ""
        self.state = STATE_PLAYER_COUNT
        self.log: list[str] = []
        self.combat_enemy = None
        self.combat_quest: Optional[dict] = None
        self.combat_pvp_target: Optional[Player] = None
        self.combat_log: list[str] = []
        self.winner: Optional[Player] = None
        self.ending_type: Optional[str] = None
        self.round_counter = 0
        self.is_day = True
        self.current_index = 0
        self.actions_left = ACTIONS_PER_TURN

    # ------------------------------------------------------------------ #
    def current_player(self) -> Player:
        return self.players[self.current_index]

    def add_log(self, text: str):
        self.log.append(text)
        self.log = self.log[-6:]

    def alive_players(self) -> list[Player]:
        return [p for p in self.players if p.alive]

    def start_game(self):
        self.current_index = 0
        self._advance_to_alive()
        self.actions_left = ACTIONS_PER_TURN
        self.state = STATE_HUB

    def use_action(self) -> bool:
        """Тратит одно действие из лимита хода. False — действий не осталось."""
        if self.actions_left <= 0:
            return False
        self.actions_left -= 1
        return True

    def next_player(self) -> Player:
        idx = self.current_index
        for _ in range(len(self.players)):
            idx = (idx + 1) % len(self.players)
            if self.players[idx].alive:
                break
        return self.players[idx]

    def _advance_to_alive(self):
        if not self.alive_players():
            return
        tries = 0
        while not self.players[self.current_index].alive and tries < 8:
            self.current_index = (self.current_index + 1) % len(self.players)
            tries += 1

    def end_turn(self):
        p = self.current_player()
        msg = p.apply_end_of_turn() if p.alive else None
        if msg:
            self.add_log(msg)
        self.check_game_over()
        if self.state == STATE_GAME_OVER:
            return
        self.round_counter += 1
        if self.round_counter % len(self.players) == 0:
            self.is_day = not self.is_day
            self.add_log("Наступает ночь..." if not self.is_day else "Наступает новый день.")
        self.current_index = (self.current_index + 1) % len(self.players)
        self._advance_to_alive()
        self.actions_left = ACTIONS_PER_TURN
        self.state = STATE_HUB

    def quests_completed_in_kingdom(self, player: Player) -> int:
        kdata = QUESTS[player.kingdom]
        ids = {q["id"] for q in kdata["surface"] + kdata["dungeon"]}
        return len(player.completed_quests & ids)

    def can_advance_kingdom(self, player: Player) -> bool:
        # Упрощено: переход открыт всегда, ограничение только по ресурсам игрока.
        return player.kingdom < 3

    def advance_kingdom(self, player: Player):
        player.kingdom += 1
        self.add_log(f"{player.name} отправляется в «{QUESTS[player.kingdom]['название']}».")

    def apply_quest_reward(self, player: Player, quest: dict, chest: bool = False):
        gold = quest.get("reward_gold", 0)
        if gold:
            player.gold += gold
            self.add_log(f"{player.name} получает {gold} золота.")
        stat = quest.get("reward_stat")
        amount = quest.get("reward_amount", 0)
        if stat:
            if stat == "health":
                player.max_health += amount
                player.health = min(player.max_health, player.health + amount)
            else:
                player.stats[stat] = player.stats.get(stat, 0) + amount
            self.add_log(f"{player.name} получает +{amount} к «{stat_ru(stat)}».")
        if chest:
            cs, ca = quest.get("chest_stat"), quest.get("chest_amount", 0)
            if cs == "health":
                player.max_health += ca
                player.health = min(player.max_health, player.health + ca)
            else:
                player.stats[cs] = player.stats.get(cs, 0) + ca
            self.add_log(f"Сундук! {player.name} получает +{ca} к «{stat_ru(cs)}».")

    def check_game_over(self):
        alive = self.alive_players()
        if len(alive) <= 1 and len(self.players) > 1:
            self.state = STATE_GAME_OVER
            self.winner = alive[0] if alive else None
            self.ending_type = "pvp"
            return
        for p in self.players:
            if p.ending:
                self.state = STATE_GAME_OVER
                self.winner = p
                self.ending_type = p.ending
                return


def stat_ru(key: Optional[str]) -> str:
    if key is None:
        return ""
    mapping = dict(STATS)
    mapping.update({"health": "Здоровье"})
    return mapping.get(key, key)
