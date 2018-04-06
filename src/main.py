#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random
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
# def move(flag):

# def ask():
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
    lastDecision = "0,0->0"
    posBeignLast = [0, 0]
    padre = None

    while True:
        x = (random.randrange(m-1)) * PIXEL
        y = (random.randrange(n-1)) * PIXEL

        x = 4 * PIXEL
        y = 3 * PIXEL

        posBeign[0] = x
        posBeign[1] = y

        if matrix[y//PIXEL][x//PIXEL] != "0":
            break

    inicial = [x,y]
    beign = Beign('Human', posBeign[0], posBeign[1], costs)
    lastDecision = "" + str(posBeign[0]//PIXEL) + "," + str(posBeign[1]//PIXEL) + "->" + str(beign.getCostT) + ""
    raiz = Node(lastDecision)
    scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][3] ="d"
    reloj = pygame.time.Clock()
    Temp = 0

    while True:

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
        scene.paint_world(screen, matrix, 1)

        if(pygame.mouse.get_pressed()[2] != 0):
            scene.change_terrain()
            scene.paint_world(screen, matrix, 1)

        if((beign.getY-PIXEL > 0) and (scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL) != '0') and (scene.getDarkSide()[(beign.getY-PIXEL)//PIXEL][beign.getX//PIXEL][2] != 'v')):
            posBeignLast[0]=beign.getX//PIXEL
            posBeignLast[1]=beign.getY//PIXEL
            beign.UP(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL),1)
            flagChild = False
        else:
            Temp += 1

        if((beign.getY+PIXEL < scene.getDimensions()[1]) and (scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL) != '0') and (scene.getDarkSide()[(beign.getY+PIXEL)//PIXEL][beign.getX//PIXEL][2] != 'v')):
            posBeignLast[0]=beign.getX//PIXEL
            posBeignLast[1]=beign.getY//PIXEL
            beign.DOWN(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL),1)
            flagChild = False
        else:
            Temp += 1

        if((beign.getX+PIXEL < scene.getDimensions()[0]) and (scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL) != '0') and (scene.getDarkSide()[beign.getY//PIXEL][(beign.getX+PIXEL)//PIXEL][2] != 'v')):
            posBeignLast[0]=beign.getX//PIXEL
            posBeignLast[1]=beign.getY//PIXEL
            beign.RIGHT(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL),1)
            flagChild = False
        else:
            Temp += 1

        if((beign.getX-PIXEL > 0) and (scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL) != '0') and (scene.getDarkSide()[beign.getY//PIXEL][(beign.getX-PIXEL)//PIXEL][2] != 'v')):
            posBeignLast[0]=beign.getX//PIXEL
            posBeignLast[1]=beign.getY//PIXEL
            beign.LEFT(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL),1)
            flagChild = False
        else:
            Temp += 1

        if(Temp == 4):
            Temp = 0
            print("ALv PRRO ALV")
            if(lastDecision == None):
                x = inicial[0]
                y = inicial[1]
            else:
                x = lastDecision.split(",")[0]
                y = lastDecision.split(",")[1].split("->")[0]
            beign.setX(int(x)*PIXEL)
            beign.setY(int(y)*PIXEL)
            if(padre != None ):
                aux = str(padre).split("/")[-1][:-2]
                lastDecision = aux
            else:
                lastDecision = "" + str(inicial[0]//PIXEL) + "," + str(inicial[1]//PIXEL) + "->0"


        else:
            Temp = 0

            if(pygame.mouse.get_pressed()[0] != 0):
                scene.ask_terrain(screen)

            Decision = 0

            if(scene.askUP(beign.getX//PIXEL, beign.getY//PIXEL) != "0"):
                Decision = Decision + 1
            if(scene.askDOWN(beign.getX//PIXEL, beign.getY//PIXEL) != "0"):
                Decision = Decision + 1
            if(scene.askRIGHT(beign.getX//PIXEL, beign.getY//PIXEL) != "0"):
                Decision = Decision + 1
            if(scene.askLEFT(beign.getX//PIXEL, beign.getY//PIXEL) != "0"):
                Decision = Decision + 1

            Visited = "v"

            scene.getDarkSide()[posBeignLast[1]][posBeignLast[0]][4] = 0
            Actual = "a"
            Shadow = scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL][0]

            if(Decision > 2):
                d = "d"
                if flagChild == False:
                    padre = search.find(raiz, lambda node: node.name == lastDecision)
                    print(padre)
                    if(padre.parent == None):
                        padre = raiz
                    elif(padre == None):
                        pass
                    Node("" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + "", parent=padre)
                    flagChild = True
                    lastDecision = "" + str(beign.getX//PIXEL) + "," + str(beign.getY//PIXEL) + "->" + str(beign.getCostT) + ""
                    print(RenderTree(raiz))
            else:
                d = 0

            scene.getDarkSide()[beign.getY//PIXEL][beign.getX//PIXEL] = [Shadow,0,Visited,d,Actual]

            scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][1]="i"
            scene.getDarkSide()[inicial[1]//PIXEL][inicial[0]//PIXEL][3]="d"

        etiqueta = pygame.mouse.get_pos()
        string = "{0}"
        if (etiqueta[0] <= scene.getDimensions()[0] and etiqueta[1] <= scene.getDimensions()[1]):
            scene.displayInfo(screen, string.format(scene.getDarkSide()[etiqueta[1]//PIXEL][etiqueta[0]//PIXEL]))

        scene.paint_world(screen, scene.getDarkSide(), 0)
        scene.paint_beign(screen, beign.getX, beign.getY)
        pygame.display.flip()
        reloj.tick(1)


if __name__ == '__main__':
    pygame.init()
    main()
