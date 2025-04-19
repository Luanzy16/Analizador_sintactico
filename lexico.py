#Diccionario con las palabaras unicas de python
KEYWORDS = {
    # Palabras reservadas de Python
    'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 
    'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield','print',
    
    # Tipos de datos numéricos y de colección
    'int', 'float', 'complex', 'bool', 'list', 'tuple', 'range', 'dict', 'set', 'frozenset', 
    'bytes', 'bytearray', 'memoryview', 'Complex', 'Real', 'Rational', 'Integral', 'Number', 'Union',

    # Funciones matemáticas y constantes
    'abs', 'divmod', 'pow', 'round', 'sum', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 
    'atanh', 'cos', 'cosh', 'sin', 'sinh', 'tan', 'tanh', 'exp', 'log', 'log10', 'log1p', 'log2', 
    'ceil', 'floor', 'trunc', 'radians', 'degrees', 'e', 'pi', 'tau', 'inf', 'nan',

    # Propiedades de solo lectura de números
    'denominator', 'imag', 'numerator', 'real',

    # Booleanos y valores especiales
    'True', 'False', 'None',

    # Excepciones y manejo de errores
    'try', 'except', 'finally', 'raise', 'assert', 'with',
    'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError', 'AttributeError', 
    'ZeroDivisionError', 'FileNotFoundError'
}

#Diccionario con todos los simbolos de operaciones
OPERATORS = {
    "+": "tk_suma", "-": "tk_resta", "*": "tk_mult", "/": "tk_div", "//": "tk_div_entera",
    "%": "tk_mod", "**": "tk_pot", "&": "tk_and_bin", "|": "tk_or_bin", "^": "tk_xor_bin",
    "~": "tk_not_bin", "<<": "tk_despl_izq", ">>": "tk_despl_der", "=": "tk_asign",
    "+=": "tk_suma_asig", "-=": "tk_resta_asig", "*=": "tk_mult_asig", "/=": "tk_div_asig",
    "//=": "tk_div_ent_asig", "%=": "tk_mod_asig", "**=": "tk_pot_asig", "&=": "tk_and_bin_asig",
    "|=": "tk_or_bin_asig", "^=": "tk_xor_bin_asig", "<<=": "tk_despl_izq_asig", ">>=": "tk_despl_der_asig",
    "==": "tk_igual", "!=": "tk_dif", "<": "tk_menor", ">": "tk_mayor", "<=": "tk_menor_igual",
    ">=": "tk_mayor_igual"
}

#Diccionario con los simbolos de puntuacion
PUNCTUATION = {
    "(": "tk_par_izq", ")": "tk_par_der", "[": "tk_cor_izq", "]": "tk_cor_der",
    "{": "tk_llave_izq", "}": "tk_llave_der", ",": "tk_coma", ":": "tk_dos_puntos",
    ";": "tk_punto_coma", ".": "tk_punto"
}


def is_digit(char):
    """
    Verifica si un carácter dado es un dígito (0-9).

    Parámetros:
        char (str): Un solo carácter a evaluar.

    Retorna:
        bool: True si el carácter es un dígito, False en caso contrario.
    """
    return "0" <= char <= "9"


def is_alpha(char):
    """
    Verifica si un carácter dado es una letra (mayúscula, minúscula) o un guion bajo (_).

    Parámetros:
        char (str): Un solo carácter a evaluar.

    Retorna:
        bool: True si el carácter es una letra o "_", False en caso contrario.
    """
    return ("a" <= char <= "z") or ("A" <= char <= "Z") or (char == "_")


def is_alnum(char):
    """
    Verifica si un carácter dado es alfanumérico (letra, dígito o guion bajo).

    Parámetros:
        char (str): Un solo carácter a evaluar.

    Retorna:
        bool: True si el carácter es una letra, un número o "_", False en caso contrario.
    """
    return is_alpha(char) or is_digit(char)


def lexer(filename):
    """
    Analizador léxico (Lexer) que procesa un archivo Python y genera una lista de tokens,
    incluyendo INDENT, DEDENT y EOF.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'")
        return

    tokens = []
    row, col = 1, 1
    i = 0
    length = len(source_code)

    # Stack para rastrear los niveles de indentación. Empieza con 0.
    indent_stack = [0]
    # Bandera para saber si estamos al comienzo de una línea lógica (después de un \n o al inicio del archivo)
    at_line_start = True

    while i < length:
        char = source_code[i]

        # --- Lógica para manejar INDENT/DEDENT al inicio de la línea ---
        if at_line_start:
            # Guardamos la posición actual antes de saltar espacios/comentarios
            start_of_line_i = i
            start_of_line_col = col

            # Saltar espacios y tabulaciones al inicio de la línea
            while i < length and source_code[i] in " \t":
                i += 1
                col += 1

            # Si después de los espacios hay un comentario, saltarlo
            if i < length and source_code[i] == '#':
                while i < length and source_code[i] != '\n':
                    i += 1
                # Ahora i está al final de la línea de comentario o al final del archivo

            # Si la línea es solo espacios, tabs o un comentario (o está vacía después de saltar)
            if i == length or source_code[i] == '\n':
                if i < length and source_code[i] == '\n': # Si hay un salto de línea, consumirlo
                    i += 1
                    row += 1
                    col = 1
                # Mantenemos at_line_start = True para la siguiente iteración (la siguiente línea)
                continue # Ir a la siguiente iteración del bucle

            # Si encontramos contenido no blanco/no comentario, calcular el nivel de indentación
            # La columna `col` ya está en la posición correcta del primer carácter no blanco
            current_indent_level = col - 1 # Los niveles de indentación son 0-basados

            last_indent_level = indent_stack[-1]

            if current_indent_level > last_indent_level:
                # Aumenta la indentación -> INDENT
                tokens.append(f"<INDENT,,{row},{col}>")
                indent_stack.append(current_indent_level)
            elif current_indent_level < last_indent_level:
                # Disminuye la indentación -> DEDENT(s)
                # Sacar niveles del stack hasta que coincida o sea menor
                while indent_stack[-1] > current_indent_level:
                    indent_stack.pop()
                    # Usamos la fila y columna donde el DEDENT lógicamente ocurre (inicio de la nueva línea)
                    tokens.append(f"<DEDENT,,{row},{col}>")

                # Verificar si el nivel actual coincide con alguno en el stack (excepto si el nivel es 0)
                # En un lexer completo, si indent_stack[-1] != current_indent_level y current_indent_level != 0, sería un error.
                if current_indent_level != 0 and indent_stack[-1] != current_indent_level:
                     # >>> Aquí podrías añadir un manejo de error de indentación más sofisticado
                     # Por ahora, solo generamos los DEDENTs necesarios para volver a un nivel válido
                     pass # print(f">>> Error de indentación(linea:{row},posicion:{col})")
                     # break # Podrías detener el lexer aquí

            # Si current_indent_level == last_indent_level, no hacemos nada (no se emite token de indentación)

            # Después de manejar la indentación, ya no estamos al inicio de una línea lógica
            at_line_start = False
            # El índice 'i' y la columna 'col' ya están apuntando al primer carácter relevante de la línea.

        # --- Procesamiento de tokens regulares (después de manejar la indentación) ---

        char = source_code[i] # Obtener el carácter actual (puede que i/col hayan cambiado en la lógica de indentación)

        # Ignorar espacios y tabulaciones que NO están al inicio de la línea (ya que ya manejamos el inicio)
        # Estos espacios son separadores entre tokens
        if char in " \t":
            col += 1
            i += 1
            continue

        # Manejar el salto de línea
        if char == "\n":
            row += 1
            col = 1
            i += 1
            at_line_start = True # La próxima iteración debe verificar la indentación
            continue # Ir a la siguiente iteración

        # Ignorar comentarios (ya se manejan al inicio de la línea, pero por si acaso hay comentarios al final de una línea con código)
        if char == "#":
             while i < length and source_code[i] != "\n":
                 i += 1
             continue


        # Si es un identificador o palabra clave
        if is_alpha(char):
            start_col = col
            lexeme = ""
            while i < length and is_alnum(source_code[i]):
                lexeme += source_code[i]
                i += 1
                col += 1
            if lexeme in KEYWORDS:
                # Según el formato deseado, las palabras clave no tienen lexema en el token, solo el tipo
                tokens.append(f"<{lexeme},,{row},{start_col}>")
            else:
                tokens.append(f"<id,{lexeme},{row},{start_col}>")
            continue # Procesar el siguiente carácter después del lexema

        # Si es un numero
        if is_digit(char):
            start_col = col
            lexeme = ""
            while i < length and is_digit(source_code[i]):
                lexeme += source_code[i]
                i += 1
                col += 1
            # Manejo básico de números enteros. No incluye floats o notación científica.
            tokens.append(f"<tk_entero,{lexeme},{row},{start_col}>")
            continue

        # si es una cadena "string"
        if char in "\"'":
            start_col = col
            quote = char
            lexeme = quote # Incluir la comilla inicial en el lexema
            i += 1
            col += 1
            # Leer hasta encontrar la comilla de cierre o el final de línea/archivo (error de cadena no cerrada)
            # Manejo básico, no incluye secuencias de escape '\'
            while i < length and source_code[i] != quote and source_code[i] != '\n':
                lexeme += source_code[i]
                i += 1
                col += 1
            if i < length and source_code[i] == quote: # Encontramos la comilla de cierre
                lexeme += quote
                i += 1
                col += 1
                tokens.append(f"<tk_cadena,{lexeme},{row},{start_col}>")
                continue
            else:
                 # Cadena no cerrada o error de salto de línea dentro de cadena
                 print(f">>> Error léxico: Cadena no cerrada o salto de línea inesperado (linea:{row},posicion:{start_col})")
                 # Puedes decidir si detener el lexer o intentar recuperarte
                 # Por ahora, añadimos el token parcial y continuamos (esto podría causar más errores)
                 tokens.append(f"<tk_cadena_erronea,{lexeme},{row},{start_col}>")
                 # Si no consumimos el \n que causó el error, el loop principal lo hará.
                 continue # Continuar después del punto del error

        #si es un operador de dos simbolos
        # Ordenamos los operadores de 2 caracteres por longitud descendente para evitar coincidencias parciales (ej: '>' antes que '>=')
        # No es estrictamente necesario con la lógica actual, pero es buena práctica para lexers más complejos.
        two_char_op = source_code[i:i+2]
        if i + 1 < length and two_char_op in OPERATORS:
            tokens.append(f"<{OPERATORS[two_char_op]},{two_char_op},{row},{col}>")
            i += 2
            col += 2
            continue

        #Si es un operador de un solo simbolo
        if char in OPERATORS:
            tokens.append(f"<{OPERATORS[char]},{char},{row},{col}>")
            i += 1
            col += 1
            continue

        #si es un signo de puntuacion
        if char in PUNCTUATION:
            tokens.append(f"<{PUNCTUATION[char]},{char},{row},{col}>")
            i += 1
            col += 1
            continue

        # Si llegamos aquí, es un carácter no reconocido
        print(f">>> Error léxico(linea:{row},posicion:{col}): Carácter no reconocido '{char}'")
        # Podemos detenernos o saltar el carácter de error y continuar
        # Para este ejemplo, nos detenemos al encontrar el primer error léxico no manejado.
        break

    # --- Lógica para manejar DEDENT(s) y EOF al final del archivo ---
    # Al final del archivo, necesitamos cerrar cualquier bloque de indentación abierto
    while len(indent_stack) > 1: # Mientras haya niveles > 0 en el stack
        indent_stack.pop()
        # Los DEDENTs al final del archivo ocurren lógicamente después del último token,
        # en la "siguiente línea" virtual. Usamos la última fila y columna conocida.
        tokens.append(f"<DEDENT,,{row},{col}>")

    # Finalmente, añadir el token EOF (End Of File)
    # Usamos la última fila y columna conocida.
    tokens.append(f"<EOF,,{row},{col}>")


    # Guardar los tokens en un archivo de salida
    output_filename = filename.replace(".py", "_tokens.txt")
    try:
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for token in tokens:
                output_file.write(token + "\n")
        print(f"Tokens guardados en '{output_filename}'")
    except IOError as e:
        print(f"Error al escribir en el archivo '{output_filename}': {e}")
    return tokens