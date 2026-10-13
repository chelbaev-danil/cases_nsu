"""Главный экран хода игрока (STATE_HUB): панель персонажа и меню действий
(тренировка, квесты, отдых, таверна, атака, переход в другое королевство,
атака Демона, сон ночью)."""

from config import BASE_HUNGER, DEMON_BOSS, QUESTS, WIDTH
from logic.game_state import STATE_COMBAT, STATE_QUESTS, STATE_SHOP, STATE_TARGET_SELECT, STATE_TRAIN
from models.enemy import Enemy
from ui.button import Button


class HubScreenMixin:
    def draw_hub(self):
        g = self.game
        p = g.current_player()
        self.draw_player_panel(p)
        self.draw_log_panel()

        kdata = QUESTS[p.kingdom]
        self.blit_center(self.font_big, f"Ход игрока {p.index + 1}: {p.name} — {kdata['название']}", 24)

        by = 200
        bw, bh, gap = 440, 50, 10
        bx = WIDTH // 2 - bw // 2
        can = g.actions_left > 0

        def add(label, action, enabled=True):
            nonlocal by
            self.buttons.append(Button((bx, by, bw, bh), label, action, enabled))
            by += bh + gap

        add("Прокачать характеристику", lambda: self.goto(STATE_TRAIN), can)
        add("Квесты", lambda: self.goto(STATE_QUESTS), can)
        add("Отдохнуть у костра (бесплатно, слегка)", self.do_rest, can)
        add(f"Таверна (золото: {p.gold})", self.enter_shop, can)

        others = [x for x in g.players if x.alive and x is not p]
        add("Напасть на игрока", lambda: self.goto(STATE_TARGET_SELECT), bool(others) and can)

        if p.kingdom < 3:
            nxt = QUESTS[p.kingdom + 1]["название"]
            add(f"Отправиться в «{nxt}»", self.do_advance_kingdom, can)
        else:
            add("Напасть на Демона (очень сильный противник!)", self.do_attack_demon, can)

        if not g.is_day:
            add("Сон (тратит все действия, полное восстановление)", self.do_sleep, can)

        self.buttons.append(Button((bx, by, bw, bh), "Закончить ход", g.end_turn))

    def do_rest(self):
        if not self.game.use_action():
            return
        p = self.game.current_player()
        p.rest()
        self.game.add_log(f"{p.name} отдыхает у костра.")

    def do_advance_kingdom(self):
        if not self.game.use_action():
            return
        p = self.game.current_player()
        self.game.advance_kingdom(p)
        p.spend_action()

    def do_attack_demon(self):
        """Прямая атака на Верховного Демона — очень сильного босса.
        К нему стоит подходить только прокачавшись и пройдя другие квесты."""
        if not self.game.use_action():
            return
        e = DEMON_BOSS["enemy"]
        g = self.game
        g.combat_enemy = Enemy(e["name"], e["health"], e["attack"])
        g.combat_quest = DEMON_BOSS
        g.combat_pvp_target = None
        g.combat_log = [f"{g.current_player().name} бросает вызов Верховному Демону!"]
        g.state = STATE_COMBAT

    def do_sleep(self):
        """Ночью: тратит все оставшиеся действия, полностью восстанавливает
        голод и усталость — после этого ход сам переходит дальше."""
        g = self.game
        p = g.current_player()
        if g.is_day or g.actions_left <= 0:
            return
        g.actions_left = 0
        p.hunger = BASE_HUNGER
        p.fatigue = 0
        g.add_log(f"{p.name} крепко спит до утра — голод и усталость полностью восстановлены.")

    def goto(self, state):
        self.game.state = state

    def enter_shop(self):
        self.setup_error = ""
        self.goto(STATE_SHOP)
