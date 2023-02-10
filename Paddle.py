import pygame
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 255)]
class Paddle:

    def __init__(self, x, y, width, height, color=random.choice(colors), VEL = 4):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color
        self.VEL = VEL

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up and self.y > 10:
            self.y -= self.VEL
        elif self.y < (self.original_y*2)-10 and up == False:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
