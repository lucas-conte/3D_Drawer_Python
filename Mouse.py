from OpenGL.GL import *
from OpenGL.GLU import *

from collections import namedtuple

XY = namedtuple('XY', ['x', 'y'])


class Mouse(object):
    def __init__(self):
        self.width = 16
        self.height = 9
        self.xy = []
        self.z = []
        self.z.append(0)

    def readMouse(self, x, y):
        y = self.height - y  # inverte y - o y para desenhar é inverso ao y da janela

        # garante que não vai ser desenhado fora da janela
        if x >= self.width - 1:
            x = self.width - 1
        if x <= 1:
            x = 1

        if y >= self.height - 1:
            y = self.height - 1
        if y <= 1:
            y = 1

        self.xy.append(XY(x, y))  # salva posição atual

    def reset(self):
        self.xy.clear()
        self.z.clear()
        self.z.append(0)  # serve para não crashar ao dar undo num desenho de uma curva

    def save(self):
        self.xy.append(XY(0, 0))  # adiciona um 'break' de curvas
        self.z.append(len(self.xy))  # salva o indice do xy para fazer undo

    def setWindowSize(self, h, w):
        self.height = h
        self.width = w

    def draw(self, r=1, g=1, b=1, w=1.5, line=True):
        # configura o openGL para desenhar em 2D
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_DEPTH_BUFFER_BIT)

        # desenhando o 'caminho' do mouse
        glColor3f(r, g, b)

        if line:
            glLineWidth(w)
            glBegin(GL_LINES)
        else:
            glPointSize(w)
            glBegin(GL_POINTS)

        for i in range(1, len(self.xy)):
            if self.xy[i].x and self.xy[i - 1].x:  # se não for um 'break' de curvas
                if line:  # para desenhar uma linha precisa de 2 pontos:
                    glVertex2d(self.xy[i - 1].x, self.xy[i - 1].y)  # o 'anterior'
                glVertex2d(self.xy[i].x, self.xy[i].y)              # e o 'atual'

        glEnd()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_LIGHTING)

    def undo(self):
        if not self.z:  # não é possivel fazer pop_back com vetor z vazio
            return
        self.z.pop()
        if not self.z:  # não é possivel fazer undo com o vetor z vazio
            return

        while len(self.xy) > self.z[-1]:  # equivalente a xy.resize(z.back())
            self.xy.pop()
