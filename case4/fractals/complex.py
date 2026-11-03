"""Роль 3. Сложные фракталы: два "ледяных", кривая Леви, дракон Хартера-Хейтуэя."""
import math
import turtle

from .utils import draw_line


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
    if order == 0:
        draw_line(size)
        return
    turtle.left(45)
    levy(order - 1, size / math.sqrt(2))
    turtle.right(90)
    levy(order - 1, size / math.sqrt(2))
    turtle.left(45)


def dragon(order: int, size: float, sign: int = 1) -> None:
    if order == 0:
        draw_line(size)
        return
    turtle.left(45 * sign)
    dragon(order - 1, size / math.sqrt(2), 1 * sign)
    turtle.right(90 * sign)
    dragon(order - 1, size / math.sqrt(2), -1 * sign)
    turtle.left(45 * sign)
