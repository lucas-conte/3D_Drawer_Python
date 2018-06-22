from OpenGL.GL import *
from OpenGL.GLUT import *
from collections import namedtuple

import Light, Primitives

# defines
LIGHT_SCALE = 0.1

# define namedtuples
XYZ = namedtuple("XYZ", ['x', 'y', 'z'])
Color = namedtuple("Color", ['r', 'g', 'b'])
OBJ = namedtuple('OBJ', ['type', 'x', 'y', 'z', 'X', 'Y', 'Z', 'tex'])
L = Light.Light
P = Light.Pos

# define colors
white = Color(1.0, 1.0, 1.0)
red   = Color(1.0, 0.0, 0.0)
green = Color(0.0, 1.0, 0.0)
blue  = Color(0.0, 0.0, 1.0)

# lights
lightsPos = list()
lightsColor = list()

# define OBJ types
BOX = 0
SPHERE = 1
PYRAMID = 2


def drawObj(obj: OBJ):
    if obj.type == BOX:
        box(obj.tex, obj.x, obj.y, obj.z, obj.X, obj.Y, obj.Z)
        return
    if obj.type == SPHERE:
        sphere(obj.tex, obj.x, obj.y, obj.z, obj.X, obj.Y, obj.Z)
        return
    if obj.type == PYRAMID:
        pyramid(obj.tex, obj.x, obj.y, obj.z, obj.X, obj.Y, obj.Z)
        return


def drawMesh(x, y, z, X, Y, Z, texture, vertices, faces, uvs):
    glColor(white)
    glBegin(GL_TRIANGLES)
    i = 0
    for face in faces:
        j = 0
        for vertex in face:
            if texture:
                glTexCoord2f(uvs[i][j].u, uvs[i][j].v)
            glVertex3f(vertices[vertex].x * X + x,
                       vertices[vertex].y * Y + y,
                       vertices[vertex].z * Z + z)
            j += 1
        i += 1

    glEnd()


def box(texId=0, posX=0, posY=0, posZ=0, scaleX=10, scaleY=10, scaleZ=10):
    if not texId:
        simpleBox(posX, posY, posZ, scaleX, scaleY, scaleZ)
        return
    posY += 10
    vertices = Primitives.cubeV
    faces = Primitives.cubeF
    uvs = Primitives.cubeT

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texId)
    drawMesh(posX, posY, posZ, scaleX, scaleY, scaleZ, True, vertices, faces, uvs)
    glDisable(GL_TEXTURE_2D)


def pyramid(texId=0, posX=0, posY=0, posZ=0, scaleX=10, scaleY=10, scaleZ=10):
    if not texId:
        simplePyramid(posX, posY, posZ, scaleX, scaleY, scaleZ)
        return
    vertices = Primitives.pyramidV
    faces = Primitives.pyramidF
    uvs = Primitives.pyramidT

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texId)
    drawMesh(posX, posY, posZ, scaleX, scaleY, scaleZ, True, vertices, faces, uvs)
    glDisable(GL_TEXTURE_2D)


def sphere(texId=0, posX=0, posY=0, posZ=0, scaleX=1, scaleY=1, scaleZ=1, color=white, quality=16):
    if texId:
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glBindTexture(GL_TEXTURE_2D, texId)
    simpleSphere(posX, posY, posZ, scaleX, scaleY, scaleZ)
    if texId:
        glDisable(GL_TEXTURE_GEN_S)
        glDisable(GL_TEXTURE_GEN_T)
        glDisable(GL_TEXTURE_2D)


def simpleBox(posX=0.0, posY=0.0, posZ=0.0, scaleX=1.0, scaleY=1.0, scaleZ=1.0, color=white):
    glColor(color)
    glPushMatrix()
    glScalef(scaleX, scaleY, scaleZ)
    # o translate é dividido pela escala para garantir consistencia no translate
    glTranslatef(posX / scaleX, (posY + 10) / scaleY, posZ / scaleZ)
    glutSolidCube(2)
    glPopMatrix()


def simpleSphere(posX=0, posY=0, posZ=0, scaleX=1, scaleY=1, scaleZ=1, color=white, quality=16):
    glColor(color)
    glPushMatrix()
    glScalef(scaleX * 10, scaleY * 10, scaleZ * 10)
    glTranslatef((posX / 10) / scaleX, (posY / 10) / scaleY, (posZ / 10) / scaleZ)
    glutSolidSphere(1, quality, quality)
    glPopMatrix()


def simplePyramid(posX=0, posY=0, posZ=0, scaleX=1, scaleY=1, scaleZ=1, color=white):
    glColor(color)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glScalef(scaleX, scaleZ, scaleY)
    glTranslatef(posX / scaleX, -posZ / scaleZ, posY / scaleY)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1.5, 1, 4, 1)
    glPopMatrix()


def simpleCylinder(posX=0, posY=0, posZ=0, scaleX=1, scaleY=1, scaleZ=1, color=white, quality=8):
    glColor(color)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glScalef(scaleX, scaleZ, scaleY)
    glTranslatef((posX / 10) / scaleX, (posY / 10) / scaleY, (posZ / 10) / scaleZ)
    glutSolidCylinder(1, 1, quality, 1)
    glPopMatrix()


def line(x0=0, y0=0, z0=0, x1=0, y1=1, z1=0, color=white, width=1):
    glLineWidth(width)
    glBegin(GL_LINES)
    glColor(color)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y1, z1)
    glEnd()


def drawLights():
    global LIGHT_SCALE
    for i in range(len(lightsPos)):
        simpleSphere(lightsPos[i].x, lightsPos[i].y, lightsPos[i].z, LIGHT_SCALE, LIGHT_SCALE, LIGHT_SCALE, lightsColor[i], 8)


def addLight(pos=P(0, 0, 0, 1), ambient=L(1, 1, 1, 1), diffuse=L(1, 1, 1, 1), specular=L(1, 1, 1, 1), on=True):
    lightsPos.append(pos)
    lightsColor.append(Color(diffuse.r, diffuse.g, diffuse.b))
    Light.createLight(pos, ambient, diffuse, specular, on)


def drawAxys():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor(green)
    glVertex3f(2000.0, 0.0, 0.0)
    glVertex3f(-2000.0, 0.0, 0.0)
    glColor(red)
    glVertex3f(0.0, 0.0, 2000.0)
    glVertex3f(0.0, 0.0, -2000.0)
    glColor(blue)
    glVertex3f(0.0, -2000.0, 0.0)
    glVertex3f(0.0, 2000.0, 0.0)
    glEnd()


