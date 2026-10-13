"""Экран таверны (STATE_SHOP): еда и отдых за золото, а также покупка
снаряжения (оружие/доспехи), которое навсегда поднимает характеристику."""

from config import (
    BASE_HUNGER,
    COLORS,
    SHOP_FOOD_COST,
    SHOP_FOOD_HUNGER,
    SHOP_ITEMS,
    SHOP_REST_COST,
    SHOP_REST_FATIGUE_DROP,
    SHOP_REST_HUNGER_BONUS,
    WIDTH,
)
from logic.game_state import STATE_HUB, stat_ru
from ui.button import Button


class ShopScreenMixin:
    def draw_shop(self):
        p = self.game.current_player()
        self.draw_player_panel(p)
        self.blit_center(self.font_title, "Таверна", 20)
        self.blit_center(self.font, f"Золото: {p.gold}", 56)

        can = self.game.actions_left > 0

        rect1 = (360, 96, 500, 56)
        self.buttons.append(Button(
            rect1, f"Купить еду — голод восстановлен ({SHOP_FOOD_COST} золота)",
            self.buy_food, enabled=can and p.gold >= SHOP_FOOD_COST))

        rect2 = (360, 160, 500, 56)
        self.buttons.append(Button(
            rect2, f"Снять комнату — усталость снята ({SHOP_REST_COST} золота)",
            self.buy_rest, enabled=can and p.gold >= SHOP_REST_COST))

        self.font.set_bold(True)
        self.screen.blit(self.font.render("Снаряжение (постоянно поднимает характеристику)",
                                          True, COLORS["text"]), (360, 234))
        self.font.set_bold(False)

        y = 268
        for item in SHOP_ITEMS:
            bought = item["id"] in p.purchased_items
            stat_label = "Здоровье" if item["stat"] == "health" else stat_ru(item["stat"])
            label = f"{item['name']} — +{item['amount']} {stat_label} ({item['cost']} золота)"
            if bought:
                label += "  [куплено]"
            enabled = can and not bought and p.gold >= item["cost"]
            self.buttons.append(Button((360, y, 500, 46), label,
                                        lambda it=item: self.buy_item(it), enabled))
            y += 52

        if self.setup_error:
            err_txt = self.font.render(self.setup_error, True, COLORS["negative"])
            self.screen.blit(err_txt, (WIDTH // 2 - err_txt.get_width() // 2, y + 6))
            y += 30

        self.buttons.append(Button((WIDTH // 2 - 100, max(y + 24, 630), 200, 44), "Назад", self.leave_shop))

    def buy_food(self):
        p = self.game.current_player()
        if p.gold < SHOP_FOOD_COST:
            self.setup_error = "Ошибка: не хватает золота на еду!"
            return
        if not self.game.use_action():
            return
        p.gold -= SHOP_FOOD_COST
        p.hunger = SHOP_FOOD_HUNGER
        self.setup_error = ""
        self.game.add_log(f"{p.name} покупает еду в таверне.")

    def buy_rest(self):
        p = self.game.current_player()
        if p.gold < SHOP_REST_COST:
            self.setup_error = "Ошибка: не хватает золота на комнату!"
            return
        if not self.game.use_action():
            return
        p.gold -= SHOP_REST_COST
        p.fatigue = max(0, p.fatigue - SHOP_REST_FATIGUE_DROP)
        p.hunger = min(BASE_HUNGER, p.hunger + SHOP_REST_HUNGER_BONUS)
        self.setup_error = ""
        self.game.add_log(f"{p.name} снимает комнату и отсыпается.")

    def buy_item(self, item: dict):
        p = self.game.current_player()
        if item["id"] in p.purchased_items:
            return
        if p.gold < item["cost"]:
            self.setup_error = "Ошибка: не хватает золота на снаряжение!"
            return
        if not self.game.use_action():
            return
        p.gold -= item["cost"]
        p.purchased_items.add(item["id"])
        if item["stat"] == "health":
            p.max_health += item["amount"]
            p.health = min(p.max_health, p.health + item["amount"])
        else:
            p.stats[item["stat"]] = p.stats.get(item["stat"], 0) + item["amount"]
        self.setup_error = ""
        self.game.add_log(f"{p.name} покупает «{item['name']}» (+{item['amount']}).")

    def leave_shop(self):
        self.setup_error = ""
        self.goto(STATE_HUB)
