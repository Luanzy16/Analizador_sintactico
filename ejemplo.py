# Ejemplo 1: Sentencias simples y asignación
a = 10
b = 20
c = a + b * 2
nombre = "Parser Test"
pass # Una sentencia 'pass' simple

# Ejemplo 2: Condicionales (if, elif, else)
if c > 50:
    print("c es grande") # print con un argumento cadena
    otro_valor = c - 50
elif c == 50:
    print("c es 50")
else:
    print("c es pequeño")
    pass # Bloque else con pass

# Ejemplo 3: Bucle While
contador = 0
while contador < 5: # Comparación como condición
    print(contador) # Llamada a print con un argumento variable
    contador = contador + 1 # Asignación con expresión

# Ejemplo 4: Definición y llamada a función
def saludar(): # Definición de función sin parámetros
    print("Hola desde la funcion")
    return 123 # Retorno con valor

# Llamadas a funciones como sentencias o en expresiones
saludar() # Llamada a función sin argumentos como sentencia
mi_resultado = saludar() # Llamada a función sin argumentos en asignación

def sumar(x, y): # Nota: El parser actual no valida los parámetros 'x, y' en 'def'
    temp = x + y
    return temp # Retorno con variable/expresión

resultado_suma = sumar(a, b) # Llamada a función con 2 argumentos (variables)
final = sumar(100, resultado_suma * 2) # Llamada con argumentos que son expresiones

# Ejemplo 5: Bucle For con range (1, 2 y 3 argumentos)
print("Inicio del bucle for")
for i in range(5): # range con 1 argumento
    print(i)

for j in range(a, b): # range con 2 argumentos (variables)
    print(j)

for k in range(0, 20, 2): # range con 3 argumentos (literales)
    print(k)

# Ejemplo 6: Anidamiento y combinación
def calcular_y_mostrar(val):
    temp_calc = val * 10
    print(temp_calc) # Llamada a print

for iter in range(3):
    if iter > 0:
        calcular_y_mostrar(iter) # Llamada a función dentro de if dentro de for
    else:
        pass

final = 999 # Sentencia final