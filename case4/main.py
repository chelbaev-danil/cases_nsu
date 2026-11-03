import colorsys
import math

import turtle

_rainbow_on = False   # включён ли радужный режим
_counter = 0          # сколько отрезков уже нарисовано (нужно для смены цвета)


def setup_window() -> None:
    turtle.setup(900, 700)
    turtle.title("Фрактальная мастерская")
    turtle.colormode(1.0)        # цвета задаём числами от 0 до 1
    turtle.hideturtle()


def init_turtle() -> None:
    turtle.colormode(1.0)
    turtle.hideturtle()          # саму черепашку не показываем
    turtle.speed(0)              # максимальная скорость
    turtle.tracer(50, 0)         # обновляем экран пачками - так быстрее


def go_to(x: float, y: float, heading: float = 0) -> None:
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(heading)
    turtle.pendown()


def set_rainbow(flag: bool) -> None:
    global _rainbow_on, _counter
    _rainbow_on = bool(flag)
    _counter = 0
    turtle.pencolor("black")


def draw_line(size: float) -> None:
    global _counter
    if _rainbow_on:
        hue = (_counter * 0.003) % 1.0
        turtle.pencolor(colorsys.hsv_to_rgb(hue, 0.9, 0.85))
        _counter += 1
    turtle.forward(size)


def depth_color(level: int) -> tuple:
    green = max(0.0, min(1.0, 1.0 - level * 0.12))
    return (0.0, green, 0.0)


# ======================================================================
# Роль 1: basic
# ======================================================================



def draw_binary_tree(depth: int, size: float, angle: float,
                     color_by_depth: bool = True) -> None:
    if color_by_depth:
        turtle.pencolor(depth_color(depth))

    # Базовый случай: глубина 0 - просто палочка (и возвращаемся назад)
    if depth == 0:
        turtle.forward(size)
        turtle.backward(size)
        return

    # Шаг рекурсии
    turtle.forward(size)                                   # ствол
    turtle.right(angle)                                    # поворот направо
    draw_binary_tree(depth - 1, size / 2, angle, color_by_depth)   # правая ветка
    turtle.left(2 * angle)                                 # поворот налево
    draw_binary_tree(depth - 1, size / 2, angle, color_by_depth)   # левая ветка
    turtle.right(angle)                                    # выравниваемся обратно
    turtle.backward(size)                                  # возвращаемся в начало


def draw_branch(n: int, size: float, angle: float = 40,
                color_by_depth: bool = True) -> None:
    if color_by_depth:
        turtle.pencolor(depth_color(n))

    turtle.forward(size)              # рисуем саму ветку

    if n > 0:
        turtle.left(angle)
        draw_branch(n - 1, size * 0.6, angle, color_by_depth)   # левая веточка
        turtle.right(angle)
        draw_branch(n - 1, size * 0.7, angle, color_by_depth)   # средняя веточка
        turtle.right(angle)
        draw_branch(n - 1, size * 0.6, angle, color_by_depth)   # правая веточка
        turtle.left(angle)            # выровнялись

    turtle.backward(size)             # вернулись в исходную точку


# ======================================================================
# Роль 2: koch
# ======================================================================
def koch(order: int, size: float) -> None:
    if order == 0:
        draw_line(size)
        return
    koch(order - 1, size / 3)
    turtle.left(60)
    koch(order - 1, size / 3)
    turtle.right(120)
    koch(order - 1, size / 3)
    turtle.left(60)
    koch(order - 1, size / 3)


def koch_snowflake(order: int, size: float) -> None:
    for _ in range(3):
        koch(order, size)
        turtle.right(120)


def minkowski(order: int, size: float) -> None:
    if order == 0:
        draw_line(size)
        return
    part = size / 4
    # последовательность: вперёд, влево, вперёд, вправо, вперёд, вправо,
    # вперёд, вперёд, влево, вперёд, влево, вперёд, вправо, вперёд
    minkowski(order - 1, part)
    turtle.left(90)
    minkowski(order - 1, part)
    turtle.right(90)
    minkowski(order - 1, part)
    turtle.right(90)
    minkowski(order - 1, part)
    minkowski(order - 1, part)
    turtle.left(90)
    minkowski(order - 1, part)
    turtle.left(90)
    minkowski(order - 1, part)
    turtle.right(90)
    minkowski(order - 1, part)


# Высота равностороннего треугольника - пригодится для центрирования
def triangle_height(size: float) -> float:
    return size * math.sqrt(3) / 2


# ======================================================================
# Роль 3: complex
# ======================================================================
"""Роль 3. Сложные фракталы: два "ледяных", кривая Леви, дракон Хартера-Хейтуэя."""



def ice_fractal_1(order: int, size: float) -> None:
    if order == 0:
        draw_line(size)
        return
    part = size / 3
    ice_fractal_1(order - 1, part)       # 1-я часть
    turtle.left(90)
    ice_fractal_1(order - 1, part)       # иголка вверх
    turtle.right(180)
    ice_fractal_1(order - 1, part)       # вернулись вниз на линию
    ice_fractal_1(order - 1, part)       # иголка вниз
    turtle.right(180)
    ice_fractal_1(order - 1, part)       # вернулись вверх на линию
    turtle.right(90)                     # снова смотрим вперёд
    ice_fractal_1(order - 1, part)       # 2-я часть
    ice_fractal_1(order - 1, part)       # 3-я часть


def ice_fractal_2(order: int, size: float, angle: float = 85) -> None:
    if order == 0:
        draw_line(size)
        return
    part = size / (2 + 2 * math.cos(math.radians(angle)))
    ice_fractal_2(order - 1, part, angle)
    turtle.left(angle)
    ice_fractal_2(order - 1, part, angle)
    turtle.right(2 * angle)
    ice_fractal_2(order - 1, part, angle)
    turtle.left(angle)
    ice_fractal_2(order - 1, part, angle)


def levy(order: int, size: float) -> None:
    """Кривая Леви (C-кривая). Отрезок заменяется на два в sqrt(2) раз короче,
    стоящих под прямым углом."""
    if order == 0:
        draw_line(size)
        return
    turtle.left(45)
    levy(order - 1, size / math.sqrt(2))
    turtle.right(90)
    levy(order - 1, size / math.sqrt(2))
    turtle.left(45)


def dragon(order: int, size: float, sign: int = 1) -> None:
    """Дракон Хартера-Хейтуэя (рекурсивная версия).

    sign = 1 или -1 - в какую сторону "ломается" отрезок.
    Второй половинке мы даём противоположный знак - из-за этого линия
    при каждом шаге складывается как лист бумаги.
    """
    if order == 0:
        draw_line(size)
        return
    turtle.left(45 * sign)
    dragon(order - 1, size / math.sqrt(2), 1 * sign)
    turtle.right(90 * sign)
    dragon(order - 1, size / math.sqrt(2), -1 * sign)
    turtle.left(45 * sign)


# ======================================================================
# Роль 4: main
# ======================================================================
"""Фрактальная мастерская - главный файл (Роль 4).

Запуск:  python main.py
Меню -> ввод параметров -> рисование -> возврат в меню.
"""



# ---------------------------------------------------------------- меню
def show_menu() -> None:
    print()
    print("=== ФРАКТАЛЬНАЯ МАСТЕРСКАЯ ===")
    print("1. Двоичное дерево")
    print("2. Фрактал 'Ветка'")
    print("3. Кривая Коха")
    print("4. Снежинка Коха")
    print("5. Кривая Минковского")
    print("6. Ледяной фрактал №1")
    print("7. Ледяной фрактал №2")
    print("8. Кривая Леви")
    print("9. Дракон Хартера-Хейтуэя")
    print("10. Выход")


# ------------------------------------------------- безопасный ввод чисел
def ask_number(prompt: str, kind, low, high, default):
    """Спрашивает число, пока пользователь не введёт правильное.
    Пустой ввод (Enter) = значение по умолчанию."""
    while True:
        raw = input(f"{prompt} [{low}..{high}, Enter = {default}]: ").strip()
        if raw == "":
            return default
        try:
            value = kind(raw.replace(",", "."))
        except ValueError:                       # ввели не число
            print("  Ошибка: нужно ввести число.")
            continue
        if not low <= value <= high:             # число вне диапазона
            print(f"  Ошибка: число должно быть от {low} до {high}.")
            continue
        return value


# Параметры, которые спрашиваем: (ключ, текст вопроса, тип, мин, макс, по умолчанию)
SIZE = ("size", "Длина стороны / размер", float, 10, 600, 200)
SIZE_TREE = ("size", "Длина ствола", float, 10, 300, 120)
SIZE_BRANCH = ("size", "Длина первой ветки", float, 10, 300, 90)
COLOR = ("color", "Цветной режим (1 - да, 0 - нет)", int, 0, 1, 1)


def _depth(max_order: int, default: int):
    return ("order", "Глубина рекурсии", int, 0, max_order, default)


# ---------------------------------------- функции "старта" и рисования
# У каждого фрактала своя стартовая точка, чтобы рисунок был по центру экрана.
def run_binary_tree(p):
    go_to(0, -turtle.window_height() / 2 + 40, 90)       # ствол растёт вверх
    draw_binary_tree(p["order"], p["size"], p["angle"], bool(p["color"]))


def run_branch(p):
    go_to(0, -turtle.window_height() / 2 + 40, 90)
    draw_branch(p["order"], p["size"], p["angle"], bool(p["color"]))


def run_koch(p):
    go_to(-p["size"] / 2, -p["size"] * 0.1, 0)
    koch(p["order"], p["size"])


def run_snowflake(p):
    # Начинаем в левой верхней вершине так, чтобы центр треугольника был в (0, 0)
    s = p["size"]
    go_to(-s / 2, s * math.sqrt(3) / 6, 0)
    koch_snowflake(p["order"], s)


def run_minkowski(p):
    go_to(-p["size"] / 2, 0, 0)
    minkowski(p["order"], p["size"])


def run_ice1(p):
    go_to(-p["size"] / 2, 0, 0)
    ice_fractal_1(p["order"], p["size"])


def run_ice2(p):
    go_to(-p["size"] / 2, -p["size"] * 0.2, 0)
    ice_fractal_2(p["order"], p["size"], p["angle"])


def run_levy(p):
    go_to(-p["size"] / 2, -p["size"] * 0.375, 0)
    levy(p["order"], p["size"])


def run_dragon(p):
    go_to(-p["size"] / 3, -p["size"] / 4, 0)
    dragon(p["order"], p["size"])


ANGLE_TREE = ("angle", "Угол ветвления (градусы)", float, 0, 90, 30)
ANGLE_BRANCH = ("angle", "Угол между веточками (градусы)", float, 0, 90, 40)
ANGLE_ICE = ("angle", "Острота зубца (градусы)", float, 30, 89, 85)

# Номер пункта меню -> (название, параметры, функция запуска)
FRACTALS = {
    "1": ("Двоичное дерево", [_depth(12, 6), SIZE_TREE, ANGLE_TREE, COLOR], run_binary_tree),
    "2": ("Фрактал 'Ветка'", [_depth(8, 5), SIZE_BRANCH, ANGLE_BRANCH, COLOR], run_branch),
    "3": ("Кривая Коха", [_depth(6, 4), SIZE, COLOR], run_koch),
    "4": ("Снежинка Коха", [_depth(6, 4), SIZE, COLOR], run_snowflake),
    "5": ("Кривая Минковского", [_depth(5, 3), SIZE, COLOR], run_minkowski),
    "6": ("Ледяной фрактал №1", [_depth(5, 3), SIZE, COLOR], run_ice1),
    "7": ("Ледяной фрактал №2", [_depth(6, 4), SIZE, ANGLE_ICE, COLOR], run_ice2),
    "8": ("Кривая Леви", [_depth(14, 10), SIZE, COLOR], run_levy),
    "9": ("Дракон Хартера-Хейтуэя", [_depth(14, 10), SIZE, COLOR], run_dragon),
}


def ask_params(choice: str) -> dict:
    title, params_spec, _ = FRACTALS[choice]
    print(f"\n--- {title} ---")
    params = {}
    for key, text, kind, low, high, default in params_spec:
        params[key] = ask_number(text, kind, low, high, default)
    return params


def render(choice: str, params: dict) -> None:
    runner = FRACTALS[choice][2]
    turtle.reset()                       # чистый экран
    init_turtle()
    set_rainbow(params["color"] == 1)
    runner(params)                       # рисуем
    go_to(0, 0, 0)                       # черепашка домой
    turtle.update()                      # показываем всё, что нарисовано
    print("Готово! Рисунок на экране.")


# ------------------------------------------------------- консольный поток

# ------------------------------------------------------- главный поток
def main() -> None:
    setup_window()
    init_turtle()
    turtle.update()

    try:
        while True:
            show_menu()
            choice = input("Выберите пункт меню: ").strip()
            if choice == "10":
                break
            if choice not in FRACTALS:
                print("Нет такого пункта. Введите число от 1 до 10.")
                continue
            params = ask_params(choice)
            try:
                render(choice, params)
            except (turtle.Terminator, turtle.TK.TclError):
                raise
            except Exception as error:
                print(f"Ошибка при рисовании: {error}")
        print("До свидания!")
        turtle.bye()
    except (turtle.Terminator, turtle.TK.TclError, EOFError, KeyboardInterrupt):
        print("\nОкно закрыто. Выход.")


if __name__ == "__main__":
    main()
