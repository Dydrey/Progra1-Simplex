import sys
from fractions import Fraction

# VARIABLE GLOBAL PARA ALMACENAR EL PROCEDIMIENTO DE LAS TABLAS INTERMEDIAS
textoSolucion = ""
matrizSolucion = [[]]
variables = 0
solucionNoAcotada = False
M = 1000


# FUNCION PARA LEER EL ARCHIVO .TXT
def leerArhivo():
    if (sys.argv[1] != "-h"):
        archivo = sys.argv[1]
    else:
        print("Parametros: -h --help 'Muestra formato de archivo para la ejecucion \n'")
        print(
            "El formato del archivo debe ser: \nmetodo,optimizacion,numeros de variables de decision, numero de restricciones\ncoeficientes de la funcion objetivo\ncoeficientes de las restricciones y signo de restriccion")
        print("Ejemplo: \n 0,min,3,3\n1,-2,1\n1,1,1<=,12\n2,1,1,<=,6\n-1,3,<=,9\n\n")
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
        textoSolucion += "Solucion Metodo Simplex \n"
        conjuntoSolucion = iteracionSimplex(matriz)

    elif metodo == 1:
        print("Gran M")
        textoSolucion = "Solucion Metodo Gran M \n"
        conjuntoSolucion = iteracionSimplex(matriz)
    elif metodo == 2:
        print("Dos Fases")
        textoSolucion = "Solucion Metodo Dos Fases \n"
    # llamada a funcion de Dos Fases
    else:
        return ("Error de metodo")
    #VERIFICA EL RESULTADO DE LA MATRIZ
    #textoSolucion += verificarMatriz(matriz)
    return conjuntoSolucion


# IMPRIME LA MATRIZ
def imprimirMatriz(matriz):
    for row in matriz:
        print(' \t'.join(map(str, row)))


# CREACION DE LA MATRIZ
def crearMatriz(variables, restricciones, listaRestricciones, coeficientes, optimizacion, metodo):
    columnas = 2 + variables
    filas = 2 + restricciones

    contadorIguales = 0
    contadorMayorIgual = 0
    banderaGranM = False
    listaPoscionesGranM = []
    contador = 1 + variables

    for restriccion in listaRestricciones:
        # ESTE If ES PARA CREAR MATRIZ DE <=

        if restriccion[len(restriccion) - 2] == "=":
            banderaGranM = True
            contadorIguales += 1
            listaPoscionesGranM.append(contador)

        elif restriccion[len(restriccion) - 2] == ">=":
            banderaGranM = True
            contadorMayorIgual += 1
            contador += 1
            listaPoscionesGranM.append(contador)

        contador += 1

    if metodo == 0:

        if restriccion[len(restriccion) - 2] == "<=":
            matriz = [[0 for i in range(columnas + restricciones)] for j in range(filas)]
            # ESTE FOR ES PARA LA FILA SUPERIOR
            for x in range(len(matriz[0])):
                if x == 0:
                    matriz[0][x] = "VB"
                elif x == len(matriz[0]) - 1:
                    matriz[0][x] = "LD"
                else:
                    matriz[0][x] = "x" + str(x)
            # ESTE FOR ES PARA LA COLUMNA DE LA IZQUIERDA
            for y in range(len(matriz)):
                if y == 0:
                    matriz[y][0] = "VB"
                elif y == 1:
                    matriz[y][0] = "U"
                else:
                    matriz[y][0] = "x" + str(variables + 1)
                    variables += 1
        llenarMatriz(matriz, coeficientes, listaRestricciones, variables, optimizacion, [])

    if metodo == 1:
        columnasExtra = 0
        if contadorMayorIgual != 0:
            columnasExtra += contadorMayorIgual * 2

        if contadorIguales != 0:
            columnasExtra += contadorIguales

        columnasExtra += abs(restricciones - (contadorIguales + contadorMayorIgual))
        matriz = [[0 for i in range(columnas + columnasExtra)] for j in range(filas)]
        llenarMatriz(matriz, coeficientes, listaRestricciones, variables, optimizacion, listaPoscionesGranM)
        imprimirMatriz(matriz)

    return matriz


# DEVUELVE LA MATRIZ EN STRING PARA GUARDARLA EN ARCHIVO
def matrizToString(matriz):
    stringMatriz = ""
    for row in matriz:
        stringMatriz = stringMatriz + (' \t'.join(map(str, row))) + "\n"
    return stringMatriz


# PEQUEÑA FUNCION PARA MOSTRAR LOS DECIMALES EN FRACCIONES
def fraccion(numeroParaFraccion):
    return str(Fraction(numeroParaFraccion).limit_denominator())


def buscarElemEnFila(elemento, fila):
    for x in range(len(fila)):
        if elemento == fila[x]:
            return x

def nuevaFuncionObjetivoM(matriz):
    nuevaFuncion = matriz[1]
    for i in range(len(matriz)): #recorre todas las filas de la matriz
        if (str(matriz[i][0]).find("S") != -1): #verifica si hay una s en las filas
            for k in range(1, len(matriz[i][0])-1): #pivote para recorrer las columnas de la fila encontrada
                matriz[i][k] = matriz[i][k] * (-M)
                nuevaFuncion[0][k] += matriz[i][k] #suma los elementos de cada columna en la nueva funcion objetivo
    matriz[1] = nuevaFuncion
    return matriz

# FUNCION PARA LLENAR LA MATRIZ CON LAS RESTRICCIONES
def llenarMatriz(matriz, coeficientes, listaRestricciones, variables, optimizacion, listaArtificial):

    global M

    if (len(listaArtificial) == 0):
        # Llena la funcion objetivo
        for x in range(len(coeficientes)):
            matriz[1][x + 1] = float(coeficientes[x]) * (-1)

        # LLENA LAS RESTRICCIONES EN LA MATRIZ
        posListaRestriccion = 0
        banderaDesigualdad = False

        # Para cada restriccion en lista de restricciones
        for i in range(len(listaRestricciones)):
            j = 1
            p = 0
            while j < (len(matriz[0])):
                if p == len(listaRestricciones[i]) - 2:
                    matriz[i + 2][len(matriz[0]) - 1] = float(listaRestricciones[i][p+1])
                    break
                else:
                    # COEFICIENTES
                    matriz[i + 2][j] = float(listaRestricciones[i][p])
                j += 1
                p += 1

        # RELLENA LA MATRIZ IDENTIDAD
        for x in range(len(matriz[0]) - variables - 2):
            matriz[2 + x][1 + variables + x] = 1

    else:
        matriz[1][0] = "U"
        matriz[0][0] = "VB"
        matriz[0][len(matriz[0]) - 1] = "LD"
        for x in range(len(coeficientes)):
            matriz[1][x + 1] = float(coeficientes[x]) * (-1)
            matriz[0][x + 1] = "x" + str(x + 1)

        if optimizacion == "min":
            for x in range(len(listaArtificial)):
                matriz[1][listaArtificial[x]] = (matriz[1][listaArtificial[x]] - M)
                matriz[0][listaArtificial[x]] = "S" + str(x + 1)
        elif optimizacion == "max":
            for x in range(len(listaArtificial)):
                matriz[1][listaArtificial[x]] = (matriz[1][listaArtificial[x]] + M)
                matriz[0][listaArtificial[x]] = "S" + str(x + 1)


        # RECORRO LA CANTIDAD DE RESTRICCIONES
        contadorRestriccion = 0

        for i in range(len(listaRestricciones)):
            # LA RESTRICCION ES SEGUN EL INDICE EN LA LISTA DE RESTRICCIONES
            restriccion = listaRestricciones[i]

            # SI ES DE TIPO <=
            if restriccion[len(restriccion) - 2] == "<=":

                j = 1 #indice de las variables
                for p in range(len(restriccion)):

                    if p == len(listaRestricciones[i]) - 2:
                        matriz[i + 2][1 + variables + contadorRestriccion] = 1
                        matriz[0][1 + variables + contadorRestriccion] = "x" + str(variables + contadorRestriccion + 1)
                        contadorRestriccion += 1

                    elif p == len(listaRestricciones):
                        matriz[i + 2][len(matriz[0]) - 1] = float(restriccion[p])
                    else:
                        # COEFICIENTES
                        matriz[i + 2][j] = float(restriccion[p])
                    j += 1

                maximo = max(matriz[i + 2][(1 + variables):][:-1])
                col = buscarElemEnFila(maximo, matriz[i + 2][(1 + variables):][:-1])
                matriz[2+i][0] = matriz[0][col + 3]

            elif restriccion[len(restriccion) - 2] == "=":
                j = 1  # indice de las variables
                for p in range(len(restriccion)):

                    if p == len(listaRestricciones[i]) - 2:
                        matriz[i + 2][1 + variables + contadorRestriccion] = 1

                    elif p == len(listaRestricciones):
                        matriz[i + 2][len(matriz[0]) - 1] = float(restriccion[p])

                    else:
                        # COEFICIENTES
                        matriz[i + 2][j] = float(restriccion[p])

                    j += 1

                maximo = max(matriz[i + 2][(1 + variables):][:-1])
                col = buscarElemEnFila(maximo, matriz[i + 2][(1 + variables):][:-1])
                matriz[2 + i][0] = matriz[0][col + 3]


            elif restriccion[len(restriccion) - 2] == ">=":
                j = 1  # indice de las variables
                for p in range(len(restriccion)):

                    if p == len(listaRestricciones[i]) - 2:
                        matriz[i + 2][1 + variables + contadorRestriccion + 1] = -1
                        matriz[i + 2][1 + variables + contadorRestriccion + 2] = 1

                    elif p == len(listaRestricciones):
                        matriz[i + 2][len(matriz[0]) - 1] = float(restriccion[p])

                    else:
                        # COEFICIENTES
                        matriz[i + 2][j] = float(restriccion[p])

                    j += 1

                maximo = max(matriz[i + 2][(1 + variables):][:-1])
                col = buscarElemEnFila(maximo, matriz[i + 2][(1 + variables):][:-1])
                matriz[2 + i][0] = matriz[0][col + 3]

        matriz = nuevaFuncionObjetivoM(matriz)



# FUNCION PARA BUSCAR LA COLUMNA CON EL NUMERO MENOR EN LA FUNCION OBJETIVO
def buscaColMenor(matriz):
    pos = 0
    menor = 99999
    for x in range(1, len(matriz[0])):
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


# FUNCION PARA SABER SI UNA VARIABLE ES BASICA
def esVB(matriz, variable):
    for i in range(2, len(matriz)):
        #print("Comparando " + variable + " con " + str(matriz[i][0]))
        if matriz[i][0] == variable:
            #print("Existe " + variable)
            return True
   # print("No existe " + variable)
    return False


# Para las soluciones degeneradas. Si en cualqueir iteracion hay una variable basica con valor o igual a cero en el lado
#derecho la solucion es degenerada >Para todas las iteraciones<
def esDegenerada(matriz, variables):
    for i in range(2, len(matriz)):
        if (matriz[i][len(matriz[0])-1] == 0):
            return True
    return False


#LISTA
def esMultiple(matriz):
    for i in range(1, len(matriz[0])):
        #print("Existe " + matriz[0][i] + "?")
        existe = esVB(matriz, matriz[0][i])
        if not (existe):
            if (matriz[1][i]) == 0:
                #print("El valor en " + matriz[0][i] + " es cero")
                return True
    return False


# Para solucion no factible. Si al llegar al optino existe una variable basica que es una variable artificial, el problema
# no es factible >Se hace en la ultima<
# def esNoFactible(matriz):


# fPara solucion no acotada. Cuando en U hay un numero negativo (Se pueden hacer iteraciones) y todos los numeros debajo de este
# son negativos o cero entonces la solucion no es acotada >Se hace en cualquier iteracion<
def esNoAcotada(matriz, colMenor):
    contador = 0
    for i in range(1, len(matriz)):
        if (matriz[i][colMenor]) <= 0:
            contador += 1
    if (contador == len(matriz) - 1):
        return True
    return False


# RUTINA PARA LA SOLUCION MODO SIMPLEX
def iteracionSimplex(matriz):
    global textoSolucion
    global matrizSolucion
    global variables
    global solucionNoAcotada
    solucionDegenerada = False

    iteracion = 0
    # BUSCA EL PIVOTE
    colMenor = buscaColMenor(matriz)
    filMenor = buscarFilMenor(matriz, colMenor)

    print("La matriz inicial es")
    imprimirMatriz(matriz)
    print("")

    #GUARDAMOS LA MATRIZ INICIAL EN EL STRING SOLUCION
    textoSolucion += "La matriz inicial es \n"+matrizToString(matriz)+"\n"

    while (matriz[1][colMenor] < 0):

        if (esNoAcotada(matriz,colMenor)):
            solucionNoAcotada = True
            break

        # DATOS SOBRE CUAL VARIABLE SALE Y CUAL ENTRA
        textoSolucion += "La VB que sale es " + matriz[filMenor][0] + "\n"
        textoSolucion += "La VB entrante es: " + matriz[0][colMenor] + "\n"

        # GUARDAMOS EL VALOR DEL PIVOTE PARA LAS ITERACIONES
        numeroPivote = round(float(matriz[filMenor][colMenor]), 3)
        textoSolucion += "El numero Pivote es: " + str(numeroPivote) + "\n"
        # print(textoSolucion)


        # CAMBIAMOS LA VB
        matriz[filMenor][0] = matriz[0][colMenor]

        # CALCULAMOS LA FILA PIVOTE
        for j in range(1, len(matriz[0])):
            matriz[filMenor][j] = round((float(matriz[filMenor][j]) / numeroPivote), 4)

        # APLICAMOS CAMBIOS AL RESTO DE LAS FILAS SEGÚN NUESTRA PIVOTE
        for i in range(1, len(matriz)):
            # EL IF ES PARA EVITAR SOBREESCRIBIR LA FILA PIVOTE
            if (i != filMenor):
                opuesto = (matriz[i][colMenor] * -1)

                for j in range(1, len(matriz[0])):
                    actual = round(float(matriz[i][j]), 3)
                    resultado = actual + (opuesto * matriz[filMenor][j])
                    # ACTUALIZAMOS EL VALOR DE LAS FILAS QUE NO SON LA PIVOTE
                    matriz[i][j] = round(resultado, 3)


        # GUARDAMOS LA MATRIZ EN EL STRING PARA EL ARCHIVO
        textoSolucion += "Estado: " + str(iteracion) + "\n"
        textoSolucion += matrizToString(matriz) + "\n"
        matrizSolucion = matriz

        print("La matriz en la iteracion " + str(iteracion) + " es")
        imprimirMatriz(matriz)
        print("")
        if (esDegenerada(matriz, variables)):
            textoSolucion += "La iteracion "+str(iteracion)+" muestra una solucion Degenerada\n"
            print("Es degenerada")


        iteracion += 1

        # BUSCA EL NUEVO PIVOTE
        colMenor = buscaColMenor(matriz)
        filMenor = buscarFilMenor(matriz, colMenor)
    #AQUI CIERRA EL WHILE

    if (solucionNoAcotada):
        print("La iteracion "+str(iteracion)+" presenta una solucion no acotada")
        textoSolucion += "La iteracion "+str(iteracion)+" presentó una solucion no acotada\n"


    return textoSolucion


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

    matriz = crearMatriz(variables, restricciones, listaRestricciones, coeficientes, optimizacion, metodo)  # SE CREA LA MATRIZ

    # DECISION DE METODO, EJECUCION Y SOLUCION
    texto = Metodo(metodo, matriz)
    if (solucionNoAcotada == False):
        archivoSolucion = open("_solucion.txt", "w")
        archivoSolucion.write(texto)


        print("Matriz Solucion Final: ")
        imprimirMatriz(matrizSolucion)
        archivoSolucion.write("Matriz Solucion Final: \n "+matrizToString(matrizSolucion)+"\n")

        # EVALUACION DE LA MATRIZ FINAL
        if(esMultiple(matrizSolucion)):
            archivoSolucion.write("La solucion es multiple")
            print("La solucion es multiple")

        archivoSolucion.close()
    '''
	if (esNoFactible(matriz)):
		print("La solucion es no factible")
	'''


main()

# Para correrlo desde terminal: python simplex.py -h archivo.txt
