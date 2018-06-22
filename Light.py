from collections import namedtuple
from OpenGL.GL import *

import Util

Pos = namedtuple("Pos", ['x', 'y', 'z', 'inf'])
Color = namedtuple("Color", ['r', 'g', 'b'])
Light = namedtuple("Light", ['r', 'g', 'b', 'a'])

# guarda as contstantes do OpenGL
LIGHTS = (GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3, GL_LIGHT4, GL_LIGHT5, GL_LIGHT6, GL_LIGHT7)
count = -1  # guarda as luzes criadas

# define lights   # tipos das listas
lights = list()   # bool (on/off)
ambient = list()  # Light
diffuse = list()  # Light
specular = list() # Light
positions = list()# Pos

AMBIENT = Light(0.1, 0.1, 0.1, 0.5)
SPECULARITY = Light(1.0, 1.0, 1.0, 1.0)
matSpecularity = 64


def createLight(pos, amb, dif, spec, on=True):
    global count
    count += 1
    positions.append(pos)
    lights.append(on)
    ambient.append(amb)
    diffuse.append(dif)
    specular.append(spec)


def handleLighting():
    # Define os parâmetros para cada uma das luzes
    for i in range(len(lights)):
        glLightfv(LIGHTS[i], GL_AMBIENT, ambient[i])
        glLightfv(LIGHTS[i], GL_DIFFUSE, diffuse[i])
        glLightfv(LIGHTS[i], GL_SPECULAR, specular[i])
        glLightfv(LIGHTS[i], GL_POSITION, positions[i])
        if lights[i]:
            glEnable(LIGHTS[i])


def prepareLighting():
    glShadeModel(GL_SMOOTH)  # Habilita o modelo de colorização de Gouraud
    glMaterialfv(GL_FRONT, GL_SPECULAR, SPECULARITY)  # Define a refletância do material
    glMateriali(GL_FRONT, GL_SHININESS, matSpecularity)  # Define a concentração do brilho
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, AMBIENT)  # Ativa o uso da luz ambiente
    glEnable(GL_COLOR_MATERIAL)  # Habilita a definição da cor do material a partir da cor corrente
    glEnable(GL_LIGHTING)  # Habilita o uso de iluminação
    glEnable(GL_DEPTH_TEST)  # Habilita o depth-buffering


def setupLighting():
    Util.addLight(
        Pos(0.0, 150.0, 0.0, 1.0),  # position
        Light(0.4, 0.4, 0.4, 1.0),  # ambient
        Light(0.5, 0.5, 0.5, 1.0),  # diffuse
        Light(0.1, 0.1, 0.1, 1.0)  # specular
    )
    Util.addLight(
        Pos(35.0, 50.0, 0.0, 1),
        Light(0.8, 0.4, 0.4, 1),
        Light(1.0, 0.2, 0.2, 1),
        Light(0.9, 0.3, 0.3, 1),
        False
    )
    Util.addLight(
        Pos(-35.0, 50.0, -35.0, 1),
        Light(0.4, 0.8, 0.4, 1),
        Light(0.2, 1.0, 0.2, 1),
        Light(0.3, 0.9, 0.3, 1),
        False
    )
    Util.addLight(
        Pos(-35.0, 50.0, 35.0, 1),
        Light(0.4, 0.4, 0.8, 1),
        Light(0.2, 0.2, 1.0, 1),
        Light(0.3, 0.3, 0.9, 1),
        False
    )



    prepareLighting()
    handleLighting()


def disableLight(light):
    glDisable(LIGHTS[light])


def enableLight(light):
    glEnable(LIGHTS[light])


def toggleLight(light):
    if light >= len(lights):
        return

    if lights[light]:
        disableLight(light)
        lights[light] = False
    else:
        enableLight(light)
        lights[light] = True

