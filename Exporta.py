# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 10:03:40 2017

@author: Guto
"""

import matplotlib.pyplot as plt
import subprocess
from matplotlib.pyplot import *
from numpy import *
from PIL import Image


def func(input, num):
    forma = input
    menorX = forma[0][0]
    maiorX = forma[0][0]
    menorY = forma[0][1]
    maiorY = forma[0][1]

    for x in range(0, len(forma)):  # verifica quais são os maiores e menores X e Y
        if menorX > forma[x][0]:
            menorX = forma[x][0]
        if maiorX < forma[x][0]:
            maiorX = forma[x][0]
        if menorY > forma[x][1]:
            menorY = forma[x][1]
        if maiorY < forma[x][1]:
            maiorY = forma[x][1]

    alturaIMG = maiorY - menorY  # calculando altura e largura da imagem a ser gerada
    larguraIMG = maiorX - menorX

    imagem = []
    linha = []

    for x in range(0, alturaIMG + 2):  # Montando as linhas (altura e largura são invertidos aqui)
        linha.append(255)
    for x in range(0, larguraIMG + 2):  # juntando todas as linhas em uma única matriz
        imagem.append(linha)

    arr = array(imagem)  # Converte a lista em vetor

    for x in range(0, len(forma)):  # colocando ponto preto nos píxel listados no vetor "forma"
        X = forma[x][0] - menorX
        Y = forma[x][1] - menorY
        arr[X][Y] = 0
        if X < alturaIMG:  # esses IFs só engrossam os pontos
            arr[X + 1][Y] = 0
        if X > 0:
            arr[X - 1][Y] = 0
        if Y < larguraIMG:
            arr[X][Y + 1] = 0
        if Y > 0:
            arr[X][Y - 1] = 0
        if X > 0 and Y > 0:
            arr[X - 1][Y - 1] = 0
        if X < alturaIMG and Y > 0:
            arr[X + 1][Y - 1] = 0
        if X > 0 and Y < larguraIMG:
            arr[X - 1][Y + 1] = 0
        if X < alturaIMG and Y < larguraIMG:
            arr[X + 1][Y + 1] = 0

    img = Image.fromarray(arr)  # convertendo array em imagem

    plt.axes(frameon=False).get_xaxis().set_visible(False)  # tira o eixo X
    plt.axes(frameon=False).get_yaxis().set_visible(False)  # tira o eixo Y

    plt.imshow(img)  # plotando a imagem
    savefig('../tf/' + str(num) + '.jpg')  # exporta a imagem sem bordas
    import os
    ret = os.popen('python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=../tf/'
                   + str(num) +
                   '.jpg').read()
    return ret
