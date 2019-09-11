import numpy as np
import cv2
import math
from random import randint

#img.shape[0] altura
#img.shape[1] largura
#img.shape[2] canal
def printa_matriz_imagem(img):
    print("COMEÇANDO MATRIZ")
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
                print(img[i, j, 0], "|" , end = "")
        print("\n")
    print("TERMINANDO MATRIZ")

def media_ingenua(caminho, LAR_JANELA, ALT_JANELA):
    img = cv2.imread(caminho)                                           #começando de uma posição válida em relação ao tamanho da janela
    for i in range(math.floor(ALT_JANELA/2), img.shape[0] - ALT_JANELA):       
        for j in range(math.floor(LAR_JANELA/2), img.shape[1] - LAR_JANELA):       
            for z in range(img.shape[2]):              
                soma = 0
                for x in range(i - math.floor(ALT_JANELA/2), i + math.ceil(ALT_JANELA/2)):#implemt. janela
                    for y in range(j - math.floor(LAR_JANELA/2), j + math.ceil(ALT_JANELA/2)):
                        soma+=img[x, y, z]
                img[i, j, z] = soma/(LAR_JANELA*ALT_JANELA)
    cv2.imshow('Output ingenuo', img)
    cv2.imwrite('ingenuo.jpg', img)

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
    cv2.imwrite('separavel.jpg', vertical)

def imagem_integral(img_integral):
    for i in range(img_integral.shape[0]):
        for j in range(img_integral.shape[1]):
            for z in range(img_integral.shape[2]):
                aux1 = img_integral[i-1, j, z]
                aux2 = img_integral[i, j-1, z]
                aux3 = img_integral[i-1, j-1, z]
                if i-1 < 0 or j-1 < 0:
                    aux3 = 0
                    if i-1 < 0:
                        aux1 = 0
                    if j-1 < 0:
                        aux2 = 0
                #print(aux1, aux2, aux3, img_integral[i, j, z])
                img_integral[i, j, z] = aux1 + aux2 - aux3 + img_integral[i, j, z]

def media_integral(caminho, LAR_JANELA, ALT_JANELA):
    img_integral = cv2.imread(caminho).astype('float32')/255
    imagem_integral(img_integral)
    saida = cv2.imread(caminho).astype('float32')/255
    for i in range(saida.shape[0]):
        for j in range(saida.shape[1]):
            inicial_i = i - math.floor(ALT_JANELA/2)        #iniciando coordenadas da janela 
            inicial_j = j - math.floor(LAR_JANELA/2) 
            final_i = i + math.floor(ALT_JANELA/2)
            final_j = j + math.floor(LAR_JANELA/2)
            #verificando se saiu da imagem e corrigindo caso saia
            if inicial_i < 0:              
                inicial_i = 0
            if inicial_j < 0:
                inicial_j = 0
            if final_i >= saida.shape[0]:        
                final_i = saida.shape[0] - 1
            if final_j >= saida.shape[1]:
                final_j = saida.shape[1] - 1
            for z in range(saida.shape[2]):
                saida[i, j, z] = img_integral[final_i, final_j, z] 
                if  inicial_i - 1  >= 0:
                    saida[i, j, z] -= img_integral[inicial_i - 1, final_j, z]
                if inicial_j - 1 >= 0:
                    saida[i, j, z] -= img_integral[final_i, inicial_j - 1, z]
                if inicial_i - 1 >= 0 and final_i - 1 >= 0:
                    saida[i, j , z] += img_integral[inicial_i - 1,inicial_j - 1, z]               
                saida[i, j, z] = (saida[i, j, z]/((final_j - (inicial_j - 1))*(final_i - (inicial_i - 1))))
    cv2.imshow('Output w/ integral', saida)           
    cv2.imwrite('integral.jpg', saida)
                    


#função "main" aqui
caminho = "./frog.jpg"
img_original = cv2.imread(caminho)
#media_ingenua(caminho, 15, 15)
#media_separavel(caminho, 7, 7)
media_integral(caminho, 15, 15)
cv2.imshow('Input', img_original)
cv2.waitKey(0)
cv2.destroyAllWindows()