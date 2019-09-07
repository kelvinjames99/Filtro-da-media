import numpy as np
import cv2
import math


def media_ingenua(caminho, LAR_JANELA, ALT_JANELA):
    img = cv2.imread(caminho)
    for i in range(math.floor(ALT_JANELA/2), img.shape[0] - ALT_JANELA):       #altura
        for j in range(math.floor(LAR_JANELA/2), img.shape[1] - LAR_JANELA):       #largura
            for z in range(img.shape[2]):               #canal
                soma = 0
                for x in range(i - math.floor(ALT_JANELA/2), i + math.ceil(ALT_JANELA/2)):#implem janela
                    for y in range(j - math.floor(LAR_JANELA/2), j + math.ceil(ALT_JANELA/2)):
                        soma+=img[x, y, z]
                img[i, j, z] = soma/(LAR_JANELA*ALT_JANELA)
    cv2.imshow('Output ingenuo', img)

def media_separavel(caminho, LAR_JANELA, ALT_JANELA):
    img = cv2.imread(caminho)
    horizontal = cv2.imread(caminho)
    #horizontal
    for i in range(horizontal.shape[0]):       
        for j in range(math.floor(LAR_JANELA/2), horizontal.shape[1] - math.ceil(LAR_JANELA/2)):       
            for z in range(horizontal.shape[2]):              
                soma = 0
                for x in range(j - math.floor(LAR_JANELA/2), j + math.ceil(LAR_JANELA/2)):
                    soma += img[i, x, z]
                horizontal[i, j, z] = soma/LAR_JANELA
    #horizontal

    #vertical
    vertical = cv2.imread(caminho)
    for i in range(math.floor(ALT_JANELA/2), vertical.shape[0] - math.ceil(ALT_JANELA/2)):
        for j in range(vertical.shape[1]):
            for z in range(vertical.shape[2]):
                soma = 0
                for x in range(i - math.floor(ALT_JANELA/2), i + math.ceil(ALT_JANELA/2)):
                    soma += horizontal[x, j, z]
                vertical[i, j, z] = soma/ALT_JANELA
    #vertical

    cv2.imshow('Output separavel', vertical)



#função "main" aqui
caminho = "./Frog.jpg"
img_original = cv2.imread(caminho)
#media_ingenua(caminho, 15, 15)
media_separavel(caminho, 7, 7)
cv2.imshow('Input', img_original)
cv2.waitKey(0)
cv2.destroyAllWindows()