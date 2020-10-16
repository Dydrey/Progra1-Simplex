import sys

def leerArhivo():
    archivo = sys.argv[2]
    f = open(archivo)
    data = f.read().strip()
    f.close()
    condiciones = []
    for line in data.split('\n'):
        condiciones.append(line.split(","))
    return(condiciones)

def Metodo(metodo):
    if metodo == 0:
        print("Simplex")
        #llamada a funcion de simplex
    elif metodo == 1:
        print("Gran M")
        #llamada a funcion de Gran M
    elif metodo == 2:
        print("Dos Fases")
        #llamada a funcion de Dos Fases
    else:
        return("Error de metodo")

#CREACION DE LA MATRIZ
def crearMatriz(variables, restricciones):

    columnas = 2+variables+restricciones
    filas = 2+restricciones
    matriz = [[ 0 for i in range(columnas) ] for j in range(filas)]
    for x in range(len(matriz[0])):
        if x == 0:
            matriz[0][x] = "VB"
        elif x == len(matriz[0])-1:
            matriz[0][x] = "LD"
        else:
            matriz[0][x] = "x"+str(x)
    ind = 1
    for y in range(len(matriz)):
        if y == 0:
            matriz[y][0] = "VB"
        elif y == 1:
            matriz[y][0] = "U"
        else:
            matriz[y][0] = "x"+str(variables+1)
            variables+=1
    return matriz
#IMPRIME LA MATRIZ
def imprimirMatriz(matriz):
    for row in matriz:
        print(' '.join(map(str, row)))

def llenarMatriz(matriz, coeficientes, listaRestricciones, variables):
    #LLENA LA FUNCION IDENTIDAD EN LA MATRIZ
    for x in range(len(coeficientes)):
        matriz[1][x+1]=int(coeficientes[x])*(-1)

    #LLENA LAS RESTRICCIONES EN LA MATRIZ
    for i in range(len(listaRestricciones)):
        j = 1
        p = 0
        while j < (len(matriz[0])):
            if p == len(listaRestricciones[i])-2:
                matriz[i+2][len(matriz[0])-1]=listaRestricciones[i][p+1]
                break
            else:
                matriz[i+2][j] = listaRestricciones[i][p]
            j += 1
            p += 1
    i = 2

    for x in range(len(matriz[0])-variables-2):
        matriz[2+x][1+variables+x] = 1




#matriz[fila][columna]
#LEER EL ARCHIVO
condiciones = leerArhivo()

#PRIMERA LINEA DEL ARCIHVO. ESTA LA ESPECIFICACION DE LA TABLA
definicion = condiciones[0]

metodo = int(definicion[0])
optimizacion = definicion[1]
variables = int(definicion[2])
restricciones = int(definicion[3])


#LISTA DE COEFICIENTES DE LA FUNCION IDENTIDAD
coeficientes = condiciones[1]

#LISTA CON LAS RESTRICCIONES
ind = 2
listaRestricciones = []
while ind <= len(condiciones)-1:
    listaRestricciones.append(condiciones[ind])
    ind += 1

matriz = crearMatriz(variables, restricciones)
llenarMatriz(matriz, coeficientes, listaRestricciones, variables)
imprimirMatriz(matriz)

Metodo(metodo)













#Para correrlo desde terminal: python simplex.py [-h] archivo.txt
