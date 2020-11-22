import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.exposure import match_histograms


def getHistograma(imagem,linha=0,coluna=0,titulo='Imagem Original'):
    color = ('b','g','r')#Ordem de leitura da biblioteca OpenCV
    for channel,col in enumerate(color):
        histr = cv2.calcHist([imagem],[channel],None,[256],[0,256])
        axs[linha+1,coluna].plot(histr,color = col)
        axs[linha+1,coluna].axis(xmin=0,xmax=256)
    axs[linha+1,coluna].set_xlabel('Intensidade da cor')
    axs[linha+1,coluna].set_ylabel('Quantidades de pixels')
    axs[linha,coluna].set_title(titulo)
    axs[linha,coluna].set_axis_off()#tira o eixo x e y das imagens que ficam na linha 1
    axs[linha,coluna].imshow(imagem)#mostra as imagens resultantes de cada histograma
    

def getEqualizacao(dirImagem): #Função de Equalização
    img = cv2.imread(dirImagem)#lê a imagem
    getHistograma(img)#cria histograma da imagem Original

    img_to_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV) #converte a imagem para o espaço de cor YUV pq n tem como equalizar logo no espaço BGR
    img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])#Equaliza a imagem
    hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)#Converte a imagem de volta para o espaço BGR(mesmo RGB)
    
    getHistograma(hist_equalization_result,0,1,'Equalização de histograma')#cria histograma da imagem Equalizada

def getEspecificacao(dirImagemOriginal,dirImagemReferencia): #Função de Especificação
    img = cv2.imread(dirImagemOriginal)#lê a imagem Original
    img2 = cv2.imread(dirImagemReferencia)#lê a imagem Referencia
    getHistograma(img2,0,2,"Imagem de Referência")#cria histograma da imagem de referência
    matched = match_histograms(img, img2, multichannel=True)
    getHistograma(matched,0,3,"Especificação de histograma")#cria histograma de Especificação


    
######main########
print("Aperte Ctrl+c para sair")
while(1):
    try:
        k = input("Diretório da imagem original: ")
        k1 = input("Diretório da imagem de referência: ")
        fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(13, 6))#matriz de gráficos que serão exibidos
        plt.subplots_adjust(0.08,None,0.96,None,1.0)#ajuste de espaçamento entre os subplots
        getEqualizacao(k)
        getEspecificacao(k,k1)
        print()
        plt.show()#mostra todos histogramas e imagens 
    except KeyboardInterrupt:
        print('Programa finalizado...')
        break
    except:
        print("Diretório Inválido!\n")
#################
