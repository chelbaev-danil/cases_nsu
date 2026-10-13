"""Экран выбора цели для PvP-атаки (STATE_TARGET_SELECT)."""

from config import WIDTH
from logic.game_state import STATE_COMBAT, STATE_HUB
from models.player import Player
from ui.button import Button


class TargetSelectScreenMixin:
    def draw_target_select(self):
        p = self.game.current_player()
        self.draw_player_panel(p)
        self.blit_center(self.font_title, "Выберите цель для атаки", 20)
        y = 180
        for other in self.game.players:
            if other is p or not other.alive:
                continue
            rect = (WIDTH // 2 - 220, y, 440, 56)
            label = f"{other.name} ({other.char_class})  HP {other.health}/{other.max_health}"
            self.buttons.append(Button(rect, label, lambda o=other: self.start_pvp(o), color=other.color))
            y += 66
        self.buttons.append(Button((WIDTH // 2 - 100, y + 10, 200, 44), "Назад",
                                    lambda: self.goto(STATE_HUB)))

    def start_pvp(self, target: Player):
        if not self.game.use_action():
            return
        self.game.combat_pvp_target = target
        self.game.combat_enemy = None
        self.game.combat_quest = None
        self.game.combat_log = [f"Начинается схватка с {target.name}!"]
        self.game.state = STATE_COMBAT
