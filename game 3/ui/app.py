"""
Класс App — точка сборки всего интерфейса: инициализация pygame и окна,
игровой цикл, обработка событий (мышь/клавиатура) и диспетчер отрисовки
по состояниям игры. Сама разметка каждого экрана вынесена в миксины
из пакета ui.screens — App лишь наследует их все и хранит общие ресурсы
(шрифты, экран, список кнопок текущего кадра).
"""

import math
import sys

from typing import Optional

import pygame

from config import ACTIONS_PER_TURN, BASE_HUNGER, COLORS, FONT_NAME, FPS, HEIGHT, QUESTS, STATS, TURN_PASS_DELAY_MS, WIDTH
from logic.game_state import (
    STATE_COMBAT,
    STATE_GAME_OVER,
    STATE_HUB,
    STATE_PLAYER_COUNT,
    STATE_QUESTS,
    STATE_SETUP,
    STATE_SHOP,
    STATE_TARGET_SELECT,
    STATE_TRAIN,
    Game,
)
from models.player import Player
from ui.helpers import wrap_text
from ui.screens.combat import CombatScreenMixin
from ui.screens.game_over import GameOverScreenMixin
from ui.screens.hub import HubScreenMixin
from ui.screens.quests import QuestsScreenMixin
from ui.screens.setup import SetupScreenMixin
from ui.screens.shop import ShopScreenMixin
from ui.screens.target_select import TargetSelectScreenMixin
from ui.screens.train import TrainScreenMixin


class App(
    SetupScreenMixin,
    HubScreenMixin,
    TrainScreenMixin,
    QuestsScreenMixin,
    TargetSelectScreenMixin,
    ShopScreenMixin,
    CombatScreenMixin,
    GameOverScreenMixin,
):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Хроники Пяти Классов")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont(FONT_NAME, 30, bold=True)
        self.font_big = pygame.font.SysFont(FONT_NAME, 22, bold=True)
        self.font = pygame.font.SysFont(FONT_NAME, 18)
        self.font_small = pygame.font.SysFont(FONT_NAME, 15)
        self.game = Game()
        self.buttons: list = []
        self.text_input = ""
        self.pending_stat_choice = None
        self.pending_quest_list_type = None
        self.selected_class: Optional[str] = None
        self.setup_error: str = ""
        self.selected_player_count: Optional[int] = None
        self.setup_records: list = []  # (имя, класс) для кнопки "Назад"
        self.pending_end_at: Optional[int] = None  # момент автопередачи хода

    # ------------------------------------------------------------------ #
    def run(self):
        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and self.game.state == STATE_SETUP:
            if event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            elif len(self.text_input) < 14 and event.unicode.isprintable():
                self.text_input += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.pending_end_at is not None:
                return  # идёт передача хода — клики игнорируются
            for b in list(self.buttons):
                if b.handle_click(event.pos):
                    break

    def now(self) -> int:
        return pygame.time.get_ticks()

    def check_turn_pass(self):
        """Если лимит действий исчерпан — планирует и выполняет автопередачу хода."""
        g = self.game
        if g.state not in (STATE_HUB, STATE_TRAIN, STATE_QUESTS, STATE_TARGET_SELECT, STATE_SHOP):
            self.pending_end_at = None
            return
        now = self.now()
        if g.actions_left <= 0:
            if self.pending_end_at is None:
                self.pending_end_at = now + TURN_PASS_DELAY_MS
            elif now >= self.pending_end_at:
                self.pending_end_at = None
                g.end_turn()
        else:
            self.pending_end_at = None

    # ------------------------------------------------------------------ #
    def draw(self):
        self.check_turn_pass()
        self.screen.fill(COLORS["bg"])
        self.buttons = []
        state = self.game.state
        if state == STATE_PLAYER_COUNT:
            self.draw_player_count()
        elif state == STATE_SETUP:
            self.draw_setup()
        elif state == STATE_HUB:
            self.draw_hub()
        elif state == STATE_TRAIN:
            self.draw_train()
        elif state == STATE_QUESTS:
            self.draw_quests()
        elif state == STATE_TARGET_SELECT:
            self.draw_target_select()
        elif state == STATE_COMBAT:
            self.draw_combat()
        elif state == STATE_SHOP:
            self.draw_shop()
        elif state == STATE_GAME_OVER:
            self.draw_game_over()

        if state not in (STATE_PLAYER_COUNT, STATE_SETUP, STATE_GAME_OVER):
            self.draw_daynight_badge()
        if state in (STATE_HUB, STATE_TRAIN, STATE_QUESTS, STATE_TARGET_SELECT, STATE_SHOP):
            self.draw_actions_badge()
            if self.pending_end_at is not None:
                nxt = self.game.next_player()
                msg = f"Лимит действий исчерпан — ход переходит к игроку {nxt.index + 1}: {nxt.name}"
                rect = pygame.Rect(330, 100, 600, 44)
                pygame.draw.rect(self.screen, COLORS["panel_light"], rect, border_radius=10)
                pygame.draw.rect(self.screen, COLORS["warning"], rect, width=2, border_radius=10)
                txt = self.font.render(msg, True, COLORS["warning"])
                self.screen.blit(txt, txt.get_rect(center=rect.center))

        self.draw_buttons()


    def draw_actions_badge(self):
        left = self.game.actions_left
        rect = pygame.Rect(WIDTH - 420, HEIGHT - 60, 210, 40)
        pygame.draw.rect(self.screen, COLORS["panel_light"], rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS["border"], rect, width=2, border_radius=8)
        txt = self.font_small.render("Действия:", True, COLORS["text"])
        self.screen.blit(txt, (rect.x + 12, rect.centery - txt.get_height() // 2))
        for i in range(ACTIONS_PER_TURN):
            c = (rect.x + 104 + i * 22, rect.centery)
            if i < left:
                pygame.draw.circle(self.screen, COLORS["positive"], c, 8)
            else:
                pygame.draw.circle(self.screen, COLORS["text_dim"], c, 8, 2)

    def draw_character_icon(self, cx, cy, scale, cls, color):
        """Условная иконка персонажа для карточек выбора класса —
        голова, тело и небольшой атрибут класса (меч, лук, посох и т.д.)."""
        scr = self.screen

        def sc(v):
            return int(v * scale)

        skin = (238, 205, 165)
        leg_h = sc(16)
        pygame.draw.rect(scr, (45, 45, 58), (cx - sc(8), cy - leg_h, sc(6), leg_h))
        pygame.draw.rect(scr, (45, 45, 58), (cx + sc(2), cy - leg_h, sc(6), leg_h))
        body_w, body_h = sc(24), sc(30)
        body_top = cy - leg_h - body_h + sc(3)
        pygame.draw.rect(scr, color, (cx - body_w // 2, body_top, body_w, body_h), border_radius=sc(6))
        hr = sc(9)
        hx, hy = cx, body_top - hr + sc(2)
        pygame.draw.circle(scr, skin, (hx, hy), hr)
        pygame.draw.circle(scr, (30, 30, 30), (hx + sc(3), hy - sc(1)), max(1, sc(1)))
        hand = (cx + sc(15), body_top + sc(14))

        if cls == "Воин":
            pygame.draw.rect(scr, (170, 172, 185), (hx - hr, hy - hr, 2 * hr, hr),
                              border_top_left_radius=hr, border_top_right_radius=hr)
            pygame.draw.line(scr, (220, 222, 235), hand, (hand[0] + sc(4), hand[1] - sc(28)), max(2, sc(3)))
            pygame.draw.circle(scr, (150, 150, 168), (cx - sc(15), body_top + sc(14)), sc(8))
        elif cls == "Лучник":
            pygame.draw.polygon(scr, (60, 120, 70), [(hx - hr - 1, hy + sc(1)), (hx + hr + 1, hy + sc(1)),
                                                       (hx, hy - hr - sc(6))])
            pygame.draw.arc(scr, (150, 100, 50), (hand[0] - sc(10), hand[1] - sc(24), sc(20), sc(48)),
                             -1.6, 1.6, max(1, sc(2)))
        elif cls == "Колдун":
            pygame.draw.polygon(scr, (110, 70, 170), [(hx - hr - sc(2), hy - hr + sc(4)),
                                                        (hx + hr + sc(2), hy - hr + sc(4)),
                                                        (hx + sc(2), hy - hr - sc(20))])
            pygame.draw.line(scr, (130, 90, 50), (hand[0], hand[1] + sc(20)), (hand[0], hand[1] - sc(30)), max(1, sc(2)))
            pygame.draw.circle(scr, (120, 200, 255), (hand[0], hand[1] - sc(33)), max(2, sc(4)))
        elif cls == "Плут":
            pygame.draw.rect(scr, (40, 40, 52), (hx - hr, hy - hr, 2 * hr, hr + sc(1)),
                              border_top_left_radius=hr, border_top_right_radius=hr)
            pygame.draw.rect(scr, (40, 40, 52), (hx - hr, hy + sc(2), 2 * hr, sc(5)))
            pygame.draw.line(scr, (215, 215, 225), hand, (hand[0] + sc(10), hand[1] - sc(10)), max(1, sc(2)))
        else:  # Алхимик
            pygame.draw.line(scr, (90, 70, 40), (hx - hr, hy), (hx + hr, hy), 1)
            pygame.draw.circle(scr, (90, 220, 120), (hand[0], hand[1] - sc(4)), sc(6))
            pygame.draw.rect(scr, (200, 200, 210), (hand[0] - sc(2), hand[1] - sc(16), sc(4), sc(7)))

    def draw_buttons(self):
        """Отрисовывает фон/текст всех кнопок, добавленных в этом кадре.
        Кнопки с пустым label — это кликабельные оверлеи поверх уже
        нарисованных вручную карточек (выбор класса/кол-ва игроков),
        поэтому им отрисовка не нужна (иначе они перекроют картинку)."""
        for b in self.buttons:
            if b.label:
                b.draw(self.screen, self.font)

    # ---------------------------- ОБЩЕЕ ------------------------------------ #
    def draw_player_panel(self, p: Player):
        rect = pygame.Rect(20, 20, 300, 620)
        pygame.draw.rect(self.screen, COLORS["panel"], rect, border_radius=10)
        pygame.draw.rect(self.screen, p.color, rect, width=2, border_radius=10)

        name_txt = self.font_big.render(f"{p.name}", True, p.color)
        self.screen.blit(name_txt, (rect.x + 14, rect.y + 12))
        cls_txt = self.font_small.render(p.char_class, True, COLORS["text_dim"])
        self.screen.blit(cls_txt, (rect.x + 14, rect.y + 38))

        y = rect.y + 66
        self.draw_mini_bar(rect.x + 14, y, 272, "Здоровье", p.health, p.max_health, COLORS["positive"])
        y += 34
        self.draw_mini_bar(rect.x + 14, y, 272, "Голод", p.hunger, BASE_HUNGER, COLORS["warning"])
        y += 34
        self.draw_mini_bar(rect.x + 14, y, 272, "Усталость", p.fatigue, 100, COLORS["negative"], invert=True)
        y += 34
        gold_txt = self.font_small.render(f"Золото: {p.gold}", True, COLORS["warning"])
        self.screen.blit(gold_txt, (rect.x + 14, y))
        y += 30

        for key, label in STATS:
            val = p.stats.get(key, 0)
            txt = self.font_small.render(f"{label}: {val}", True, COLORS["text"])
            self.screen.blit(txt, (rect.x + 14, y))
            y += 22

        y += 10
        priv_lines = wrap_text(p.privilege, 34)
        for line in priv_lines:
            txt = self.font_small.render(line, True, COLORS["warning"])
            self.screen.blit(txt, (rect.x + 14, y))
            y += 18

        kingdom_txt = self.font_small.render(f"Королевство: {QUESTS[p.kingdom]['название']}",
                                              True, COLORS["text_dim"])
        self.screen.blit(kingdom_txt, (rect.x + 14, rect.bottom - 26))

    def draw_mini_bar(self, x, y, w, label, val, maxv, color, invert=False):
        pygame.draw.rect(self.screen, COLORS["panel_light"], (x, y + 14, w, 12), border_radius=4)
        ratio = max(0, min(1, val / maxv)) if maxv else 0
        bar_color = color
        pygame.draw.rect(self.screen, bar_color, (x, y + 14, int(w * ratio), 12), border_radius=4)
        txt = self.font_small.render(f"{label}: {val}/{maxv}", True, COLORS["text"])
        self.screen.blit(txt, (x, y))

    def draw_log_panel(self):
        rect = pygame.Rect(WIDTH - 340, 20, 320, 160)
        pygame.draw.rect(self.screen, COLORS["panel"], rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS["border"], rect, width=1, border_radius=10)
        title = self.font_small.render("Журнал событий", True, COLORS["text_dim"])
        self.screen.blit(title, (rect.x + 12, rect.y + 8))
        y = rect.y + 30
        for line in self.game.log[-6:]:
            for wrapped in wrap_text(line, 42):
                txt = self.font_small.render(wrapped, True, COLORS["text"])
                self.screen.blit(txt, (rect.x + 12, y))
                y += 18

    def draw_daynight_badge(self):
        is_day = self.game.is_day
        color = (230, 200, 90) if is_day else (120, 140, 220)
        rect = pygame.Rect(WIDTH - 200, HEIGHT - 60, 180, 40)
        pygame.draw.rect(self.screen, COLORS["panel_light"], rect, border_radius=8)
        pygame.draw.rect(self.screen, color, rect, width=2, border_radius=8)
        icon_c = (rect.x + 24, rect.centery)
        if is_day:
            pygame.draw.circle(self.screen, color, icon_c, 9)
        else:
            pygame.draw.circle(self.screen, color, icon_c, 10)
            pygame.draw.circle(self.screen, COLORS["panel_light"], (icon_c[0] + 5, icon_c[1] - 3), 8)
        txt = self.font.render("День" if is_day else "Ночь", True, color)
        self.screen.blit(txt, (rect.x + 48, rect.centery - txt.get_height() // 2))

    def blit_center(self, font, text, y):
        txt = font.render(text, True, COLORS["text"])
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))
