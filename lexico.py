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

    indent_stack = [0]
    at_line_start = True

    while i < length:
        char = source_code[i]

        if at_line_start:
            start_of_line_i = i
            start_of_line_col = col

            while i < length and source_code[i] in " \t":
                i += 1
                col += 1

            if i < length and source_code[i] == '#':
                while i < length and source_code[i] != '\n':
                    i += 1

            if i == length or source_code[i] == '\n':
                if i < length and source_code[i] == '\n':
                    i += 1
                    row += 1
                    col = 1
                continue

            current_indent_level = col - 1
            last_indent_level = indent_stack[-1]

            if current_indent_level > last_indent_level:
                tokens.append(f"<INDENT,,{row},{col}>")
                indent_stack.append(current_indent_level)
            elif current_indent_level < last_indent_level:
                while indent_stack[-1] > current_indent_level:
                    indent_stack.pop()
                    tokens.append(f"<DEDENT,,{row},{col}>")

                if current_indent_level != 0 and indent_stack[-1] != current_indent_level:
                     pass

            at_line_start = False

        char = source_code[i]

        if char in " \t":
            col += 1
            i += 1
            continue

        if char == "\n":
            row += 1
            col = 1
            i += 1
            at_line_start = True
            continue

        if char == "#":
             while i < length and source_code[i] != "\n":
                 i += 1
             continue

        if is_alpha(char):
            start_col = col
            lexeme = ""
            while i < length and is_alnum(source_code[i]):
                lexeme += source_code[i]
                i += 1
                col += 1
            if lexeme in KEYWORDS:
                tokens.append(f"<{lexeme},,{row},{start_col}>")
            else:
                tokens.append(f"<id,{lexeme},{row},{start_col}>")
            continue

        if is_digit(char):
            start_col = col
            lexeme = ""
            while i < length and is_digit(source_code[i]):
                lexeme += source_code[i]
                i += 1
                col += 1
            tokens.append(f"<tk_entero,{lexeme},{row},{start_col}>")
            continue

        if char in "\"'":
            start_col = col
            quote = char
            lexeme = quote
            i += 1
            col += 1
            while i < length and source_code[i] != quote and source_code[i] != '\n':
                lexeme += source_code[i]
                i += 1
                col += 1
            if i < length and source_code[i] == quote:
                lexeme += quote
                i += 1
                col += 1
                tokens.append(f"<tk_cadena,{lexeme},{row},{start_col}>")
                continue
            else:
                 print(f">>> Error léxico: Cadena no cerrada o salto de línea inesperado (linea:{row},posicion:{start_col})")
                 tokens.append(f"<tk_cadena_erronea,{lexeme},{row},{start_col}>")
                 continue

        two_char_op = source_code[i:i+2]
        if i + 1 < length and two_char_op in OPERATORS:
            tokens.append(f"<{OPERATORS[two_char_op]},{two_char_op},{row},{col}>")
            i += 2
            col += 2
            continue

        if char in OPERATORS:
            tokens.append(f"<{OPERATORS[char]},{char},{row},{col}>")
            i += 1
            col += 1
            continue

        if char in PUNCTUATION:
            tokens.append(f"<{PUNCTUATION[char]},{char},{row},{col}>")
            i += 1
            col += 1
            continue

        print(f">>> Error léxico(linea:{row},posicion:{col}): Carácter no reconocido '{char}'")
        break

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(f"<DEDENT,,{row},{col}>")

    tokens.append(f"<EOF,,{row},{col}>")

    output_filename = filename.replace(".py", "_tokens.txt")
    try:
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for token in tokens:
                output_file.write(token + "\n")
        print(f"Tokens guardados en '{output_filename}'")
    except IOError as e:
        print(f"Error al escribir en el archivo '{output_filename}': {e}")
    return tokens