import pygame, sys
from pygame.locals import *

class Scene:
    def __init__(self, m, n):
        width = m * PIXEL
        height = n * PIXEL
        self.dimensions = (width, height)

    def getDimensions(self):
        return self.dimensions

    def create_screen(self, dimensions):
        screen = pygame.display.set_mode((self.dimensions))
        pygame.display.set_caption('Artificial Intelligence')
        return screen

    def paint_world(self, screen, matrix):
        x = 0
        y = 0
        screen.fill(WHITE)
        for line in matrix:
            for value in line:
                if value == '0':
                    pygame.draw.rect(screen, GRAY, (x, y, PIXEL, PIXEL), 0)
                if value == '1':
                    pygame.draw.rect(screen, ORANGE_L, (x, y, PIXEL, PIXEL), 0)
                x += PIXEL
            y += PIXEL
            x = 0
        pygame.display.update()