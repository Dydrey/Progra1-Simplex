import sys
from fractions import Fraction

# VARIABLE GLOBAL PARA ALMACENAR EL PROCEDIMIENTO DE LAS TABLAS INTERMEDIAS
textoSolucion = ""


# FUNION PARA LEER EL ARHIVO .TXT
def leerArhivo():
    archivo = sys.argv[2]
    f = open(archivo)
    data = f.read().strip()
    f.close()
    condiciones = []
    for line in data.split('\n'):
        condiciones.append(line.split(","))
    return (condiciones)


# LOGICA PARA DEFINIR PROCEDIMIENTO
def Metodo(metodo, matriz):
    # VARIABLES DE CONFIGURACION
    conjuntoSolucion = []
    global textoSolucion
    if metodo == 0:
        print("Simplex")
        textoSolucion += "Solución Método Simplex \n"
        conjuntoSolucion = iteracionSimplex(matriz)

    elif metodo == 1:
        print("Gran M")
        textoSolucion = "Solución Método Gran M \n"
        conjuntoSolucion = iteracionGranM(matriz)
    elif metodo == 2:
        print("Dos Fases")
        textoSolucion = "Solución Método Dos Fases \n"
        # llamada a funcion de Dos Fases
    else:
        return ("Error de metodo")

    return conjuntoSolucion


# CREACION DE LA MATRIZ
def crearMatriz(variables, restricciones):
    columnas = 2 + variables + restricciones
    filas = 2 + restricciones
    matriz = [[0 for i in range(columnas)] for j in range(filas)]
    for x in range(len(matriz[0])):
        if x == 0:
            matriz[0][x] = "VB"
        elif x == len(matriz[0]) - 1:
            matriz[0][x] = "LD"
        else:
            matriz[0][x] = "x" + str(x)
    for y in range(len(matriz)):
        if y == 0:
            matriz[y][0] = "VB"
        elif y == 1:
            matriz[y][0] = "U"
        else:
            matriz[y][0] = "x" + str(variables + 1)
            variables += 1
    return matriz


# IMPRIME LA MATRIZ
def imprimirMatriz(matriz):
    for row in matriz:
        print(' \t'.join(map(str, row)))


# DEVUELVE LA MATRIZ EN STRING PARA GUARDARLA EN ARCHIVO
def matrizToString(matriz):
    stringMatriz = ""
    for row in matriz:
        stringMatriz = stringMatriz + (' \t'.join(map(str, row))) + "\n"
    return stringMatriz


# PEQUEÑA FUNCION PARA MOSTRAR LOS DECIMALES EN FRACCIONES
def fraccion(numeroParaFraccion):
    return str(Fraction(numeroParaFraccion).limit_denominator())


# FUNCION PARA LLENAR LA MATRIZ CON LAS RESTRICCIONES
def llenarMatriz(matriz, coeficientes, listaRestricciones, variables, optimizacion):
    # CONVERSION FUNCION OBJETIVO (FALTA AGREGAR CASO MIN)
    for x in range(len(coeficientes)):
        # if (optimizacion == "max"):
        # CASO MAX
        matriz[1][x + 1] = int(coeficientes[x]) * (-1)
        # else:

    # LLENA LAS RESTRICCIONES EN LA MATRIZ
    for i in range(len(listaRestricciones)):
        j = 1
        p = 0
        while j < (len(matriz[0])):
            if p == len(listaRestricciones[i]) - 2:
                # RESULTADOS DE EQUIVALENCIAS
                matriz[i + 2][len(matriz[0]) - 1] = int(listaRestricciones[i][p + 1])
                break
            else:
                # COEFICIENTES RESTRICCIONES
                matriz[i + 2][j] = int(listaRestricciones[i][p])
            j += 1
            p += 1
    i = 2

    # RELLENA LA MATRIZ IDENTIDAD
    for x in range(len(matriz[0]) - variables - 2):
        matriz[2 + x][1 + variables + x] = 1


# FUNCION PARA BUSCAR LA COLUMNA CON EL NUMERO MENOR EN LA FUNCION OBJETIVO
def buscaColMenor(matriz):
    pos = 0
    menor = 99999
    for x in range( 1, len(matriz[0])):
        elemActual = matriz[1][x]
        if elemActual < menor:
            pos = x
            menor = elemActual
    return pos


# FUNCION PARA BUSCAR LA FILA QUE DIVIDA AL LADO DERECHO CON EL MENOR RESULTADO
def buscarFilMenor(matriz, colMenor):
    i = 2
    filMenor = 99999
    resultado = 0
    while i < len(matriz):
        if (matriz[i][colMenor] != 0) and (matriz[i][len(matriz[i]) - 1] != 0):
            valorLD = (matriz[i][len(matriz[i]) - 1] / matriz[i][colMenor])
            if ((valorLD < filMenor) and (valorLD > 0)):
                filMenor = valorLD
                resultado = i
        i += 1
    return resultado


#def parsearGranM(matriz):



# RUTINA PARA LA SOLUCION MODO SIMPLEX
def iteracionSimplex(matriz):
    global textoSolucion
    seguirIteracion = True
    iteracion = 0
    # BUSCA EL PIVOTE
    colMenor = buscaColMenor(matriz)
    filMenor = buscarFilMenor(matriz, colMenor)

    while (matriz[1][colMenor] < 0):

        # GUARDAMOS LA MATRIZ EN EL STRING PARA EL ARCHIVO
        textoSolucion += "Estado: " + str(iteracion) + "\n"
        textoSolucion += matrizToString(matriz) + "\n"

        # DATOS SOBRE CUAL VARIABLE SALE Y CUAL ENTRA
        # print("La variable que sale es " + matriz[filMenor][0])
        textoSolucion += "La VB que sale es " + matriz[filMenor][0] + "\n"
        # print("La variable entrante es: " + matriz[0][colMenor])
        textoSolucion += "La VB entrante es: " + matriz[0][colMenor] + "\n"

        # GUARDAMOS EL VALOR DEL PIVOTE PARA LAS ITERACIONES
        numeroPivote = float(matriz[filMenor][colMenor])
        textoSolucion += "El número Pivote es: " + str(numeroPivote) + "\n"
        print(textoSolucion)

        '''
        print("Iteracion: " + str(iteracion))
        imprimirMatriz(matriz)
        print("La VB que sale es " + str(matriz[filMenor][0]))
        print("La VB entrante es: " + str(matriz[0][colMenor]))
        print("")
        #################################################################
        '''

        # CAMBIAMOS LA VB
        matriz[filMenor][0] = matriz[0][colMenor]

        # CALCULAMOS LA FILA PIVOTE
        for j in range(1, len(matriz[0])):
            matriz[filMenor][j] = (float(matriz[filMenor][j]) / numeroPivote)

        # APLICAMOS CAMBIOS AL RESTO DE LAS FILAS SEGÚN NUESTRA PIVOTE
        for i in range(1, len(matriz)):
            # EL IF ES PARA EVITAR SOBREESCRIBIR LA FILA PIVOTE
            if (i != filMenor):
                opuesto = (matriz[i][colMenor] * -1)

                for j in range(1, len(matriz[0])):
                    actual = float(matriz[i][j])
                    resultado = actual + (opuesto * matriz[filMenor][j])
                    #print("Fila es: " + str(i) + " Columna es: " + str(j) + " actual es: " + str(actual))
                    #print(str(actual) + " + (" + str(opuesto) + " * " + str(matriz[filMenor][j]) + ") = " + str(resultado))
                    # ACTUALIZAMOS EL VALOR DE LAS FILAS QUE NO SON LA PIVOTE
                    matriz[i][j] = resultado

        #print("La nueva matriz es:")
        imprimirMatriz(matriz)
        iteracion += 1
        # BUSCA EL NUEVO PIVOTE
        colMenor = buscaColMenor(matriz)
        filMenor = buscarFilMenor(matriz, colMenor)
        #print("El nuevo pivote de fila es " + str(matriz[1][colMenor]) + " en la columna " + str(colMenor))
        #print("El nuevo pivote de columa es " + str(matriz[filMenor][1]) + " en la fila " + str(filMenor))
        #print("")

# RUTINA PARA LA SOLUCION MODO GRAM M
def iteracionGranM(matriz):
    print("En trabajo, disculpe las molestias")


def main():
    # LEER EL ARCHIVO
    condiciones = leerArhivo()

    # PRIMERA LINEA DEL ARCIHVO. ESTA LA ESPECIFICACION DE LA TABLA
    definicion = condiciones[0]

    # PRIMERA LINEA DEL ARCHIVO PARSEADA
    metodo = int(definicion[0])
    optimizacion = definicion[1]
    variables = int(definicion[2])
    restricciones = int(definicion[3])

    # SEGUNDA LINEA DEL ARCHIVO
    coeficientes = condiciones[1]

    # RESTO DEL ARCHIVO
    # GENERA LA LISTA CON LAS RESTRICCIONES
    ind = 2
    listaRestricciones = []
    while ind <= len(condiciones) - 1:
        listaRestricciones.append(condiciones[ind])
        ind += 1

    matriz = crearMatriz(variables, restricciones)  # SE CREA LA MATRIZ
    llenarMatriz(matriz, coeficientes, listaRestricciones, variables,
                 optimizacion)  # SE LLENA LA MATRIZ CON LOS VALORES DEL ARCHIVO
    # imprimirMatriz(matriz) #SE IMPRIME LA MATRIZ

    # DECISION DE METODO, EJECUCION Y SOLUCION
    print(Metodo(metodo, matriz))

    # print(colMenor, filMenor)
    # print(matriz[filMenor][colMenor])


main()

# Para correrlo desde terminal: python simplex.py [-h]python simplex.py [-h] ejemploSimplex3.txt
