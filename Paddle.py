import pygame

class Paddle:

    def __init__(self, x, y, width, height, color=(255,255,255), VEL = 4):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color
        self.VEL = VEL

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up=True, VEL=4):
        self.VEL = VEL
        if up and self.y > 10:
            self.y -= self.VEL
        elif self.y < (self.original_y*2)-10 and up == False:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
