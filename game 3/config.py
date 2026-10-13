"""
Общие константы и настройки игры: размеры окна, цвета, характеристики,
классы персонажей, таблица квестов и параметры голода/усталости/таверны.
Ничего "умного" здесь нет — только данные, на которые опираются остальные модули.
"""

WIDTH, HEIGHT = 1280, 720
FPS = 60

COLORS = {
    "bg": (24, 24, 32),
    "panel": (40, 40, 54),
    "panel_light": (54, 54, 72),
    "text": (230, 230, 235),
    "text_dim": (160, 160, 175),
    "border": (90, 90, 110),
    "button": (70, 70, 96),
    "button_hover": (100, 100, 140),
    "button_disabled": (50, 50, 58),
    "positive": (100, 220, 120),
    "negative": (220, 100, 100),
    "warning": (230, 190, 90),
    "player": [
        (210, 90, 90),   # Игрок 1 - красный
        (90, 140, 210),  # Игрок 2 - синий
        (100, 190, 110), # Игрок 3 - зелёный
        (215, 180, 80),  # Игрок 4 - жёлтый
    ],
}

FONT_NAME = "arial"

STATS = [
    ("strength", "Сила"),
    ("agility", "Ловкость"),
    ("intellect", "Интеллект"),
    ("stealth", "Скрытность"),
    ("attack_range", "Дальность атак"),
    ("stamina", "Выносливость"),
    ("magic_affinity", "Магия"),
]
# health / hunger / fatigue отображаются отдельно как ресурсы

BASE_STATS = {
    "strength": 8,
    "agility": 8,
    "intellect": 8,
    "stealth": 8,
    "attack_range": 8,
    "stamina": 40,
    "magic_affinity": 8,
}
BASE_HEALTH = 100
BASE_HUNGER = 100
BASE_FATIGUE = 0

CLASS_DATA = {
    # attack_weights — из каких характеристик складывается сила атаки класса
    # и с каким весом (сумма весов = 1.0). Так атака честно завязана на
    # реальные, актуальные характеристики персонажа, а не на одно число.
    "Воин": {
        "bonus": {"strength": 6, "stamina": 15},
        "health_bonus": 30,
        "attack_weights": {"strength": 0.85, "stamina": 0.15},  # упор на Силу
        "privilege": "Стойкость: получаемый урон снижается на 10%.",
        "desc": "Мастер ближнего боя. Много здоровья и силы.",
    },
    "Лучник": {
        "bonus": {"attack_range": 8, "agility": 5},
        "health_bonus": 10,
        "attack_weights": {"attack_range": 0.5, "agility": 0.3, "strength": 0.2},
        "privilege": "Меткий глаз: шанс критического удара +15%.",
        "desc": "Дальний бой: Дальность атак, Ловкость и немного Силы.",
    },
    "Колдун": {
        "bonus": {"intellect": 8, "magic_affinity": 8},
        "health_bonus": -10,
        "attack_weights": {"magic_affinity": 0.6, "intellect": 0.4},
        "privilege": "Атаки используют Магию и Интеллект вместо Силы.",
        "desc": "Мощная магия: Магия и Интеллект, ценой хрупкости.",
    },
    "Плут": {
        "bonus": {"stealth": 10, "agility": 6},
        "health_bonus": 0,
        "attack_weights": {"stealth": 0.4, "agility": 0.35, "strength": 0.25},
        "privilege": "Уклонение +15%, критический урон x1.75 вместо x1.5.",
        "desc": "Скрытный убийца: Скрытность, Ловкость и Сила.",
    },
    "Алхимик": {
        "bonus": {"magic_affinity": 6, "intellect": 6},
        "health_bonus": 0,
        "attack_weights": {"intellect": 0.8, "magic_affinity": 0.2},
        "privilege": "Лечение усилено на 40%.",
        "desc": "Поддержка отряда: атаки и лечение через Интеллект.",
    },
}
CLASS_NAMES = list(CLASS_DATA.keys())

QUESTS_PER_KINGDOM_TO_ADVANCE = 3

QUESTS = {
    1: {
        "название": "Тренировочный лагерь",
        "surface": [
            {"id": "S1", "name": "Разведка окрестностей", "reward_stat": "agility",
             "reward_amount": 2, "reward_gold": 5, "enemy": None},
            {"id": "S2", "name": "Охота на волков", "reward_stat": "strength",
             "reward_amount": 2, "reward_gold": 6,
             "enemy": {"name": "Стая волков", "health": 30, "attack": 6}},
            {"id": "S3", "name": "Сопровождение торговца", "reward_stat": "stealth",
             "reward_amount": 2, "reward_gold": 8, "enemy": None},
        ],
        "dungeon": [
            {"id": "D1", "name": "Пещера летучих мышей", "reward_stat": "intellect",
             "reward_amount": 2, "reward_gold": 8,
             "enemy": {"name": "Рой мышей", "health": 25, "attack": 5},
             "chest_stat": "health", "chest_amount": 10},
            {"id": "D2", "name": "Заброшенная шахта", "reward_stat": "magic_affinity",
             "reward_amount": 2, "reward_gold": 10,
             "enemy": {"name": "Каменный голем", "health": 45, "attack": 9},
             "chest_stat": "stamina", "chest_amount": 10},
        ],
    },
    2: {
        "название": "Соседнее королевство",
        "surface": [
            {"id": "S4", "name": "Бандиты на дороге", "reward_stat": "strength",
             "reward_amount": 3, "reward_gold": 10,
             "enemy": {"name": "Бандит", "health": 55, "attack": 10}},
            {"id": "S5", "name": "Дипломатическая миссия", "reward_stat": "intellect",
             "reward_amount": 3, "reward_gold": 12, "enemy": None},
        ],
        "dungeon": [
            {"id": "D3", "name": "Гробница древнего короля", "reward_stat": "magic_affinity",
             "reward_amount": 3, "reward_gold": 14,
             "enemy": {"name": "Страж-скелет", "health": 70, "attack": 12},
             "chest_stat": "health", "chest_amount": 15},
            {"id": "D4", "name": "Логово тролля", "reward_stat": "attack_range",
             "reward_amount": 3, "reward_gold": 16,
             "enemy": {"name": "Тролль", "health": 90, "attack": 14},
             "chest_stat": "strength", "chest_amount": 5},
        ],
    },
    3: {
        "название": "Внешний мир",
        "surface": [
            {"id": "S6", "name": "Патруль демонов", "reward_stat": "stealth",
             "reward_amount": 4, "reward_gold": 18,
             "enemy": {"name": "Демон-разведчик", "health": 80, "attack": 15}},
        ],
        "dungeon": [],
    },
}

# Финальный босс — крайне сильный противник. Атакуется отдельной кнопкой
# "Напасть на Демона" из лагеря (см. ui/screens/hub.py), а не как обычный
# квест: к нему стоит подходить только прокачавшись и пройдя другие квесты.
DEMON_BOSS = {"id": "BOSS", "name": "Замок Верховного Демона", "reward_stat": None,
              "reward_amount": 0, "reward_gold": 0,
              "enemy": {"name": "Верховный Демон", "health": 650, "attack": 42},
              "boss": True}

SHOP_FOOD_COST = 6
SHOP_FOOD_HUNGER = 100
SHOP_REST_COST = 10
SHOP_REST_FATIGUE_DROP = 100
SHOP_REST_HUNGER_BONUS = 20

# Снаряжение таверны: постоянно поднимает характеристику, покупается один раз.
SHOP_ITEMS = [
    {"id": "item_hammer", "name": "Молот силы", "stat": "strength", "amount": 10, "cost": 35},
    {"id": "item_bow", "name": "Лук меткости", "stat": "attack_range", "amount": 10, "cost": 35},
    {"id": "item_tome", "name": "Гримуар магии", "stat": "magic_affinity", "amount": 10, "cost": 35},
    {"id": "item_cloak", "name": "Плащ теней", "stat": "stealth", "amount": 10, "cost": 35},
    {"id": "item_amulet", "name": "Амулет разума", "stat": "intellect", "amount": 10, "cost": 35},
    {"id": "item_boots", "name": "Сапоги ловкости", "stat": "agility", "amount": 8, "cost": 30},
    {"id": "item_armor", "name": "Тяжёлые доспехи", "stat": "health", "amount": 25, "cost": 45},
]

ACTION_HUNGER_COST = 12
ACTION_FATIGUE_GAIN = 12
FATIGUE_PENALTY_THRESHOLD = 80
FATIGUE_DAMAGE_MULT = 0.7
STARVATION_DAMAGE = 6

MIN_PLAYERS = 2
MAX_PLAYERS = 4

ACTIONS_PER_TURN = 2   # лимит действий за ход, потом ход переходит следующему игроку
TURN_PASS_DELAY_MS = 1200
