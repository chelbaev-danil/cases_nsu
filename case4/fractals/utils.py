import colorsys
import turtle

_rainbow_on = False   # включён ли радужный режим
_counter = 0          # сколько отрезков уже нарисовано (нужно для смены цвета)


def init_turtle() -> None:
    turtle.colormode(1.0)        # цвета задаём числами от 0 до 1
    turtle.hideturtle()          # саму черепашку не показываем
    turtle.speed(0)              # максимальная скорость
    turtle.tracer(200, 0)        # обновляем экран пачками - так быстрее


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
