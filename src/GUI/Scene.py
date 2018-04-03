import pygame, sys
from pygame.locals import *

# Constantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
ORANGE_L = (252, 190, 149)
BLUE = (0, 177, 249)
YELLOW = (255, 190, 65)
GREEN = (146, 209, 101)

COLOR_L = (244,110,120)

PIXEL = 30


def paint_coord(screen, x, y):
    if x == 0 and y ==0 or x == 0 and y !=0 or x != 0 and y == 0:
        pygame.draw.rect(screen, BLACK, (x, y, PIXEL, PIXEL))


class Scene:
    darkside = []
    world = []

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

    def paint_world(self, screen, matrix, flag):
        if flag == 0:
            self.darkside = matrix
        if flag == 1:
            self.world = matrix

        x = 0
        y = 0

        screen.fill(WHITE)
        for line in matrix:
            #paint_coord(screen, x, y)
            #x += PIXEL
            for value in line:
                #if y == 0:
                    #paint_coord(screen, x, y)
                    #y += PIXEL
                #if flag == 0:

                if value == '0':
                    pygame.draw.rect(screen, GRAY, (x, y, PIXEL, PIXEL), 0)
                elif value == '1':
                    pygame.draw.rect(screen, ORANGE_L, (x, y, PIXEL, PIXEL), 0)
                elif value == '2':
                    pygame.draw.rect(screen, BLUE, (x, y, PIXEL, PIXEL), 0)
                elif value == '3':
                    pygame.draw.rect(screen, YELLOW, (x, y, PIXEL, PIXEL), 0)
                elif value == '4':
                    pygame.draw.rect(screen, GREEN, (x, y, PIXEL, PIXEL), 0)
                x += PIXEL
            y += PIXEL
            x = 0
        pygame.display.update()

    def ask_terrain(self, screen):
        pos = pygame.mouse.get_pos()
        num = self.world[pos[1]/PIXEL][pos[0]/PIXEL]
        font = pygame.font.SysFont('comicsansms', 30)

        if num == '0':
            label = font.render("Mountain", 1, COLOR_L)
        elif num == '1':
            label = font.render("Earth", 1, COLOR_L)
        elif num == '2':
            label = font.render("Water", 1, COLOR_L)
        elif num == '3':
            label = font.render("Sand", 1, COLOR_L)
        elif num == '4':
            label = font.render("Forest", 1, COLOR_L)

        screen.blit(label, (pos[0], pos[1]))
        pygame.display.flip()
