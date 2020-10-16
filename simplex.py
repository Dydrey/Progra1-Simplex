import sys

archivo = sys.argv[2]
f = open("archivo.txt")
data = f.read().strip()
f.close()

condiciones = []
for line in data.split('\n'):
    condiciones.append(line.split(","))
print(condiciones)

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

definicion = condiciones[0]
coeficientes = condiciones[1]

metodo = int(definicion[0])
optimizacion = definicion[1]
variables = int(definicion[2])
restricciones = int(definicion[3])
Metodo(metodo)


