"""Роль 1. Базовые рекурсивные фракталы: двоичное дерево и "Ветка"."""
import turtle

from .utils import depth_color


def draw_binary_tree(depth: int, size: float, angle: float,
                     color_by_depth: bool = True) -> None:
    """Двоичное дерево.

    depth - глубина рекурсии, size - длина ствола, angle - угол ветвления.
    Каждая ветка в 2 раза короче предыдущей.
    После работы черепашка стоит там же и смотрит туда же, где была в начале.
    """
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
    """Фрактал "Ветка": у каждой ветки растут три маленькие веточки
    (налево, прямо и направо).

    n - глубина, size - длина первой ветки, angle - угол между веточками.
    """
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
