"""
Экраны создания партии: выбор количества игроков (STATE_PLAYER_COUNT)
и по очереди — имя и класс для каждого игрока (STATE_SETUP).
Это Mixin — он рассчитан на подмешивание в App и обращается к self.game,
self.buttons, self.screen и т.д., которые определены там.
"""

import pygame

from config import CLASS_DATA, COLORS, MAX_PLAYERS, MIN_PLAYERS, WIDTH
from logic.game_state import STATE_PLAYER_COUNT, STATE_SETUP, stat_ru
from models.player import make_player
from ui.button import Button


class SetupScreenMixin:
    # ------------------------ КОЛИЧЕСТВО ИГРОКОВ --------------------------- #
    def draw_player_count(self):
        self.blit_center(self.font_title, "Сколько всего игроков?", 70)
        self.blit_center(self.font, "Выберите карточку — от 2 до 4 участников", 108)

        options = list(range(MIN_PLAYERS, MAX_PLAYERS + 1))
        card_w, card_h, gap = 220, 220, 30
        total_w = len(options) * card_w + (len(options) - 1) * gap
        start_x = WIDTH // 2 - total_w // 2
        card_y = 170

        for i, count in enumerate(options):
            rect = pygame.Rect(start_x + i * (card_w + gap), card_y, card_w, card_h)
            selected = self.selected_player_count == count
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            if selected:
                bg = COLORS["button_hover"]
            elif hovered:
                bg = COLORS["panel_light"]
            else:
                bg = COLORS["panel"]
            pygame.draw.rect(self.screen, bg, rect, border_radius=14)
            border_color = COLORS["positive"] if selected else COLORS["border"]
            pygame.draw.rect(self.screen, border_color, rect, width=3 if selected else 1,
                              border_radius=14)

            # Иконки-силуэты игроков внутри карточки
            icon_gap = 40
            icons_w = (count - 1) * icon_gap
            icon_x0 = rect.centerx - icons_w // 2
            icon_y = rect.y + 70
            for j in range(count):
                self.draw_person_icon(icon_x0 + j * icon_gap, icon_y, 22, COLORS["player"][j % 4])

            label = f"{count} игрока"
            label_txt = self.font_big.render(label, True, COLORS["text"])
            self.screen.blit(label_txt, label_txt.get_rect(center=(rect.centerx, rect.bottom - 44)))
            if selected:
                check_txt = self.font.render("выбрано", True, COLORS["positive"])
                self.screen.blit(check_txt, check_txt.get_rect(center=(rect.centerx, rect.bottom - 18)))

            self.buttons.append(Button(rect, "", lambda c=count: self.select_player_count(c)))

        err_y = card_y + card_h + 30
        if self.setup_error:
            self.blit_center(self.font, self.setup_error, err_y)
            err_y += 30

        nav_y = err_y + 30
        self.buttons.append(Button((WIDTH // 2 - 220, nav_y, 200, 48), "Назад",
                                    lambda: None, enabled=False))
        self.buttons.append(Button((WIDTH // 2 + 20, nav_y, 200, 48), "Далее",
                                    self.confirm_player_count))

    def draw_person_icon(self, cx, cy, size, color):
        """Простая иконка-силуэт человечка: голова + тело."""
        head_r = int(size * 0.42)
        pygame.draw.circle(self.screen, color, (cx, cy - size), head_r)
        body_rect = pygame.Rect(0, 0, int(size * 1.3), int(size * 1.4))
        body_rect.midtop = (cx, cy - size + head_r)
        pygame.draw.rect(self.screen, color, body_rect,
                          border_top_left_radius=int(size * 0.6),
                          border_top_right_radius=int(size * 0.6))

    def select_player_count(self, count: int):
        self.selected_player_count = count
        self.setup_error = ""

    def confirm_player_count(self):
        if self.selected_player_count is None:
            self.setup_error = "Ошибка: выберите количество игроков!"
            return
        self.game.total_players = self.selected_player_count
        self.game.setup_index = 0
        self.game.players = []
        self.setup_records = []
        self.selected_class = None
        self.text_input = ""
        self.setup_error = ""
        self.game.state = STATE_SETUP

    # ---------------------------- SETUP -------------------------------- #
    def draw_setup(self):
        g = self.game
        title = f"Игрок {g.setup_index + 1} из {g.total_players}: имя и класс персонажа"
        self.blit_center(self.font_title, title, 40)

        box = pygame.Rect(WIDTH // 2 - 180, 88, 360, 44)
        pygame.draw.rect(self.screen, COLORS["panel_light"], box, border_radius=8)
        pygame.draw.rect(self.screen, COLORS["border"], box, width=1, border_radius=8)
        name_display = self.text_input if self.text_input else f"Игрок {g.setup_index + 1}"
        txt = self.font.render(name_display, True, COLORS["text"])
        self.screen.blit(txt, txt.get_rect(center=box.center))

        y = 148
        for cname, cdata in CLASS_DATA.items():
            rect = pygame.Rect(140, y, WIDTH - 280, 84)
            selected = self.selected_class == cname
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            if selected:
                bg = COLORS["button_hover"]
            elif hovered:
                bg = COLORS["panel_light"]
            else:
                bg = COLORS["panel"]
            pygame.draw.rect(self.screen, bg, rect, border_radius=10)
            border_color = COLORS["positive"] if selected else COLORS["border"]
            pygame.draw.rect(self.screen, border_color, rect, width=2 if selected else 1, border_radius=10)
            name_txt = self.font_big.render(cname, True, COLORS["text"])
            self.screen.blit(name_txt, (rect.x + 100, rect.y + 8))
            desc_txt = self.font_small.render(cdata["desc"], True, COLORS["text_dim"])
            self.screen.blit(desc_txt, (rect.x + 100, rect.y + 34))
            priv_txt = self.font_small.render("* " + cdata["privilege"], True, COLORS["warning"])
            self.screen.blit(priv_txt, (rect.x + 100, rect.y + 54))
            bonus_str = ", ".join(f"+{v} {stat_ru(k)}" for k, v in cdata["bonus"].items())
            bonus_txt = self.font_small.render(bonus_str, True, COLORS["positive"])
            self.screen.blit(bonus_txt, (rect.right - bonus_txt.get_width() - 16, rect.y + 8))

            self.draw_character_icon(rect.x + 50, rect.bottom - 10, 1.7, cname,
                                      COLORS["player"][self.game.setup_index % 4])
            self.buttons.append(Button(rect, "", lambda cn=cname: self.select_class(cn)))
            y += 92

        if self.setup_error:
            err_txt = self.font.render(self.setup_error, True, COLORS["negative"])
            self.screen.blit(err_txt, (WIDTH // 2 - err_txt.get_width() // 2, y + 6))

        nav_y = y + 40
        self.buttons.append(Button((WIDTH // 2 - 220, nav_y, 200, 48), "Назад", self.setup_back))
        self.buttons.append(Button((WIDTH // 2 + 20, nav_y, 200, 48), "Далее", self.setup_next))

    def select_class(self, char_class: str):
        self.selected_class = char_class
        self.setup_error = ""

    def setup_next(self):
        g = self.game
        if g.setup_index >= g.total_players:
            # страховка: все игроки уже созданы, повторный клик не должен ничего добавлять
            g.start_game()
            return
        if self.selected_class is None:
            self.setup_error = "Ошибка: выберите класс персонажа!"
            return
        name = self.text_input.strip() or f"Игрок {g.setup_index + 1}"
        player = make_player(g.setup_index, name, self.selected_class)
        g.players.append(player)
        self.setup_records.append((name, self.selected_class))
        g.setup_index += 1
        self.text_input = ""
        self.selected_class = None
        self.setup_error = ""
        if g.setup_index >= g.total_players:
            g.start_game()
            g.add_log("Все герои прибывают в тренировочный лагерь.")
        # иначе остаёмся в STATE_SETUP для следующего игрока

    def setup_back(self):
        g = self.game
        self.setup_error = ""
        if g.setup_index == 0:
            # возвращаемся к выбору количества игроков
            self.selected_player_count = g.total_players
            g.state = STATE_PLAYER_COUNT
            return
        # убираем последнего добавленного игрока и восстанавливаем его данные для правки
        if g.players:
            g.players.pop()
        g.setup_index -= 1
        if self.setup_records:
            prev_name, prev_class = self.setup_records.pop()
        else:
            prev_name, prev_class = "", None
        self.text_input = prev_name
        self.selected_class = prev_class
