#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys
from pygame.locals import *

#Modulos personales
from src.GUI import Scene

# Constantes

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
ORANGE_L = (252, 190, 149)
BLUE = (0, 177, 249)

PIXEL = 30

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
    matrix = read('file.txt')

    m = len(matrix[0])
    n = len(matrix)-1

    scene = Scene(m, n)

    screen = scene.create_screen(scene.getDimensions())

    scene.paint_world(screen, matrix)

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
