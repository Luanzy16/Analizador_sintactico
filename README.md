# Lexer y Analizador Sintáctico (Parser) Básico para un Subconjunto de Python

Este proyecto implementa un analizador léxico (lexer) y un analizador sintáctico (parser) para un pequeño subconjunto del lenguaje de programación Python. Es una herramienta educativa diseñada para ilustrar los procesos de tokenización y análisis de la estructura de un programa, utilizando la técnica de análisis descendente recursivo manual y explicando su relación con un autómata con pila.

## Componentes del Proyecto

1.  **`lexico.py`**: Contiene la implementación del **Analizador Léxico (Lexer)**. Su trabajo es leer el código fuente y convertirlo en una secuencia de tokens.
2.  **`parser.py`**: Contiene la clase **`ManualRecursiveParser`**, que implementa el **Analizador Sintáctico (Parser)**, y la función `main_analisis_sintactico` que orquesta el proceso.

## Características Soportadas

El parser soporta un subconjunto simplificado de la sintaxis de Python, incluyendo:

* **Variables:** Declaración e uso básico de identificadores (`id`).
* **Asignaciones:** Sentencias de asignación simples (`id = expresion`).
* **Condiciones:** Sentencias `if`, `elif` (cero o más), y `else` (opcional).
* **Bucles:** Sentencias `while`.
* **Funciones:** Definiciones básicas (`def nombre(): ...`) sin soporte para parámetros o argumentos.
* **Retorno:** Sentencia `return` (opcionalmente con una expresión).
* **Sentencia `pass`:** La sentencia `pass`.
* **Impresión:** Llamada básica a la función `print(expresion)`.
* **Operaciones:** Expresiones aritméticas básicas (`+`, `-`, `*`, `/`) con precedencia implícita por la estructura de las reglas, y operadores de comparación (`==`, `!=`, `<`, `>`, `<=`, `>=`).
* **Agrupación:** Uso de paréntesis `()` en expresiones.
* **Bloques de Código:** Manejo de la estructura de bloques basada en la indentación, utilizando tokens `INDENT` y `DEDENT` proporcionados por el lexer.
* **Tokens Especiales:** Reconocimiento de `INDENT`, `DEDENT`, y `EOF` (End Of File).
* **Manejo Básico de Tokens:** Identificación de números enteros (`tk_entero`) y cadenas (`tk_cadena`).
* **Ignora:** Comentarios (`#`) y espacios en blanco irrelevantes.
* **Reporte de Errores:** Detecta el primer error léxico (formato de token inválido) o sintáctico (secuencia de tokens inesperada) y reporta su ubicación (fila y columna) correctamente.

## Cómo Usar

1.  Asegúrate de tener Python instalado en tu sistema.
2.  Guarda el código del lexer en un archivo llamado `lexico.py`.
3.  Guarda el código del parser (incluyendo la clase `ManualRecursiveParser` y la función `main_analisis_sintactico`) en un archivo llamado `parser.py`.
4.  Crea un archivo de texto con extensión `.py` (por ejemplo, `ejemplo.py`) conteniendo código Python que se ajuste al subconjunto de gramática soportado.
5.  Abre una terminal o línea de comandos en el directorio donde guardaste los archivos.
6.  Ejecuta el script `parser.py` pasando el nombre de tu archivo de entrada como argumento:

    ```bash
    python parser.py ejemplo.py
    ```
    (Nota: El script `parser.py` está configurado por defecto para usar `ejemplo_sintactico.py` como archivo de entrada si no se especifica otro, y `salida_sintactica.txt` como salida).

7.  El lexer generará un archivo intermedio con los tokens (ej. `ejemplo_tokens.txt`).
8.  El parser leerá los tokens y realizará el análisis sintáctico.
9.  El resultado del análisis (éxito o el primer error encontrado) se escribirá en el archivo de salida especificado (ej. `salida_sintactica.txt`).

## Cómo Funciona

### 1. Análisis Léxico (`lexico.py`)

El lexer lee el archivo de código fuente carácter por carácter. Su función es agrupar secuencias de caracteres en unidades significativas llamadas **tokens**. Por ejemplo, `x = 10` se convierte en la secuencia de tokens `id`, `tk_asign`, `tk_entero`.

El lexer es responsable de:

* Ignorar espacios en blanco y comentarios.
* Identificar diferentes tipos de tokens (palabras clave, identificadores, números, cadenas, operadores, puntuación).
* Un aspecto crucial para Python: **Detectar los cambios en los niveles de indentación** al principio de las líneas lógicas y generar tokens especiales `INDENT` (cuando la indentación aumenta) y `DEDENT` (cuando disminuye).
* Generar un token `EOF` al final del archivo.
* Formatear cada token como un string `<TIPO,LEXEMA,FILA,COL>`.

### 2. Análisis Sintáctico (`parser.py`)

El parser toma la lista de tokens generada por el lexer como su entrada. Su tarea es verificar si la secuencia de tokens se ajusta a la gramática del lenguaje y, conceptualmente, construir un árbol de análisis sintáctico (aunque no se construye explícitamente en este código). Si la secuencia de tokens no cumple las reglas gramaticales, reporta un error.

Este parser utiliza la técnica de **Análisis Sintáctico Descendente Recursivo Manual**. Esto significa que:

* Cada **regla no terminal** de la gramática (ej. `statement`, `if_stmt`, `expression`) está implementada como un **método (función)** en la clase `ManualRecursiveParser`.
* Estos métodos se llaman recursivamente unos a otros, siguiendo la estructura jerárquica de la gramática. Por ejemplo, el método `_if_stmt` llama al método `_comparison` para parsear la condición y al método `_suite` para parsear el bloque de código indentado.
* El método **`_match(expected_type)`** es el mecanismo central para interactuar con la entrada de tokens. Compara el tipo del token actual (`_peek()`) con el tipo esperado. Si coinciden, **consume** el token actual (`_consume()`) y avanza al siguiente. Si no, indica un error sintáctico.
* El método **`_peek()`** permite "mirar" el próximo token de la entrada sin consumirlo, lo cual es vital para decidir qué regla aplicar cuando hay múltiples opciones (ej. en `_statement`, se mira el primer token para saber si es una asignación, un `if`, un `while`, etc.). Esto lo convierte en un parser *predictivo* simple.

### 3. Implementación como un Autómata con Pila (AP)

Aunque el código no define explícitamente los estados y una estructura de datos de pila, **el analizador descendente recursivo se comporta como un Autómata con Pila Determinista (APD)**. La analogía es la siguiente:

* **Estados del AP:** El "estado" del AP está implícito en **qué método de regla gramatical se está ejecutando** y **en qué punto de su ejecución se encuentra**.
* **Alfabeto de Entrada ($\Sigma$):** Son los **tokens terminales** proporcionados por el lexer.
* **Alfabeto de la Pila ($\Gamma$):** Está compuesto por los **símbolos no terminales** de tu gramática (los nombres de tus métodos: `_program`, `_statement`, `_suite`, etc.).
* **La Pila (Stack):** ¡Esta es la **pila de llamadas (call stack)** del programa!
    * Cuando un método `A` llama a un método `B` (que representa una sub-regla no terminal), el sistema operativo **empuja (push)** el contexto de `A` (incluida la dirección de retorno) en la cima de la pila de llamadas y comienza a ejecutar `B`. Conceptualmente, esto es análogo a que el AP reemplace el no terminal `A` en la cima de su pila por los símbolos del lado derecho de la producción que comienza con `B`, y `B` es ahora el nuevo símbolo a procesar en la cima conceptual.
    * Cuando un método `B` termina de ejecutarse (porque ha parseado exitosamente la sub-estructura que representaba), **retorna**. Esto es análogo a **sacar (pop)** el no terminal `B` de la cima de la pila del AP. La ejecución regresa a donde `A` se quedó, en la cima conceptual de la pila del AP.
* **Función de Transición ($\delta$):** La lógica dentro de cada método (las llamadas a `_match`, las llamadas recursivas a otros métodos, y las estructuras `if/elif/else/while` que usan `_peek`) implementa la función de transición. Decide qué hacer (consumir un terminal, llamar a otro método, o retornar) basándose en el estado implícito (la función actual) y el próximo token de entrada (`_peek()`).
* **Símbolo Inicial de la Pila:** El símbolo inicial es `_program`, puesto implícitamente por la llamada inicial en `parse()`.
* **Condición de Aceptación:** El análisis es exitoso si se consume toda la entrada (`EOF`) y la pila de llamadas está vacía (es decir, la llamada inicial a `_program` ha retornado), lo que significa que toda la estructura definida por la regla `_program` ha sido reconocida.

En resumen, la recursión en el código simula el manejo de la pila de un autómata con pila de manera implícita, haciendo que la implementación sea directa y corresponda visualmente a la estructura de la gramática descendente.

## Reporte de Errores

El parser reporta el **primer error** sintáctico o de formato de token que encuentra. Utiliza una excepción (`SyntaxError`) para detener la ejecución del análisis tan pronto como se detecta un error. El mensaje de error incluye la **fila y columna exactas** donde se encontró el token inesperado o con formato incorrecto.

## Limitaciones

Este proyecto es una implementación educativa y no un parser completo de Python. No soporta la gramática completa del lenguaje, incluyendo (pero no limitado a):

* Clases
* Importaciones
* Manejo de excepciones (`try`, `except`, `finally`)
* Decoradores
* Generadores (`yield`)
* Bucles `for` cuanto tiene varios argumentos
* Sentencias `break`, `continue`
* Argumentos y parámetros de funciones
* Tipos de datos más complejos (listas, diccionarios, etc.) y sus operaciones (indexación, slicing)
* Operadores avanzados (operadores lógicos `and`/`or`/`not`, bit a bit, etc.)
* Comprehensions de lista/diccionario/conjunto
* Expresiones lambda complejas

## Archivos

* `lexico.py`: Contiene la implementación del lexer.
* `parser.py`: Contiene la clase `ManualRecursiveParser` y la lógica principal de ejecución (`main_analisis_sintactico`).
* `ejemplo_sintactico.py`: (Opcional) Un archivo de ejemplo para probar el parser.
* `ejemplo_sintactico_tokens.txt`: (Generado por el lexer) La salida de tokens del archivo de entrada.
* `salida_sintactica.txt`: (Generado por el parser) El resultado del análisis sintáctico.

---