#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *
from Map.Map import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
ORANGE_L = (252, 190, 149)
BLUE = (0, 177, 249)
YELLOW = (255, 190, 65)
GREEN = (146, 209, 101)
DEFAULT = (243, 123, 173)
COLOR_L = (244,110,120)

COLOR_BEIGN = (255, 0, 0)
COLOR_LABEL = (255,0,255)

PIXEL = 30

class Window(object):

    def __init__(self):
        global PIXEL
        pygame.init()
        self.__reloj = pygame.time.Clock()
        self.map = Map()
        dim = self.map.getDimensions()
        self.canvas = pygame.display.set_mode([dim[0]*PIXEL,dim[1]*PIXEL])
        pygame.display.set_caption('Artificial Intelligence')

    def loop(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
            #self.paint()
            pygame.display.flip()
            self.__reloj.tick(7)

    def paint(self):
        global PIXEL
        x=0
        y=0
        for line in self.map.getMatrix():
            for value in line:
                if x == 3*PIXEL and y == 3*PIXEL:
                    global COLOR_BEIGN
                    pygame.draw.rect(self.canvas, COLOR_BEIGN, (x, y, PIXEL, PIXEL), 0)
                elif value == '0':
                    global GRAY
                    pygame.draw.rect(self.canvas, GRAY, (x, y, PIXEL, PIXEL), 0)
                elif value == '1':
                    global ORANGE_L
                    pygame.draw.rect(self.canvas, ORANGE_L, (x, y, PIXEL, PIXEL), 0)
                elif value == '2':
                    global BLUE
                    pygame.draw.rect(self.canvas, BLUE, (x, y, PIXEL, PIXEL), 0)
                elif value == '3':
                    global YELLOW
                    pygame.draw.rect(self.canvas, YELLOW, (x, y, PIXEL, PIXEL), 0)
                elif value == '4':
                    global GREEN
                    pygame.draw.rect(self.canvas, GREEN, (x, y, PIXEL, PIXEL), 0)
                elif value == -1:
                    global BLACK
                    pygame.draw.rect(self.canvas, BLACK, (x, y, PIXEL, PIXEL), 0)
                else:
                    global DEFAULT
                    pygame.draw.rect(self.canvas, DEFAULT, (x, y, PIXEL, PIXEL), 0)
                x += PIXEL
            y += PIXEL
            x = 0

    def ask_terrain(self):
        global COLOR_L
        pos = pygame.mouse.get_pos()
        num = self.world[pos[1]//PIXEL][pos[0]//PIXEL]
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

        self.canvas.blit(label, (pos[0], pos[1]))
        pygame.display.flip()

    def displayInfo(self, string):
        global COLOR_LABEL
        pos = pygame.mouse.get_pos()
        font = pygame.font.SysFont("monospace bold", 16)
        label = font.render(str(string), 1, COLOR_LABEL )
        self.canvas.blit(label, (pos[0]+5, pos[1]-10))
