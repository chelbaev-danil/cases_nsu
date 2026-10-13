"""Класс Button: кликабельная кнопка интерфейса (фон в зависимости
от состояния, наведение мыши, обработка клика)."""

import pygame

from config import COLORS


class Button:
    def __init__(self, rect, label, action, enabled: bool = True, color=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action
        self.enabled = enabled
        self.color = color

    def draw(self, surf, font):
        if not self.enabled:
            bg = COLORS["button_disabled"]
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            bg = COLORS["button_hover"]
        else:
            bg = self.color or COLORS["button"]
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, COLORS["border"], self.rect, width=1, border_radius=8)
        color = COLORS["text"] if self.enabled else COLORS["text_dim"]
        txt = font.render(self.label, True, color)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_click(self, pos) -> bool:
        if self.enabled and self.rect.collidepoint(pos):
            self.action()
            return True
        return False
