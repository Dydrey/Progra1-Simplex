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

condiciones = leerArhivo()

definicion = condiciones[0]

metodo = int(definicion[0])
optimizacion = definicion[1]
variables = int(definicion[2])
restricciones = int(definicion[3])

coeficientes = condiciones[1]

Metodo(metodo)

#Para correrlo desde terminal: python simplex.py [-h] archivo.txt
