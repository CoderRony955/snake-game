import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
FPS = 7

# Visual settings
SNAKE_RADIUS = GRID_SIZE // 2
FOOD_RADIUS = GRID_SIZE // 2 - 2
SHINE_RADIUS = FOOD_RADIUS // 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
GRID_COLOR = (40, 40, 40)
BUTTON_COLOR = (50, 120, 190)
BUTTON_HOVER_COLOR = (70, 140, 210)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 36)
        self.is_hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False
