# Ejemplo 1: Sentencias simples y asignación
a = 10
b = 20
c = a + b * 2
nombre = "Parser Test"
pass 

# Ejemplo 2: Condicionales (if, elif, else)
if c > 50:
    print("c es grande") 
    otro_valor = c - 50
elif c == 50:
    print("c es 50")
else:
    print("c es pequeño")
    pass

# Ejemplo 3: Bucle While
contador = 0
while contador < 5:
    print(contador) 
    contador = contador + 1 

# Ejemplo 4: Definición y llamada a función
def saludar(): 
    print("Hola desde la funcion")
    return 123

# Llamadas a funciones como sentencias o en expresiones
saludar() 
mi_resultado = saludar()

def sumar(x, y):
    temp = x + y
    return temp 

resultado_suma = sumar(a, b) 
final = sumar(100, resultado_suma * 2)

# Ejemplo 5: Bucle For con range (1, 2 y 3 argumentos)
print("Inicio del bucle for")
for i in range(5): 
    print(i)

for j in range(a, b): 
    print(j)

for k in range(0, 20, 2): 
    print(k)

# Ejemplo 6: Anidamiento y combinación
def calcular_y_mostrar(val):
    temp_calc = val * 10
    print(temp_calc) 

for iter in range(3):
    if iter > 0:
        calcular_y_mostrar(iter) 
    else:
        pass

final = 999 

#ejemplo 6: listas y llamadas a funciones
var = -1 
x = []

while var <= 6:
    x.append(var)
    var += 1
