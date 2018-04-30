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
# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
def min(nodos):
    nodoF = nodos[0]
    min = int(str(nodoF).split("/")[-1].split(",")[-1].split("'")[0])
    for nodo in nodos:
        actual = int(str(nodo).split("/")[-1].split(",")[-1].split("'")[0])
        if(actual < min):
            nodoF = nodo
    return nodo

# ---------------------------------------------------------------------

def main():
    text = Archivo()
    matrix = text.read('file.txt')
    BD_Char = Archivo()
    costs = BD_Char.read('BEIGN/beigns.txt')

    m = len(matrix[0])
    n = len(matrix)-1

    scene = Scene(m, n)
    screen = scene.create_screen(scene.getDimensions())
    scene.paint_world(screen, matrix, 1)
    scene.copy_world(m, n)
    scene.paint_world(screen, scene.getDarkSide(), 0)
    posBeign = [0, 0]
    final = [0,0]

    while True:
        y1 = (random.randrange(n-1)) * PIXEL
        x1 = (random.randrange(m-1)) * PIXEL
        y2 = (random.randrange(n-1)) * PIXEL
        x2 = (random.randrange(m-1)) * PIXEL

        posBeign[0] = x1
        posBeign[1] = y1
        final[0] = x2
        final[1] = y2

        if matrix[y1//PIXEL][x1//PIXEL] != "0" and matrix[y2//PIXEL][x2//PIXEL] != "0":
            break

    inicial = [x1,y1]
    beign = Beign('Human', posBeign[0], posBeign[1], costs)
    distancia = abs((final[0]-inicial[0])//PIXEL + (final[1]-inicial[1])//PIXEL)
    raiz = Node(str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->0," + str(distancia))
    padre = raiz
    back = False
    open_node = []
    close_node = []
    scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][3] ="d"
    reloj = pygame.time.Clock()
    scene.paint_world(screen, scene.getDarkSide(), 0)
    scene.paint_beign(screen, beign.getX, beign.getY)
    open_node.append(raiz)
    print("inicio: {}, {}".format(inicial[0]//PIXEL, inicial[1]//PIXEL))
    print("final: {}, {}".format(final[0]//PIXEL, final[1]//PIXEL))

    while True:
        if(pygame.mouse.get_pressed()[0] != 0):
            scene.ask_terrain(screen)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
        scene.paint_world(screen, matrix, 1)

        if(pygame.mouse.get_pressed()[2] != 0):
            scene.change_terrain()
            scene.paint_world(screen, matrix, 1)

        if(beign.getX == final[0] and beign.getY == final[1]):
            distancia = abs((final[0]-beign.getX)//PIXEL + (final[1]-beign.getY)//PIXEL)
            total = beign.getCostT + distancia
            padre = Node(str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "," + str(total), parent=padre)
            ruta = str(padre).split("'")[1]
            print("Ruta: \t{}".format(ruta))
            time.sleep(60)
            continue
        if(back):
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.LEFT(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            flagChild = False
            back = False
        elif(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.UP(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            flagChild = False
            back = False
        elif(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.DOWN(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            flagChild = False
            back = False
        elif(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.RIGHT(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            flagChild = False
            back = False
        else:
            if(back):
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
                close_node.append(padre)
                open_node.remove(padre)
                padre = min(open_node)
            else:
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])

        Decision = 0
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        if(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        if(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        if(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,1)):
            Decision = Decision + 1

        Actual = "a"
        Shadow = scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][0]

        if Decision > 2:
            d = "d"
            if (flagChild == False):
                back = True
                distancia = abs((final[0]-beign.getX)//PIXEL + (final[1]-beign.getY)//PIXEL)
                total = beign.getCostT + distancia
                padre = Node(str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "," + str(total), parent=padre)
                flagChild = True
                open_node.append(padre)
                padre = padre.parent

        elif Decision == 1:
            d = 0
            if (flagChild == False):
                back = True
                distancia = abs((final[0]-beign.getX)//PIXEL + (final[1]-beign.getY)//PIXEL)
                total = beign.getCostT + distancia
                padre = Node(str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "," + str(total), parent=padre)
                flagChild = True
                padre = padre.parent
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
        reloj.tick(15)


if __name__ == '__main__':
    pygame.init()
    main()
