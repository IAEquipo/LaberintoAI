#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys
from pygame.locals import *


#Modulos personales
from GUI.Scene import *
from Archivo.Archivo import *

# Constantes


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------

def main():
    texto = Archivo()
    matrix = texto.read('file.txt')
    m = len(matrix[0])
    n = len(matrix)-1

    scene = Scene(m, n)
    screen = scene.create_screen(scene.getDimensions())
    scene.paint_world(screen, matrix, 1)


    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
        scene.paint_world(screen, matrix, 1)

        if(pygame.mouse.get_pressed()[0] != 0):
            scene.ask_terrain(screen)
        if(pygame.mouse.get_pressed()[2] != 0):
            scene.change_terrain()
            scene.paint_world(screen, matrix, 1)


if __name__ == '__main__':
    pygame.init()
    main()
