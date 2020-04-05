import cv2
import numpy
import glob
import random
import math

def distancia_euclidiana(matriz1, matriz2):
    retorno = 0
    for i in range(len(matriz1)):
        for j in range(len(matriz1[0])):
            retorno += (int(matriz2[i][j])- int(matriz1[i][j]))**2
            if (retorno < 0):
                retorno *= -1
    return math.sqrt(retorno)

def realiza_teste(indiceDoTeste,parteReal,parteImaginaria,indiceI):
    menorDistanciaAux = None
    distancia = None

    if(indiceDoTeste == 5):
        moduloReal = 0
        moduloImaginario = 0

        moduloTesteReal = 0
        moduloTesteImaginario = 0

        moduloArea = 0
        moduloTeste = 0

        linhas  = len(parteReal)
        colunas = len(parteReal[0])
        for i in range(linhas):
            for j in range(colunas):
                moduloReal += (int(parteReal[i][j]))**2
                if(moduloReal < 0):
                    moduloReal *= -1
        moduloReal = math.sqrt(moduloReal)
        
        linhas = len(parteImaginaria)
        colunas = len(parteImaginaria[0])
        for i in range(linhas):
            for j in range(colunas):
                moduloImaginario += (int(parteImaginaria[i][j]))**2
                if(moduloImaginario < 0):
                    moduloImaginario *= -1
        moduloImaginario = math.sqrt(moduloImaginario)
        
    for a in range(QNT):
        for j in range(9):
            magnitudeTeste = imagensDeTeste[a][j]

            linhas,colunas = magnitudeTeste.shape
            cLinha,cColuna = linhas//2,colunas//2

            areaTeste = magnitudeTeste[clinha-QUAD:clinha+QUAD, ccoluna-QUAD:ccoluna+QUAD]

            if(indiceDoTeste == 1):
                parteRealAreaTeste = numpy.real(areaTeste)
                distancia = distancia_euclidiana(parteReal,parteRealAreaTeste)
            elif(indiceDoTeste == 2):
                parteImaginariaTeste = numpy.imag(areaTeste)
                distancia = distancia_euclidiana(parteImaginaria,parteImaginariaTeste)
            elif(indiceDoTeste == 3):
                parteRealAreaTeste = numpy.real(areaTeste)
                parteImaginariaTeste = numpy.imag(areaTeste)

                distancia = distancia_euclidiana(parteReal,parteRealAreaTeste)
                distancia += distancia_eulidiana(parteImaginaria,parteImaginariaTeste)
            elif(indiceDoTeste == 4):
                parteRealAreaTeste = numpy.real(areaTeste)
                parteImaginariaTeste = numpy.imag(areaTeste)
                distancia = distancia_euclidiana(parteReal,parteRealAreaTeste)
                if(menorDistanciaAux == None):
                    menorDistanciaAux = distancia
                if(distancia < menorDistanciaAux):
                    menorDistanciaAux = valor
                distancia = distancia_euclidiana(parteReal,parteImaginariaTeste)
                if(distancia < menorDistanciaAux):
                    menorDistanciaAux = distancia
                distancia = distancia_euclidiana(parteImaginaria,parteRealAreaTeste)
                if(distancia < menorDistanciaAux):
                    menorDistanciaAux = distancia
                distancia = distancia_euclidiana(parteImaginaria,parteImaginariaTeste)
                if(distancia < menorDistanciaAux):
                    menorDistanciaAux = distancia
                distancia = menorDistanciaAux
            elif(indiceDoTeste == 5):
                parteRealAreaTeste = numpy.real(areaTeste)
                parteImaginariaTeste = numpy.imag(areaTeste)

                linhas = len(parteReal)
                colunas = len(parteReal[0])
                for linha in range(linhas):
                    for coluna in range(colunas):
                        moduloTesteReal += (int(parteRealTeste[linha][coluna]))**2
                        if(moduloTesteReal < 0):
                            moduloTesteReal *= -1
                moduloTesteReal = math.sqrt(moduloTesteReal)

                linhas = len(parteImaginaria)
                colunas = len(parteImaginaria[0])
                for linha in range(linhas):
                    for coluna in range(colunas):
                        moduloTesteImaginario += (int(parteImaginariaTeste[linha][coluna]))**2
                        if(moduloTesteImaginario < 0):
                            moduloTesteImaginario *= -1
                moduloTesteImaginario = math.sqrt(moduloTesteImaginario)

                distancia = math.sqrt(((moduloTesteReal + moduloTesteImaginario)-(moduloReal + moduloImaginario))**2)
                

    if(menorDistancia == None):
        menorDistancia = distancia
    if(distancia <= menorDistancia):
        menorDistancia = distancia
        indiceI, indiceA, indiceJ = i,a,j
    return menorDistancia,indiceI,indiceA,indiceJ



QNT = 40
QUAD = 4

imagensOrlFaces    = []*QNT
imagensSorteadas   = []*QNT
imagensDeTeste     = []*QNT
urlsImgsEscolhidas = []*QNT
urlsImgsDeTeste    = []*QNT

erros   = [0]*5
acertos = [0]*5

print("Passo 1 - Pegando as URLs")
#Pega todas as URLS
for i in range(1,QNT+1):
    imagensOrlFaces[i] = glob.iglob("orl_faces\orl_faces\s" +i+ "\*")

print("Passo 2 - Sorteando e convertendo imagens")
#Sorteia uma imagem, pega todas as imagens e transforma, compara se ela é a aleatória
for i in range(QNT):
    print("Passo 2.1 - Sorteando uma imagem")
    imagemAleatoria = "orl_faces\orl_faces\s"+(i+1)+"\\"+random.randint(1,10)+".pgm"
    for a in imagensOrlFaces:
        print("Passo 2.2 - Transformando as demais imagens")
        imagem = cv2.imread(a,cv2.IMREAD_GRAYSCALE) #carrega a imagem
        imagemTransformada = numpy.fft.fft2(imagem)
        fftshift = numpy.fft.fftshift(imagemTransformada)

        print("Passo 2.3 - Se for a imagem sorteada, coloca nas URL de imagens escolhidas")
        if (a == imagemAleatoria):
            urlsImgsEscolhidas[i] = imagemAleatoria
            imagensSorteadas[i] = fftshift
        else:
            print("Passo 2.4 - Se não for a imagem sorteada, só guarda em URL e imagens de teste")
            urlsImgsDeTeste[i].append(a)
            imagensDeTeste[i].append(fftshift)



for i in range(QNT):
    menorDistancia = None
    
    magnitudeEscolhida = imagensSorteadas[i]

    linhas, colunas = magnitudeEscolhida.shape
    cLinha,cColunas = linhas//2, colunas//2

    area = magnitudeEscolhida[cLinha-QUAD:cLinha+QUAD, cColuna-QUAD:cColuna+QUAD]
    parteReal = numpy.real(area)
    parteImaginaria = numpy.imag(area)

    for testes in range(5):
        menorDistancia,indiceI,indiceA,indiceJ = realizaTeste(testes+1,parteReal,parteImaginaria,i,area)
        if(indiceI == indiceA):
            acertos[testes] += 1
        else:
            erros[testes] += 1

print("RESULTADO")
for i in range(len(acertos)):
    print("Acertos %d: %d" %((i+1),acertos[i]))
    print("Erros %d: %d" %((i+1),erros[i]))
