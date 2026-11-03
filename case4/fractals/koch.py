"""Роль 2. Кривая Коха, снежинка Коха и кривая Минковского."""
import math
import turtle

from .utils import draw_line


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


def triangle_height(size: float) -> float:
    return size * math.sqrt(3) / 2
