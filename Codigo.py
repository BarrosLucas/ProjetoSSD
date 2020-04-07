"""
UNIVERSIDADE FEDERAL DA PARAÍBA
Engenheria de Computação
Sinais e Sistemas Dinâmicos

ALUNOS:
    Daniel de Sá Pires
    Júlio Leite Tavares Neto
    Lucas Freitas de Barros
"""


import cv2
import numpy
import glob
import random
import math

#Inicializo todas as listas criadas
def inicializando():
    for i in range(40):
        imagensOrlFaces.append([])
        imagensSorteadas.append([])
        imagensDeTeste.append([])
        urlsImgsEscolhidas.append([])
        urlsImgsDeTeste.append([])
        url = "orl_faces\orl_faces\s"+str(i+1)+"\*"
        imagensOrlFaces[i] = glob.iglob(url)

#Calcula o módulo
def modulo(linhas,colunas,matriz):
    modulo = 0
    for i in range(linhas):
        for j in range(colunas):
            modulo += (int(matriz[i][j]))**2
            if(modulo < 0):
                modulo *= -1
    return math.sqrt(modulo)

#Calcula a distância euclidiana entre duas matrizes
def distancia_euclidiana(matriz1, matriz2):
    retorno = 0
    for i in range(len(matriz1)):
        for j in range(len(matriz1[0])):
            retorno += (int(matriz2[i][j])- int(matriz1[i][j]))**2
            if (retorno < 0):
                retorno *= -1
    return math.sqrt(retorno)

#Realiza os 5 testes
def realiza_teste(indiceDoTeste,parteReal,parteImaginaria,indiceI):
    #Inicializa variáveis que serão úteis no decorrer dos testes
    menorDistancia = None
    menorDistanciaAux = None
    distancia = None

    #Caso seja solicitada a execução do 5º teste, uma sequência
    #de passos deve ser seguida antes da execução do teste
    #propriamente dito. Isso consiste em determinar os módulos
    #real e imaginário da imagem sorteada corrente. Para isso
    #é feito o módulo das partes reais da imagem corrente, e
    #o módulo das partes imaginárias da imagem corrente. Lembrando
    #que o módulo se dá pela raiz quadrada da soma dos quadrados
    if(indiceDoTeste == 5):
        moduloTesteReal = 0
        moduloTesteImaginario = 0

        moduloArea = 0
        moduloTeste = 0

        #Cálcula o módulo da parte real da imagem escolhida
        moduloReal = modulo(len(parteReal),len(parteReal[0]),parteReal)
        
        #Calcula o módulo da parte imaginária da imagem escolhida
        moduloImaginario = modulo(len(parteImaginaria),len(parteImaginaria[0]),parteImaginaria)

    #Percorre todas as imagens de teste
    for a in range(QNT):
        for j in range(9):
            #Pega a imagem de teste atual
            magnitudeTeste = imagensDeTeste[a][j]

            #Extrai a posição do quadrado na imagem
            linhas,colunas = magnitudeTeste.shape
            cLinha,cColuna = linhas//2,colunas//2

            #Pega a área da image
            areaTeste = magnitudeTeste[cLinha-QUAD:cLinha+QUAD, cColuna-QUAD:cColuna+QUAD]

            #Caso seja feito o Teste 1, a distância calculada será entre a parte real
            #da imagem aleatória corrente e a parte real da imagem atual
            if(indiceDoTeste == 1):
                parteRealAreaTeste = numpy.real(areaTeste)
                distancia = distancia_euclidiana(parteReal,parteRealAreaTeste)

            #Caso seja feito o Teste 2, a distância calculada será entre a parte imaginária
            #da imagem aleatória corrente e a parte imaginária da imagem atual
            elif(indiceDoTeste == 2):
                parteImaginariaTeste = numpy.imag(areaTeste)
                distancia = distancia_euclidiana(parteImaginaria,parteImaginariaTeste)

            #Caso seja feito o Teste 3, a distância calculada será a soma da distância entre
            #as partes reais e imaginárias entre as imagens aleatória e correntes
            elif(indiceDoTeste == 3):
                parteRealAreaTeste = numpy.real(areaTeste)
                parteImaginariaTeste = numpy.imag(areaTeste)

                distancia = distancia_euclidiana(parteReal,parteRealAreaTeste)
                distancia += distancia_euclidiana(parteImaginaria,parteImaginariaTeste)

            #Caso seja feito o Teste 4, a distância será a menor distância entre uma das
            #opções:
            #1 - distância entre as partes reais das imagens aleatórias correntes e da
            #imagem atual
            #2 - distância entre a parte real da imagem aleatória atual e a parte imaginária
            #da imagem de teste atual
            #3 - distância entre a parte imaginária da imagem aleatória atual e a parte
            #real da imagem de teste atual
            #4 - distância entre a parte imaginária da imagem aleatória atual e a parte
            #imaginária da imagem de teste atual
            elif(indiceDoTeste == 4):
                parteRealAreaTeste = numpy.real(areaTeste)
                parteImaginariaTeste = numpy.imag(areaTeste)
                distancia = distancia_euclidiana(parteReal,parteRealAreaTeste)
                if(menorDistanciaAux == None):
                    menorDistanciaAux = distancia
                if(distancia < menorDistanciaAux):
                    menorDistanciaAux = distancia
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

            #Caso seja feito o Teste 5, a distância será dada pela raiz quadrada do
            #quadrado dadiferença da soma dos módulos de cada imagem envolvida.
            elif(indiceDoTeste == 5):
                parteRealAreaTeste = numpy.real(areaTeste)
                parteImaginariaTeste = numpy.imag(areaTeste)

                moduloTesteReal = modulo(len(parteRealAreaTeste),len(parteRealAreaTeste[0]),parteRealAreaTeste)
                moduloTesteImaginario = modulo(len(parteImaginariaTeste),len(parteImaginariaTeste[0]),parteImaginariaTeste)

                distancia = math.sqrt(((moduloTesteReal + moduloTesteImaginario)-(moduloReal + moduloImaginario))**2)
                

            #Compara a distância obtida com o teste atual com a menor distância
            #já calculada e atualiza os valores dos índices.
            if(menorDistancia == None):
                menorDistancia = distancia
                indiceI, indiceA, indiceJ = indiceI,a,j
            if(distancia < menorDistancia):
                menorDistancia = distancia
                indiceI, indiceA, indiceJ = indiceI,a,j
    return menorDistancia,indiceI,indiceA,indiceJ


#Constantes
QNT = 40
QUAD = 4

#Aqui conterá todas as URLS já no formato glob para que possam ser acessadas
#(note que as URLS são string que foram convertidas para um objeto do qual é
#possível pegar todos os arquivos de um diretório)
imagensOrlFaces    = [] 

#Guarda as imagens aleatórias sorteadas convertidas 
imagensSorteadas   = []

#As demais imagens convertidas para que possam ser comparadas com a sorteada
imagensDeTeste     = []

#Guarda as URLS das imagens aleatórias sorteadas e convertidas
urlsImgsEscolhidas = []

#Guarda a URL das demais imagens convertidas que serão comparadas
urlsImgsDeTeste    = []


#Guarda a quantidade de erros e acertos que terão em cada um dos 5 testes
erros   = [0]*5
acertos = [0]*5


print("Passo 1 - Pegando as URLs")
#Pega todas as URLS e inicializ as listas
inicializando()

print("Passo 2 - Sorteando e convertendo imagens")
#Sorteia uma imagem, pega todas as imagens e transforma, compara se ela é a aleatória
for i in range(QNT):
    #Pega o caminho de uma imagem aleatória de cada uma das 40 pastas
    imagemAleatoria = "orl_faces\orl_faces\s"+str(i+1)+"\\"+str(random.randint(1,10))+".pgm"

    #Percorre todas as imagens da pasta atual
    for a in imagensOrlFaces[i]:
        #Carrega a imagem
        imagem = cv2.imread(a,cv2.IMREAD_GRAYSCALE)

        #Faz a transformada nelas
        imagemTransformada = numpy.fft.fft2(imagem)
        fftshift = numpy.fft.fftshift(imagemTransformada)

        #Se o caminho da imagem atual for o mesmo que foi sorteado em "imagemAleatoria"
        #guarda a imagem convertida e sua URL nas listas "urlsImgsEscolhidas" e
        #imagensSorteadas, respectivamente. Caso contrário, guarda sua url e a imagem
        #convertida em "urlsImgsDeTeste" e "imagensDeTeste" respectivamente, prontas
        #para serem testadas.
        if (a == imagemAleatoria):
            urlsImgsEscolhidas[i] = imagemAleatoria
            imagensSorteadas[i] = fftshift
        else:
            urlsImgsDeTeste[i].append(a)
            imagensDeTeste[i].append(fftshift)


print("Passo 3 - Testando e comparando")
#Iniciam os testes
for i in range(QNT):
    #Pega a imagem sorteada da pasta atual
    magnitudeEscolhida = imagensSorteadas[i]

    #Recupera a posição do quadrado
    linhas, colunas = magnitudeEscolhida.shape
    cLinha, cColuna = linhas//2, colunas//2

    #Calcula a área e pega a parte real e imaginária da mesma
    area = magnitudeEscolhida[cLinha-QUAD:cLinha+QUAD, cColuna-QUAD:cColuna+QUAD]
    parteReal = numpy.real(area)
    parteImaginaria = numpy.imag(area)

    #Inicia o loop para a execução de cada um dos 5 testes com a imagem corrente
    for testes in range(5):
        menorDistancia,indiceI,indiceA,indiceJ = realiza_teste(testes+1,parteReal,parteImaginaria,i)
        #Compara com os índices das imagens e calcula os acertos e erros que
        #existiram na comparação.
        if(indiceI == indiceA):
            acertos[testes] += 1
        else:
            erros[testes] += 1

print("\n\nRESULTADO\n")
for i in range(len(acertos)):
    print("#-- TESTE %d --#" %(i+1))
    print("Acertos: %d" %(acertos[i]))
    print("Erros: %d\n" %(erros[i]))
