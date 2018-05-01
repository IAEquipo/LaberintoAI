#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random, time, graphviz, threading
from subprocess import check_call

from pygame.locals import *
from anytree import Node, RenderTree
from anytree.search import *
from anytree.exporter import DotExporter

#Modulos personales
from GUI.Scene import *
from Archivo.Archivo import *
from BEIGN.Beign import *

# Constantes
PIXEL = 30
# definiciones globales
text = Archivo()
matrix = text.read('lab2.txt')
BD_Char = Archivo()
costs = BD_Char.read('BEIGN/beigns.txt')
reloj = pygame.time.Clock()

m = len(matrix[0])
n = len(matrix)-1

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
    return nodoF

# ---------------------------------------------------------------------

def main(cad, meta, scene, screen):
    posBeign = [0, 0]
    final = meta
    Final = True
    while True:
        y1 = (random.randrange(n-1)) * PIXEL
        x1 = (random.randrange(m-1)) * PIXEL
        posBeign[0] = x1
        posBeign[1] = y1

        if matrix[y1//PIXEL][x1//PIXEL] != "0":
            break

    inicial = [x1,y1]
    beign = Beign(cad, posBeign[0], posBeign[1], costs)
    distancia = abs((final[0]-inicial[0])//PIXEL + (final[1]-inicial[1])//PIXEL)
    raiz = Node(str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->0," + str(distancia))
    padre = raiz
    back = False
    open_node = []
    close_node = []
    scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][3] ="d"
    scene.paint_world(screen, scene.getDarkSide(), 0)
    scene.paint_beign(screen, beign.getX, beign.getY)
    open_node.append(raiz)
    print("inicio {}: {}, {}".format(cad, inicial[0]//PIXEL, inicial[1]//PIXEL))
    print("final {}: {}, {}".format(cad, final[0]//PIXEL, final[1]//PIXEL))

    while True:
        print("x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))
        scene.print_darkside()
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
            if (Final):
                Final = False
                distancia = abs((final[0]-beign.getX)//PIXEL + (final[1]-beign.getY)//PIXEL)
                total = beign.getCostT + distancia
                padre = Node(str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "," + str(total), parent=padre)
                ruta = str(padre).split("'")[1]
                DotExporter(raiz).to_dotfile(str(cad)+".dot")
                check_call(['dot','-Tpng',str(cad)+'.dot','-o',str(cad)+'.png'])
                print(cad)
                print(RenderTree(raiz))
                print("Ruta: \t{}".format(ruta))
            return
        if(back):
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])

        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0) and beign.LEFT(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"L"),0)):
            scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][4] = 0
            beign.LEFT(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"L"),1)
            flagChild = False
            back = False
        elif(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0) and beign.UP(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"U"),0)):
            scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][4] = 0
            beign.UP(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"U"),1)
            flagChild = False
            back = False
        elif(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0) and beign.DOWN(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"D"),0)):
            scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][4] = 0
            beign.DOWN(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"D"),1)
            flagChild = False
            back = False
        elif(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0) and beign.RIGHT(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"R"),0)):
            scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][4] = 0
            beign.RIGHT(scene.getMap(beign.getX//PIXEL, beign.getY//PIXEL,"R"),1)
            flagChild = False
            back = False
            flagChild = True
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
        #print("Decision: {}".format(Decision))
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
        #i += 1
        pygame.display.flip()
        reloj.tick(15)


if __name__ == '__main__':
    pygame.init()

    scene1 = Scene(m, n)
    screen1 = scene1.create_screen(scene1.getDimensions())
    scene1.paint_world(screen1, matrix, 1)
    scene1.copy_world(m, n)
    scene1.paint_world(screen1, scene1.getDarkSide(), 0)

    scene2 = Scene(m, n)
    screen2 = scene2.create_screen(scene2.getDimensions())
    scene2.paint_world(screen2, matrix, 1)
    scene2.copy_world(m, n)
    scene2.paint_world(screen2, scene2.getDarkSide(), 0)

    meta1 = [0*PIXEL,0*PIXEL]
    meta2 = [14*PIXEL,14*PIXEL]
    main('Octopus',meta1, scene1, screen1)
    main('Human',meta2, scene2, screen2)
    #h1 = threading.Thread(target=main, args=('Octopus',meta1, scene1, screen1), name='Octopus')
    #h2 = threading.Thread(target=main, args=('Human',meta2, scene2, screen2), name='Human')
    #h1.start()
    #h2.start()
    #h1.join()
    #h2.join()
