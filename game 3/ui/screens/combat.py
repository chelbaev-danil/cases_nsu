"""Экран боя (STATE_COMBAT): атака/лечение/перемирие/бегство, HP-бары,
журнал боя и разрешение исхода (победа/поражение/бегство)."""

import pygame

from config import COLORS, WIDTH
from logic.combat import apply_damage, compute_attack, compute_heal
from logic.game_state import STATE_GAME_OVER, STATE_HUB
from models.player import Player
from ui.button import Button
from ui.helpers import target_display


class CombatScreenMixin:
    def draw_combat(self):
        g = self.game
        p = g.current_player()
        target = g.combat_pvp_target or g.combat_enemy

        target_name = target.name if not isinstance(target, Player) else f"{target.name} ({target.char_class})"
        self.blit_center(self.font_title, f"Бой: {p.name}  ПРОТИВ  {target_name}", 20)

        # HP бары
        self.draw_hp_bar(120, 90, 400, p.name, p.health, p.max_health, p.color)
        t_max = target.max_health
        t_color = target.color if isinstance(target, Player) else COLORS["negative"]
        self.draw_hp_bar(WIDTH - 520, 90, 400, target_name, target.health, t_max, t_color)

        # Лог боя
        log_rect = (120, 150, WIDTH - 240, 220)
        self.draw_panel_box(log_rect)
        ly = log_rect[1] + 12
        for line in g.combat_log[-8:]:
            txt = self.font_small.render(line, True, COLORS["text"])
            self.screen.blit(txt, (log_rect[0] + 14, ly))
            ly += 22

        both_alive = p.health > 0 and target.health > 0
        bx, by, bw, bh, gap = 140, 400, 240, 52, 16
        self.buttons.append(Button((bx, by, bw, bh), "Атаковать",
                                    lambda: self.combat_action("attack"), both_alive))
        self.buttons.append(Button((bx + bw + gap, by, bw, bh), "Лечение",
                                    lambda: self.combat_action("heal"), both_alive))
        self.buttons.append(Button((bx + 2 * (bw + gap), by, bw, bh), "Перемирие",
                                    lambda: self.combat_action("truce"),
                                    both_alive and isinstance(target, Player)))
        self.buttons.append(Button((bx + 3 * (bw + gap), by, bw, bh), "Бежать",
                                    lambda: self.combat_action("flee"), both_alive))

        if not both_alive:
            self.buttons.append(Button((WIDTH // 2 - 120, 480, 240, 50), "Продолжить",
                                        self.resolve_combat_end))

    def draw_panel_box(self, rect):
        r = pygame.Rect(rect)
        pygame.draw.rect(self.screen, COLORS["panel"], r, border_radius=10)
        pygame.draw.rect(self.screen, COLORS["border"], r, width=1, border_radius=10)

    def draw_hp_bar(self, x, y, w, label, hp, max_hp, color):
        pygame.draw.rect(self.screen, COLORS["panel_light"], (x, y, w, 30), border_radius=6)
        ratio = max(0, hp) / max_hp if max_hp else 0
        pygame.draw.rect(self.screen, color, (x, y, int(w * ratio), 30), border_radius=6)
        pygame.draw.rect(self.screen, COLORS["border"], (x, y, w, 30), width=1, border_radius=6)
        txt = self.font_small.render(f"{label}: {max(0, hp)}/{max_hp}", True, COLORS["text"])
        self.screen.blit(txt, (x, y - 22))

    def combat_action(self, action: str):
        g = self.game
        p = g.current_player()
        target = g.combat_pvp_target or g.combat_enemy

        if action == "flee":
            g.combat_log.append(f"{p.name} отступает из боя.")
            p.spend_action()
            g.state = STATE_HUB
            return

        if action == "truce" and isinstance(target, Player):
            g.combat_log.append(f"{p.name} и {target.name} заключают перемирие.")
            p.spend_action()
            g.state = STATE_HUB
            return

        if action == "heal":
            heal = compute_heal(p)
            p.health = min(p.max_health, p.health + heal)
            g.combat_log.append(f"{p.name} лечится на {heal} HP.")
        else:  # attack
            res = compute_attack(p, target, g.is_day)
            if res["dodged"]:
                g.combat_log.append(f"{target_display(target)} уворачивается от атаки!")
            else:
                apply_damage(target, res["damage"])
                crit_str = " (КРИТ!)" if res["crit"] else ""
                g.combat_log.append(f"{p.name} наносит {res['damage']} урона{crit_str}.")

        p.spend_action()

        if target.health <= 0:
            g.combat_log.append(f"{target_display(target)} повержен(а)!")
            self.on_target_defeated()
            return

        # ответный удар цели
        res2 = compute_attack(target, p, g.is_day)
        if res2["dodged"]:
            g.combat_log.append(f"{p.name} уворачивается от ответного удара!")
        else:
            apply_damage(p, res2["damage"])
            crit_str = " (КРИТ!)" if res2["crit"] else ""
            g.combat_log.append(f"{target_display(target)} отвечает на {res2['damage']} урона{crit_str}.")
        if p.health <= 0:
            g.combat_log.append(f"{p.name} терпит поражение!")

    def on_target_defeated(self):
        g = self.game
        p = g.current_player()
        if g.combat_quest is not None:
            quest = g.combat_quest
            is_boss = quest.get("boss", False)
            if is_boss:
                p.ending = "hero"
                g.add_log(f"{p.name} побеждает Верховного Демона и становится Героем Мира!")
            else:
                g.apply_quest_reward(p, quest, chest=bool(quest.get("chest_stat")))
                p.completed_quests.add(quest["id"])
        elif g.combat_pvp_target is not None:
            target = g.combat_pvp_target
            target.alive = False
            g.add_log(f"{p.name} побеждает {target.name} в поединке!")

    def resolve_combat_end(self):
        g = self.game
        p = g.current_player()
        if p.health <= 0 and p.alive:
            p.alive = False
            g.add_log(f"{p.name} погибает в бою!")
        g.combat_enemy = None
        g.combat_quest = None
        g.combat_pvp_target = None
        g.check_game_over()
        if g.state != STATE_GAME_OVER:
            if not p.alive:
                g.end_turn()  # погибший игрок пропускает ход, очередь идёт дальше
            else:
                g.state = STATE_HUB
