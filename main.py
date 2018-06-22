import Camera, Mouse, Util, Light, Exporta
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import time

num = 100

# keyboard defines
ESC_KEY = b'\x1b'

# control defines
CLICK_MIN_TIME = 0.1  # 1 décimo de segundo

camera = Camera.Camera()
mouse = Mouse.Mouse()

mouseLock = False  # controla a trava do mouse ao clicar rapidamente para desenhar
saveMouse = False  # controla se a posição do mouse vai ser salva

start = 0  # controla o tempo do click do mouse

# window size
width = 800
height = 600

# texture
img = pygame.image.load('texture/tex.jpg')
texData = pygame.image.tostring(img, "RGBA", 1)
texWidth = img.get_width()
texHeight = img.get_height()
texId = 0

# objects
objects = list()
SIZE = (
    10,  # Util.BOX     = 0
    1,   # Util.SPHERE  = 1
    10   # Util.PYRAMID = 2
)


def handleViewParameters():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(camera.fov, camera.fAspect, 0.1, 2500)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT)
    camera.look()


def texture():
    global texId
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    texId = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texId)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texWidth, texHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, texData)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    handleViewParameters()
    Util.drawAxys()
    for obj in objects:
        Util.drawObj(obj)
    # Util.drawLights()
    mouse.draw()
    glutSwapBuffers()


def init():
    global height, width
    handleViewParameters()
    glClearColor(0.2, 0.2, 0.2, 1.0)
    mouse.setWindowSize(height, width)
    Light.setupLighting()
    texture()


def handleWindowSize(w, h):
    global height, width
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    camera.fAspect = w / h
    mouse.setWindowSize(h, w)
    height = h
    width = w
    handleViewParameters()


def handleMouseButtons(button, state, x, y):
    global mouseLock, saveMouse, start
    # variavel de diferença de tempo entre o click
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # print("  Mouse1 v")
            if mouseLock:          # se o mouse estiver travado e foi apertado um segundo click
                # print("    mouseLock = true => para de salvar o mouse")
                saveMouse = False  # para de salvar a posição do mouse
                mouse.save()       # salva a posição do mouse para fazer undo
            else:
                # print("    mouseLock = false => salva o tempo")
                start = time.time()  # grava o tempo do click para baixo do mouse1
                saveMouse = True        # começa a salvar as posições do mouse

        if state == GLUT_UP:
            # print("  Mouse1 ^")
            if mouseLock:          # se o mouse estiver travado e foi solto o segundo click
                # print("    mouseLock = true => destrava o mouse")
                mouseLock = False  # destrava o mouse
            else:
                # print("    mouseLock = false => checa se deu tempo")
                end = time.time()  # grava o tempo que o mouse1 foi solto
                delta = end - start  # calcula a diferença de tempo
                # print("      delta: " + str(delta))
                if delta > CLICK_MIN_TIME:  # se o click levou mais de CLICK_MIN_TIME segundo(s)
                    # print("      delta > tempo => nao é um click, então para de salvar")
                    saveMouse = False       # para de gravar as posições do mouse
                    mouse.save()            # salva a posição do mouse para fazer undo
                else:                 # se o click levou menos de 1 segundo
                    # print("      delta < tempo => é um click começa a salvar o mouse")
                    mouseLock = True  # trava o mouse

    glutPostRedisplay()
    handleViewParameters()


def handleMouseMotion(x, y):  # essa função só é chamada quando está sendo pressionado algum botão do mouse
    if saveMouse:
        mouse.readMouse(x, y)
    glutPostRedisplay()


def handleMouseMotionP(x, y):  # essa função é chamada quando mesmo sem estar sendo pressionado algum botão do mouse
    if saveMouse:
        mouse.readMouse(x, y)
    glutPostRedisplay()


def readResults(str):
    if str == 'quadrado\n':
        return Util.BOX
    if str == 'triangulo\n':
        return Util.PYRAMID
    if str == 'circulo\n':
        return Util.SPHERE


def handleKeyboard(key, x, y):
    global num
    if key == ESC_KEY:
        exit()
    if key == b' ':
        tipo = readResults(Exporta.func(mouse.xy, num))
        num += 1
        mouse.reset()  # limpa o desenho do mouse
        xyz = camera.returnDist(100)
        objects.append(Util.OBJ(tipo, xyz[0], xyz[1], xyz[2], SIZE[tipo], SIZE[tipo], SIZE[tipo], texId))
    if key == b'z':
        mouse.undo()  # desfaz a ultima curva desenhada
    if key == b'w' or key == b'a' or key == b's' or key == b'd':  # se w|a|s|d manda movimento para a camera
        camera.handleLook(key)
    if b'1' <= key <= b'8':  # numeros de 1 a 8
        Light.toggleLight(int(key)-1)

    glutPostRedisplay()


def handleSKeyboard(key, x, y):
    camera.handleEye(key)  # se setinhas manda o movimento para a camera
    glutPostRedisplay()


def mTick(value):
    glutPostRedisplay()
    glutTimerFunc(33, mTick, 1)


def main():
    os.chdir('tensorflow-for-poets-2')
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowPosition(300, 0)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"PROJETO CG - DANILO TUZITA | LUCAS CONTE | MARCOS AUGUSTO")
    glutReshapeFunc(handleWindowSize)

    glutDisplayFunc(draw)

    glutMouseFunc(handleMouseButtons)
    glutMotionFunc(handleMouseMotion)
    glutPassiveMotionFunc(handleMouseMotionP)

    glutKeyboardFunc(handleKeyboard)
    glutSpecialFunc(handleSKeyboard)
    glutTimerFunc(33, mTick, 1)
    init()
    glutMainLoop()


main()
