#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random, time
from pygame.locals import *
from anytree import Node, RenderTree, search
from anytree.dotexport import RenderTreeGraph

#Modulos personales
from GUI.Scene import *
from Archivo.Archivo import *
from BEIGN.Beign import *

# Constantes
PIXEL = 30
# definiciones globales


text = Archivo()
matrix = text.read('file.txt')
BD_Char = Archivo()
costs = BD_Char.read('BEIGN/beigns.txt')
reloj = pygame.time.Clock()

m = len(matrix[0])
n = len(matrix)-1

scene = Scene(m, n)
screen = scene.create_screen(scene.getDimensions())
scene.paint_world(screen, matrix, 1)
scene.copy_world(m, n)
scene.paint_world(screen, scene.getDarkSide(), 0)
posBeign = [0, 0]
while True:
    x = (random.randrange(m-1)) * PIXEL
    y = (random.randrange(n-1)) * PIXEL

    x = 3 * PIXEL
    y = 3 * PIXEL

    posBeign[0] = x
    posBeign[1] = y

    if matrix[y//PIXEL][x//PIXEL] != "0":
        break

inicial = [x,y]
beign = Beign('Human', posBeign[0], posBeign[1], costs)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
# def move(flag):

# def ask():
# ---------------------------------------------------------------------

def anchura(nodo):
    x = str(nodo).split("/")[-1].split(",")[0]
    y = str(nodo).split("/")[-1].split(",")[1].split("->")[0]
    beign.setX(int(x)*PIXEL)
    beign.setY(int(y)*PIXEL)
    beign.setCostT(str(nodo).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
    padre = nodo
    back = False
    forward = False
    flagChild = False
    while(True):
        if(pygame.mouse.get_pressed()[0] != 0):
            scene.ask_terrain(screen)

        #print("x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
        scene.paint_world(screen, matrix, 1)

        if(pygame.mouse.get_pressed()[2] != 0):
            scene.change_terrain()
            scene.paint_world(screen, matrix, 1)

        if(back):
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
            if(padre.is_root):
                return

        #print("1. {}".format(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("2. {}".format(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("3. {}".format(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("4. {}".format(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.LEFT(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        elif(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.UP(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        elif(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.DOWN(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        elif(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.RIGHT(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        else:
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])

            if(forward):
                for i in range(len(padre.children)):
                    #print("for de main: {}".format(i))
                    forward = True
                    anchura(padre.children[i])
                forward = False
            elif(padre.is_root):
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
            elif(back):
                padre = padre.parent
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
                forward = False
            else:
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                back = True

        Decision = 0
        #print("L: {}".format(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        #print("U: {}".format(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        #print("D: {}".format(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        #print("R: {}".format(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        Actual = "a"
        Shadow = scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][0]

        #print("Decision: {}".format(Decision))
        if(Decision > 2):
            d = "d"
            if (flagChild == True):
                flagChild = False
                hijo = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
                padre  = hijo.parent
                back = True
                #print(RenderTree(raiz))
        elif(Decision == 1):
            d = 0
            hijo = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
            padre = hijo.parent
            back = True
            print(RenderTree(nodo))
        else:
            d = 0

        scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL] = [Shadow,0,"v",d,Actual]

        scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][1]="i"
        scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][3]="d"
        scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][2]="v"

        scene.paint_world(screen, scene.getDarkSide(), 0)
        scene.paint_beign(screen, beign.getX, beign.getY)
        etiqueta = pygame.mouse.get_pos()
        string = "{0}"
        if (etiqueta[0] <= scene.getDimensions()[0] and etiqueta[1] <= scene.getDimensions()[1]):
            scene.displayInfo(screen, string.format(scene.getDarkSide()[etiqueta[1]//PIXEL][etiqueta[0]//PIXEL]))
        pygame.display.flip()
        reloj.tick(1)




def main():
    back = False
    raiz = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->0")
    padre = raiz
    scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][3] ="d"

    Temp = 0
    forward = True
    scene.paint_world(screen, scene.getDarkSide(), 0)
    scene.paint_beign(screen, beign.getX, beign.getY)

    while True:
        if(pygame.mouse.get_pressed()[0] != 0):
            scene.ask_terrain(screen)

        #print("x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
        scene.paint_world(screen, matrix, 1)

        if(pygame.mouse.get_pressed()[2] != 0):
            scene.change_terrain()
            scene.paint_world(screen, matrix, 1)

        if(back):
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])

        #print("1. {}".format(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("2. {}".format(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("3. {}".format(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("4. {}".format(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.LEFT(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        elif(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.UP(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        elif(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.DOWN(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        elif(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.RIGHT(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            flagChild = True
        else:
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])

            if(padre.is_root):
                print(padre.children)
                for i in range(len(padre.children)):
                    print("for de main: {}".format(i))
                    forward = True
                    anchura(padre.children[i])
                forward = False
            elif(back):
                padre = padre.parent
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
                forward = False
            else:
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                back = True

        Decision = 0
        #print("L: {}".format(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        #print("U: {}".format(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        #print("D: {}".format(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        #print("R: {}".format(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,1)))
        if(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        Actual = "a"
        Shadow = scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][0]

        #print("Decision: {}".format(Decision))
        if(Decision > 2):
            d = "d"
            if (flagChild == True):
                flagChild = False
                hijo = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
                padre  = hijo.parent
                back = True
                #print(RenderTree(raiz))
        elif(Decision == 1):
            d = 0
            hijo = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
            padre = hijo.parent
            back = True
            print(RenderTree(raiz))
        else:
            d = 0

        scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL] = [Shadow,0,"v",d,Actual]

        scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][1]="i"
        scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][3]="d"
        scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][2]="v"

        scene.paint_world(screen, scene.getDarkSide(), 0)
        scene.paint_beign(screen, beign.getX, beign.getY)
        etiqueta = pygame.mouse.get_pos()
        string = "{0}"
        if (etiqueta[0] <= scene.getDimensions()[0] and etiqueta[1] <= scene.getDimensions()[1]):
            scene.displayInfo(screen, string.format(scene.getDarkSide()[etiqueta[1]//PIXEL][etiqueta[0]//PIXEL]))
        pygame.display.flip()
        reloj.tick(1)


if __name__ == '__main__':
    pygame.init()
    main()
