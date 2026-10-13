"""Финальный экран (STATE_GAME_OVER): текст концовки и сводка по игрокам."""

from config import HEIGHT, WIDTH
from logic.game_state import Game
from ui.button import Button


class GameOverScreenMixin:
    def draw_game_over(self):
        g = self.game
        self.blit_center(self.font_title, "Игра окончена", 60)
        if g.winner:
            texts = {
                "pvp": f"{g.winner.name} ({g.winner.char_class}) остаётся последним героем в живых!",
                "hero": f"{g.winner.name} ({g.winner.char_class}) побеждает Демона и становится Героем Мира!",
            }
            msg = texts.get(g.ending_type, "Игра завершена.")
        else:
            msg = "Все герои пали."
        self.blit_center(self.font_big, msg, 140)

        y = 220
        for p in g.players:
            status = "Жив" if p.alive else "Погиб"
            line = f"{p.name} — {p.char_class} — HP {p.health}/{p.max_health} — {status}"
            txt = self.font.render(line, True, p.color)
            self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))
            y += 30

        self.buttons.append(Button((WIDTH // 2 - 110, HEIGHT - 100, 220, 48), "Новая игра",
                                    self.restart))

    def restart(self):
        self.game = Game()
        self.text_input = ""
        self.selected_class = None
        self.setup_error = ""
        self.selected_player_count = None
        self.setup_records = []
