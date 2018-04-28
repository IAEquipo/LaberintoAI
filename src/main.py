#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random, time
from pygame.locals import *
from anytree import Node, RenderTree
from anytree.search import *
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
    i = 0
    x = str(nodo).split("/")[-1].split(",")[0]
    y = str(nodo).split("/")[-1].split(",")[1].split("->")[0]
    beign.setX(int(x)*PIXEL)
    beign.setY(int(y)*PIXEL)
    beign.setCostT(str(nodo).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
    padre = nodo
    back = False
    forward = True
    flagChild = False

    #print("Nodo raiz de anchura: {}".format(padre))

    while(True):
        #print("Iteracion: {}".format(i))
        if(pygame.mouse.get_pressed()[0] != 0):
            scene.ask_terrain(screen)

        #print("x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
        scene.paint_world(screen, matrix, 1)

        #print(padre)

        if(pygame.mouse.get_pressed()[2] != 0):
            scene.change_terrain()
            scene.paint_world(screen, matrix, 1)

        if(back):
            #print(padre)
            flagChild = False
            try:
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
                #print(" Regresa x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))
                forward = False
            except AttributeError:
                forward = True
                back = False
                return

        #print("1. {}".format(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("2. {}".format(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("3. {}".format(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        #print("4. {}".format(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)))
        if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.LEFT(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            forward = True
            flagChild = True
        elif(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.UP(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            forward = True
            flagChild = True
        elif(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.DOWN(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            forward = True
            flagChild = True
        elif(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0)):
            beign.RIGHT(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL,0),1)
            back = False
            forward = True
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
                back = True
            elif(padre.is_root):
                return
            elif(back):
                padre = padre.parent
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
                forward = False
                back = True
            else:
                x = str(padre).split("/")[-1].split(",")[0]
                y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
                beign.setX(int(x)*PIXEL)
                beign.setY(int(y)*PIXEL)
                back = True
                forward = False

        #print("x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))

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

        #print("Decision: {}".format(Decision))
        #print("is_root: {}".format(padre.is_root))
        if(Decision > 2):
            d = "d"
            if (flagChild == True):
                flagChild = False
                #print("find: {}".format(findall(padre, lambda node: node.name == "" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "")))
                if (findall(padre, lambda node: node.name == "" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "") != None):
                    #print("D2 -> 1:{}".format(padre))
                    aux = str(padre).split("/")[-1].split("->")[0]
                    #print("aux: {}".format(aux))
                    #print("cad: {}".format("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + ""))
                    if(("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "") != aux):
                        padre = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
                        padre  = padre.parent
                        #print("D2 -> 2:{}".format(padre))
                back = True
                forward = False
                #print(RenderTree(raiz))
        elif(Decision == 1 and not padre.is_root):
            d = 0
            #print("find: {}".format(findall(padre, lambda node: node.name == "" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "")))
            if (flagChild == True):
                flagChild = False
                if (findall(padre, lambda node: node.name == "" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "") != None):
                    #print("D1 -> 1:{}".format(padre))
                    aux = str(padre).split("/")[-1].split("->")[0]
                    #print("aux: {}".format(aux))
                    #print("cad: {}".format("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + ""))
                    if(("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "") != aux):
                        padre = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
                        padre = padre.parent
                        #print("D1 -> 2:{}".format(padre))
                back = True
                forward = False
                #print(RenderTree(nodo))
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
        i += 1
        pygame.display.flip()
        reloj.tick(1)



def main():
    back = False
    forward = True
    #i = 0
    raiz = Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->0")
    padre = raiz
    scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][3] ="d"
    #Temp = 0

    scene.paint_world(screen, scene.getDarkSide(), 0)
    scene.paint_beign(screen, beign.getX, beign.getY)

    while True:
        #print(i)
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
            #print(padre)
            x = str(padre).split("/")[-1].split(",")[0]
            y = str(padre).split("/")[-1].split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            beign.setCostT(str(padre).split("/")[-1].split(",")[1].split("->")[1].split("'")[0])
            flagChild = False
            #print(" Regresa x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))

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
                #print(padre.children)
                for i in range(len(padre.children)):
                    #print("for de main: {}".format(i))
                    forward = True
                    anchura(padre.children[i])
                print(RenderTree(raiz))
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

        #print("x: {}\ty: {}".format(beign.getX//PIXEL, beign.getY//PIXEL))
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
            #print(RenderTree(raiz))
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
        reloj.tick(1)


if __name__ == '__main__':
    pygame.init()
    main()
