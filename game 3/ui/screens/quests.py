"""Экран списка квестов (STATE_QUESTS): наземные квесты и подземелья
текущего королевства, запуск боя или мирного квеста."""

from config import COLORS, HEIGHT, QUESTS, WIDTH
from logic.game_state import STATE_COMBAT, STATE_HUB, stat_ru
from models.enemy import Enemy
from ui.button import Button


class QuestsScreenMixin:
    def draw_quests(self):
        p = self.game.current_player()
        self.draw_player_panel(p)
        kdata = QUESTS[p.kingdom]
        self.blit_center(self.font_title, f"Квесты — {kdata['название']}", 20)

        y = 150
        self.font.set_bold(True)
        self.screen.blit(self.font.render("Наземные квесты", True, COLORS["text"]), (340, y))
        self.font.set_bold(False)
        y += 34
        for q in kdata["surface"]:
            y = self.draw_quest_row(q, p, y, is_dungeon=False)

        y += 20
        self.font.set_bold(True)
        self.screen.blit(self.font.render("Подземелья / пещеры", True, COLORS["text"]), (340, y))
        self.font.set_bold(False)
        y += 34
        for q in kdata["dungeon"]:
            y = self.draw_quest_row(q, p, y, is_dungeon=True)

        self.buttons.append(Button((WIDTH // 2 - 100, HEIGHT - 60, 200, 44), "Назад",
                                    lambda: self.goto(STATE_HUB)))

    def draw_quest_row(self, q, player, y, is_dungeon):
        done = q["id"] in player.completed_quests
        rect = (340, y, WIDTH - 380, 46)
        reward = f"+{q['reward_amount']} {stat_ru(q['reward_stat'])}" if q.get("reward_stat") else ""
        enemy_str = f" | враг: {q['enemy']['name']}" if q.get("enemy") else ""
        chest_str = ""
        if is_dungeon and q.get("chest_stat"):
            chest_str = f" | сундук: +{q['chest_amount']} {stat_ru(q['chest_stat'])}"
        label = f"{q['name']}  ({reward}{enemy_str}{chest_str})"
        if done:
            label += "  [пройден]"
        enabled = not done
        self.buttons.append(Button(rect, label, lambda qq=q, d=is_dungeon: self.start_quest(qq, d), enabled))
        return y + 54

    def start_quest(self, quest, is_dungeon):
        if not self.game.use_action():
            return
        p = self.game.current_player()
        if quest.get("enemy"):
            e = quest["enemy"]
            self.game.combat_enemy = Enemy(e["name"], e["health"], e["attack"])
            self.game.combat_quest = quest
            self.game.combat_pvp_target = None
            self.game.combat_log = [f"Начинается бой с «{e['name']}»!"]
            self.game.state = STATE_COMBAT
        else:
            self.game.apply_quest_reward(p, quest, chest=False)
            p.completed_quests.add(quest["id"])
            p.spend_action()
            self.game.state = STATE_HUB
