"""Роль 3. Сложные фракталы: два "ледяных", кривая Леви, дракон Хартера-Хейтуэя."""
import math
import turtle

from .utils import draw_line


def ice_fractal_1(order: int, size: float) -> None:
    """"Ледяной" фрактал №1 (ледяной крест).

    Отрезок делится на 3 части. В точке между 1-й и 2-й частью вырастает
    "иголка" вверх и вниз - получается крестик, как кристаллик льда.
    Всего 7 кусочков в 3 раза короче: 3 по горизонтали + 4 по вертикали.
    Черепашка в конце возвращается в исходный угол.
    """
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
    """"Ледяной" фрактал №2 (кривая Чезаро - "острая" версия кривой Коха).

    Отрезок заменяется на 4 части. Угол angle = 85 градусов (у Коха было бы 60),
    поэтому "иголка" получается острее и похожа на ледяной зубец.
    Длина одной части: r = size / (2 + 2*cos(angle)) - так конец
    ломаной попадает ровно в конец исходного отрезка.
    """
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
