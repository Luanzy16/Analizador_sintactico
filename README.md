# Lexer y Parser Básico para un Subconjunto de la gramtica de Python

Este proyecto implementa un **analizador léxico** (`lexer`) y un **analizador sintáctico** (`parser`) para un subconjunto reducido de la gramatica de Python.
---

##  Estructura del Proyecto

| Archivo         | Descripción                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `lexico.py`     | Implementa el **lexer**: convierte el código fuente en una lista de tokens. |
| `parser.py`     | Contiene la clase `ManualRecursiveParser` y la función `main_analisis_sintactico`. |
| `ejemplo_sintactico.py` | Código Python de prueba (opcional).                                      |
| `ejemplo_sintactico_tokens.txt` | Tokens generados por el lexer.                                   |
| `salida_sintactica.txt` | Resultado del análisis sintáctico (éxito o error).                      |

---

## Características Soportadas

El parser reconoce un subconjunto de Python que incluye:

- ✅ Variables e identificadores
- ✅ Asignaciones simples (`id = expresión`)
- ✅ Condicionales: `if`, `elif`, `else`
- ✅ Bucles `while`
- ✅ Funciones: `def nombre(): ...` 
- ✅ Sentencia `return`
- ✅ Sentencia `pass`
- ✅ Impresión: `print(expresión)`
- ✅ Expresiones aritméticas y comparaciones
- ✅ Indentación con `INDENT` / `DEDENT`
- ✅ Tokens: números (`tk_entero`), cadenas (`tk_cadena`)
- ✅ Ignora comentarios y espacios innecesarios
- ✅ Reporte del **primer error** léxico o sintáctico con **fila y columna**

---

## Cómo Usar

1. Asegúrate de tener Python instalado.
2. Guarda los archivos `lexico.py` y `parser.py`.
3. Crea un archivo de prueba, por ejemplo `ejemplo.py`.
4. Ejecuta en la terminal:

```bash
python parser.py
```

---

## 🔍 Cómo Funciona

### 🧩 Lexer (`lexico.py`)

- Convierte el código fuente en una **lista de tokens**
- Ignora comentarios y espacios
- Reconoce indentación (`INDENT` / `DEDENT`)
- Agrega `EOF` al final
- Formato de token: `<TIPO,LEXEMA,FILA,COL>`

---

### 🧠 Parser (`parser.py`)

- Verifica si la secuencia de tokens sigue las **reglas gramaticales**
- Usa **análisis descendente recursivo**
- Cada no terminal se implementa como un **método**
- Si hay error, lanza una excepción con la posición exacta

---


## ⚠️ Limitaciones

Este parser **no** soporta:

- Clases, módulos e importaciones
- Excepciones (`try`, `except`)
- Decoradores y generadores
- Tipos de datos compuestos 
- Operadores lógicos y bit a bit
- Sentencias `break`, `continue`

