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

#LEER EL ARCHIVO
condiciones = leerArhivo()

#PRIMERA LINEA DEL ARCIHVO. ESTA LA ESPECIFICACION DE LA TABLA
definicion = condiciones[0]

metodo = int(definicion[0])
optimizacion = definicion[1]
variables = int(definicion[2])
restricciones = int(definicion[3])

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
    '''
    for row in matriz:
      print(' '.join(map(str,row)))
    '''
    return matriz


#COEFICIENTES DE LA FUNCION IDENTIDAD
coeficientes = condiciones[1]




matriz = crearMatriz(variables, restricciones)

Metodo(metodo)













#Para correrlo desde terminal: python simplex.py [-h] archivo.txt
