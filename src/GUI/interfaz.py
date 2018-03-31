#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, time
from pygame.locals import *

# Constantes

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
ORANGE_L = (252, 190, 149)

PIXEL = 30

# Clases
# ---------------------------------------------------------------------

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
        for line in vector:
            for value in line:
                if value == '0':
                    pygame.draw.rect(screen, GRAY, (x, y, PIXEL, PIXEL), 0)
                if value == '1':
                    pygame.draw.rect(screen, ORGANGE_L, (x, y, PIXEL, PIXEL), 0)
                x += PIXEL
            y += PIXEL
            x = 0
        pygame.display.update()

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
def read(ruta):
    with open(ruta, 'r') as leer:
        contenido = leer.read().split('\n')
    i = 0
    for line in contenido:
        contenido[i] = line.split(',')
        i = i + 1

    leer.close()
    return contenido

# ---------------------------------------------------------------------

def main():
    vector = read('file.txt')

    m = len(matrix[0])
    n = len(matrix)-1

    scene = Scene(m, n)

    screen = scene.create_screen(scene.getDimensions())

    scene.paint_world(screen, vector)

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
