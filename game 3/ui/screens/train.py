"""Экран тренировки характеристик (STATE_TRAIN)."""

import random

from config import STATS, WIDTH
from logic.game_state import STATE_HUB, stat_ru
from ui.button import Button


class TrainScreenMixin:
    def draw_train(self):
        p = self.game.current_player()
        self.draw_player_panel(p)
        self.blit_center(self.font_title, "Выберите характеристику для тренировки", 20)
        y = 160
        for key, label in STATS:
            rect = (WIDTH // 2 - 220, y, 440, 50)
            cur = p.stats.get(key, 0)
            self.buttons.append(Button(rect, f"{label}  (сейчас {cur})",
                                        lambda k=key: self.do_train(k)))
            y += 60
        self.buttons.append(Button((WIDTH // 2 - 100, y + 10, 200, 44), "Назад",
                                    lambda: self.goto(STATE_HUB)))

    def do_train(self, stat_key: str):
        if not self.game.use_action():
            self.game.state = STATE_HUB
            return
        p = self.game.current_player()
        gain = random.randint(1, 3)
        p.stats[stat_key] = p.stats.get(stat_key, 0) + gain
        p.spend_action()
        self.game.add_log(f"{p.name} тренирует «{stat_ru(stat_key)}» (+{gain}).")
        self.game.state = STATE_HUB
