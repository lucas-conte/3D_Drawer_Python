from OpenGL.GL import *
from OpenGL.GLU import *
import math

# defines arrow keys
UP = 101
DOWN = 103
LEFT = 100
RIGHT = 102
CTRL = 114
SHIFT = 112


class Camera(object):
    def __init__(self):
        self.yaw = -135
        self.pitch = 0
        self.speed = 3

        self.eyeX = 100
        self.eyeY = 25
        self.eyeZ = 100

        self.lookX = 0
        self.lookY = 0
        self.lookZ = 0

        self.fov = 60
        self.fAspect = 16/9

    def getEye(self):
        return {'eyeX': self.eyeX, 'eyeY': self.eyeY, 'eyeZ': self.eyeZ}

    def getLook(self):
        return {'lookX': self.lookX, 'lookY': self.lookY, 'lookZ': self.lookZ}

    def lookAt(self):
        glLoadIdentity()
        gluLookAt(self.eyeX, self.eyeY, self.eyeZ, self.lookX, self.lookY, self.lookZ, 0, 1, 0)

    def look(self):
        self.lookX = self.eyeX
        self.lookY = self.eyeY
        self.lookZ = self.eyeZ
        tempPitch = self.pitch * math.pi / 180
        tempYaw = self.yaw * math.pi / 180

        self.lookY += math.sin(tempPitch)
        self.lookX += math.sin(tempYaw)
        self.lookZ += math.cos(tempYaw)
        self.lookAt()

    def handleLook(self, key):
        tempYaw = self.yaw * math.pi / 180
        strafeYaw = (self.yaw + 90) * math.pi / 180
        if key == b'w':
            self.eyeX += self.speed * math.sin(tempYaw)
            self.eyeZ += self.speed * math.cos(tempYaw)
        if key == b's':
            self.eyeX -= self.speed * math.sin(tempYaw)
            self.eyeZ -= self.speed * math.cos(tempYaw)
        if key == b'a':
            self.eyeX += self.speed * math.sin(strafeYaw)
            self.eyeZ += self.speed * math.cos(strafeYaw)
        if key == b'd':
            self.eyeX -= self.speed * math.sin(strafeYaw)
            self.eyeZ -= self.speed * math.cos(strafeYaw)

        self.look()

    def handleEye(self, key):
        if key == UP:
            self.pitch += 3
            if self.pitch >= 90:
                self.pitch = 90
        if key == DOWN:
            self.pitch -= 3
            if self.pitch <= -90:
                self.pitch = -90
        if key == LEFT:
            self.yaw += 3
        if key == RIGHT:
            self.yaw -= 3
        if key == CTRL:
            self.eyeY -= self.speed
        if key == SHIFT:
            self.eyeY += self.speed

        self.look()

    def returnDist(self, dist=30):
        lookX = self.eyeX
        lookY = self.eyeY
        lookZ = self.eyeZ
        tempPitch = self.pitch * math.pi / 180
        tempYaw = self.yaw * math.pi / 180

        lookY += math.sin(tempPitch)*dist
        lookX += math.sin(tempYaw)*dist
        lookZ += math.cos(tempYaw)*dist
        return lookX, lookY, lookZ
