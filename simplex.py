import sys
import copy

# VARIABLE GLOBAL PARA ALMACENAR EL PROCEDIMIENTO DE LAS TABLAS INTERMEDIAS
textoSolucion = ""
matrizSolucion = [[]]
variables = 0
solucionNoAcotada = False
nombreArchivoSolucion=""
M = 1000
MFO = 1000
M = 10

# FUNCION PARA LEER EL ARCHIVO .TXT
def leerArhivo():
    global nombreArchivoSolucion
    if (sys.argv[1] != "-h"):
        archivo = sys.argv[1]
    else:
        print("Parametros: -h --help 'Muestra formato de archivo para la ejecucion \n'")
        print(
            "El formato del archivo debe ser: \nmetodo,optimizacion,numeros de variables de decision, numero de restricciones\ncoeficientes de la funcion objetivo\ncoeficientes de las restricciones y signo de restriccion")
        print("Ejemplo: \n0,min,3,3\n1,-2,1\n1,1,1<=,12\n2,1,1,<=,6\n-1,3,<=,9\n\n")
        archivo = sys.argv[2]
    f = open(archivo)
    data = f.read().strip()
    nombreArchivoSolucion = (archivo.split('.'))[0] #recupera el nombre del archivo y lo guarda en la variable global
    f.close()
    condiciones = []
    for line in data.split('\n'): #obtiene los datos del archivo
        condiciones.append(line.split(","))
    return (condiciones)


# LOGICA PARA DEFINIR PROCEDIMIENTO
def Metodo(metodo, variables, restricciones, coeficientes, listaRestricciones, optimizacion):
    # VARIABLES DE CONFIGURACION
    conjuntoSolucion = []
    global textoSolucion
    if metodo == 0:
        matriz = crearMatriz(variables, restricciones)  # SE CREA LA MATRIZ
        llenarMatriz(matriz, coeficientes, listaRestricciones, variables, optimizacion)  # SE LLENA LA MATRIZ CON LOS VALORES DEL ARCHIVO
        textoSolucion += "Solucion Metodo Simplex \n"
        conjuntoSolucion = iteracionSimplex(matriz)

    elif metodo == 1:
        matriz = crearMatrizGranM(variables, restricciones, listaRestricciones, optimizacion, coeficientes)
        llenarMatrizGranM(matriz, variables, listaRestricciones, coeficientes, optimizacion, restricciones)
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


# FUNCION PARA BUSCAR LA POSICION DE UN ELEMENTO EN UNA FILA
def buscarElemEnFila(elemento, fila):
    for x in range(len(fila)):
        if elemento == fila[x]:
            return x


# Identifico todas las restricciones que tienen s de variable basica. A estas filas se multiplica cada valor de su fila
# por -M incluido el LD. Estas filas modificadas se le suman a la funcion objetivo. Finalmente se restaura la funcion
# objetivo en la matriz.
def nuevaFuncionObjetivoM(matriz):

    global MFO
    matrizDuplicada = copy.deepcopy(matriz)
    filaObjetivoSumada = matrizDuplicada[1]

    for x in range(2, len(matriz)): # recorre todas las filas de la matriz

        if (matriz[x][0])[0] == "s": # verifica si hay una s en la restriccion

            for y in range(1, len(matriz[x])): # recorro la fila

                matrizDuplicada[x][y] = matrizDuplicada[x][y] * (-MFO)
                filaObjetivoSumada[y] += matrizDuplicada[x][y] #suma los elementos de cada columna en la nueva funcion objetivo

    print("La matriz normal es")
    imprimirMatriz(matriz)
    matriz[1] = filaObjetivoSumada
    print("LA MATRIZ ES")
    imprimirMatriz(matriz)
    return matriz


# Se crea la funcion para modificar la funcion objetivo pero se mantiene documentada donde se usa porque aun no funciona correctamente
# FUNCION PARA LLENAR LA MATRIZ DE GRAN M
def llenarMatrizGranM(matriz, variables, listaRestricciones, coeficientes, optimizacion, restricciones):

    # Variable global M, normalmente equivalente a un numero muy grande
    global M

    # Se meten las dos que siempre estan, VB y taLD
    matriz[0][0] = "VB"
    matriz[0][len(matriz[0])-1] = "LD"

    # Contadores de las variables de holgura y artificiales
    variableHolgura = 1
    variableArtificial = 1

    # Contador para la columna de todas las variables
    contadorColumna = 1

    # Se meten todas las variables basicas
    for x in range(1, variables + 1):
        matriz[0][x] = "x" + str(x)
        variableHolgura += 1
        contadorColumna += 1

    # Se meten las variables de holgura o artificiales
    for restriccion in listaRestricciones:
        desigualdad = restriccion[len(restriccion)-2]
        # Si la desigualdad es mayor o igual
        if desigualdad == ">=":
            # Se agrega la variable artificial y holgura
            matriz[0][contadorColumna] = "s" + str(variableArtificial)
            matriz[0][contadorColumna + 1] = "x" + str(variableHolgura)
            variableHolgura += 1
            variableArtificial += 1
            contadorColumna += 2
        # Si la desigualdad es igual
        elif desigualdad == "=":
            # Se agrega variable artificial
            matriz[0][contadorColumna] = "s" + str(variableArtificial)
            variableArtificial += 1
            contadorColumna += 1
        # Si la desigualdad es menor o igual
        elif desigualdad == "<=":
            # Se agrega variable de holgura
            matriz[0][contadorColumna] = "x" + str(variableHolgura)
            variableHolgura += 1
            contadorColumna += 1

    # Se agrega la variable basica U
    matriz[1][0] = "U"

    # Para el contenido de los coeficientes de las variables de la funcion objetivo
    for x in range(len(coeficientes)):
        matriz[1][x + 1] = float(coeficientes[x]) * (-1)
        matriz[0][x + 1] = "x" + str(x + 1)

    # Para el contenido de las variables artificales de la funcion objetivo
    if optimizacion == "min":
        M = (M * (-1))

    for x in range(1, len(matriz[0])-1):
        posActual = x

        if (matriz[0][posActual])[0] == "s":
            matriz[1][posActual] = float(M)

    # Para todas las restricciones~~~filas~~~
    for x in range(len(listaRestricciones)):
        # Se toma la restriccion actual
        restriccion = listaRestricciones[x]

        #~~~columnas~~~
        for i in range(len(restriccion)):
            # Si esta en la ultima posicion de la restriccion
            if i == (len(restriccion)-1):
                matriz[2 + x][len(matriz[0])-1] = float(restriccion[i])
            # Si esta en la posicion de la desigualdad en la restriccion
            elif i == (len(restriccion)-2):
                pass
            # Para todas las demas
            else:
                matriz[2 + x][1 + i] = float(restriccion[i])

    # Para la matriz identidad de las variables no basicas
    # x son las filas
    # y son las columnas
    y = 1 + variables
    for x in range(restricciones):
        restriccion = listaRestricciones[x]
        desigualdad = restriccion[len(restriccion) - 2]
        restriccion = listaRestricciones[x]
        if desigualdad == ">=":
            # Se agrega el 1 de la variable artificial y el -1 de la variable de holgura
            matriz[2 + x][y] = 1
            matriz[2 + x][y + 1] = -1
            y += 2
        # Si la desigualdad es igual
        elif desigualdad == "=":
            # Se agrega el 1 de la variable artificial
            matriz[2 + x][y] = 1
            y += 1
        # Si la desigualdad es menor o igual
        elif desigualdad == "<=":
            # Se agrega el 1 de la variable de holgura
            matriz[2 + x][y] = 1
            y += 1
        x += 1

    # Para todas las restricciones
    for x in range(len(listaRestricciones)):
        # Se busca el numero mayor de las variables no basicas para tomar su variable como basica
        maximo = max(matriz[x + 2][(1 + variables):][:-1])
        col = buscarElemEnFila(maximo, matriz[x + 2][(1 + variables):][:-1])
        matriz[2 + x][0] = matriz[0][col + 3]



    print("LA funcion normal es")
    imprimirMatriz(matriz)
    print("Funcion modificada es")
    imprimirMatriz(matriz)

    nuevaFuncionObjetivoM(matriz)


# Se crea la funcion para modificar la funcion objetivo pero se mantiene documentada donde se usa porque aun no funciona correctamente

# FUNCION PARA CREAR LA MATRIZ DE GRAN M
def crearMatrizGranM(variables, restricciones, listaRestricciones, optimizacion, coeficientes):
    columnas = 2 + variables
    filas = 2 + restricciones

    contadorIguales = 0
    contadorMayorIgual = 0
    contador = 1 + variables

    for restriccion in listaRestricciones:

        if restriccion[len(restriccion) - 2] == "=":
            contadorIguales += 1

        elif restriccion[len(restriccion) - 2] == ">=":
            contadorMayorIgual += 1
            contador += 1

        contador += 1

    columnasExtra = 0
    if contadorMayorIgual != 0:
        columnasExtra += contadorMayorIgual * 2

    if contadorIguales != 0:
        columnasExtra += contadorIguales

    columnasExtra += abs(restricciones - (contadorIguales + contadorMayorIgual))
    matriz = [[0 for i in range(columnas + columnasExtra)] for j in range(filas)]


    return matriz


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


# FUNCION PARA LLENAR LA MATRIZ CON LAS RESTRICCIONES
def llenarMatriz(matriz, coeficientes, listaRestricciones, variables, optimizacion):
    # CONVERSION FUNCION OBJETIVO (FALTA AGREGAR CASO MIN)
    for x in range(len(coeficientes)):
        # if (optimizacion == "max"):
        # CASO MAX
        matriz[1][x + 1] = float(coeficientes[x]) * (-1)
    # else:

    # LLENA LAS RESTRICCIONES EN LA MATRIZ
    for i in range(len(listaRestricciones)):
        j = 1
        p = 0
        while j < (len(matriz[0])):
            if p == len(listaRestricciones[i]) - 2:
                # RESULTADOS DE EQUIVALENCIAS
                matriz[i + 2][len(matriz[0]) - 1] = float(listaRestricciones[i][p + 1])
                break
            else:
                # COEFICIENTES
                matriz[i + 2][j] = float(listaRestricciones[i][p])
            j += 1
            p += 1
    i = 2

    # RELLENA LA MATRIZ IDENTIDAD
    for x in range(len(matriz[0]) - variables - 2):
        matriz[2 + x][1 + variables + x] = 1


# FUNCION PARA BUSCAR LA COLUMNA CON EL NUMERO MENOR EN LA FUNCION OBJETIVO
def buscaColMenor(matriz):
    pos = 0
    menor = 999999999
    for x in range(1, len(matriz[0])):
        elemActual = matriz[1][x]
        if elemActual < menor:
            pos = x
            menor = elemActual
    return pos


# FUNCION PARA BUSCAR LA FILA QUE DIVIDA AL LADO DERECHO CON EL MENOR RESULTADO
def buscarFilMenor(matriz, colMenor):
    i = 2
    filMenor = 999999999
    resultado = 0
    while i < len(matriz):
        #print(str(matriz[i][colMenor]));
        #print(str((matriz[i][len(matriz[i]) - 1])))
        if (matriz[i][colMenor] != 0) and (matriz[i][len(matriz[i]) - 1] != 0):
            valorLD = (matriz[i][len(matriz[i]) - 1] / matriz[i][colMenor])
           #print("valor LD "+str(valorLD) + " en "+str(matriz[i][len(matriz[i]) - 1])+ "con"+ str(matriz[i][colMenor]))
            if ((valorLD < filMenor) and(valorLD > 0)):
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
# derecho la solucion es degenerada >Para todas las iteraciones<
def esDegenerada(matriz, variables):
    for i in range(2, len(matriz)):
        if (matriz[i][len(matriz[0])-1] == 0):
            return True
    return False


# Para las soluciones multiples. Si en la ultima iteracion hay una variable basica que el resultado en su
# lado derecho es cero, la solucion muestra multiples soluciones {se hace en la ultima iteracion}
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
def esNoFactible(matriz):
    for i in range(0, len(matriz)):
        if str(matriz[i][0]).find("S") != -1: #busca si contiene una s en la primera columna
            return True
    return False

# Para el final del recorrido. Compone lo que seria las soluciones para escribirlas en el archivo de texto
# Verifica la fila de variables con la columna 0 final, para obtener si hay soluciones para las variables basicas
def crearBasicaFactible(matriz):

    solucionBasica = "Respuesta Final: Z = "+str(matriz[1][len(matriz[1])-1]) +" con, BF = ("
    arregloSoluciones = [0]*(len(matriz[0])-2)

    #recorre las columnas
    for j in range(1, len(matriz[0])-1):

        #recorre las filas
        for i in range(2, len(matriz)):

            if (matriz[0][j] == matriz[i][0]):
                    arregloSoluciones[j-1] = matriz[i][len(matriz[1])-1]

    solucionBasica += ', '.join([str(elem) for elem in arregloSoluciones])+ ")"
    return solucionBasica

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

        # APLICAMOS CAMBIOS AL RESTO DE LAS FILAS SEGUN NUESTRA PIVOTE
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
        textoSolucion += "La iteracion "+str(iteracion)+" presento una solucion no acotada\n"


    return textoSolucion


def main():
    global nombreArchivoSolucion

    # LEER EL ARCHIVO
    condiciones = leerArhivo()
    nombreArchivoSolucion += "_Solution.txt"  # agregamos el sufijo al nombre del archivo

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

    # DECISION DE METODO, EJECUCION Y SOLUCION
    texto = Metodo(metodo, variables, restricciones, coeficientes, listaRestricciones, optimizacion)
    archivoSolucion = open(nombreArchivoSolucion, "w")
    if (solucionNoAcotada == False):

        #escribe el contenido de las iteraciones y demas
        archivoSolucion.write(texto)


        print("Matriz Solucion Final: ")
        imprimirMatriz(matrizSolucion)
        archivoSolucion.write("Matriz Solucion Final: \n "+matrizToString(matrizSolucion)+"\n")

        # EVALUACION DE LA MATRIZ FINAL
        if(esMultiple(matrizSolucion)):
            archivoSolucion.write("La solucion es multiple")
            print("La solucion es multiple")



    BF = crearBasicaFactible(matrizSolucion)
    print(BF)
    texto += BF
    archivoSolucion.write(texto)
    archivoSolucion.close()


main()

# Para correrlo desde terminal: python simplex.py -h archivo.txt
