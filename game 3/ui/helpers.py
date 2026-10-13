"""Мелкие независимые вспомогательные функции интерфейса."""

from models.player import Player


def target_display(target) -> str:
    if isinstance(target, Player):
        return target.name
    return target.name


def wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
