
import lexico

class ManualRecursiveParser:
    """
    Analizador Sintáctico Descendente Recursivo manual.
    Consume tokens generados por el lexer proporcionado.
    """
    def __init__(self, tokens_list):
        self.tokens = tokens_list
        self.current_token_index = 0
        self.error_info = None
        self.analysis_aborted = False

    def _parse_token_string(self, token_string):
        """ Parsea un string de token y devuelve una lista [TIPO, LEXEMA, FILA, COL] """
        if not token_string or not token_string.startswith('<') or not token_string.endswith('>'):
             if token_string and token_string.startswith('<EOF'):
                  return ['EOF', '', 0, 0]
             print(f"Parser Error: Formato de token inválido: {token_string}")
             return None

        content = token_string[1:-1]
        try:
            last_comma_pos = content.rindex(',')
            col_str = content[last_comma_pos + 1:]

            second_last_comma_pos = content.rindex(',', 0, last_comma_pos)
            row_str = content[second_last_comma_pos + 1 : last_comma_pos]

            type_lexeme_part = content[:second_last_comma_pos]

            first_comma_pos = type_lexeme_part.find(',')
            if first_comma_pos == -1:
                 token_type = type_lexeme_part
                 lexeme = ""
            else:
                token_type = type_lexeme_part[:first_comma_pos]
                lexeme = type_lexeme_part[first_comma_pos + 1:]

            row = int(row_str)
            col = int(col_str)

            return [token_type, lexeme, row, col]

        except ValueError:
            print(f"Parser Error: No se pudieron parsear componentes numéricos del token: {token_string}")
            return None
        except IndexError:
             print(f"Parser Error: Problema de índice parseando token (menos de 2 comas?): {token_string}")
             return None
        except Exception as e:
             print(f"Parser Error: Error inesperado parseando token '{token_string}': {e}")
             return None


    def _peek(self):
        """ Devuelve el token actual parseado [TIPO, LEXEMA, FILA, COL] sin consumirlo. Maneja fin de archivo y errores de formato. """
        if self.analysis_aborted:
            return ['EOF', '', 0, 0]

        if self.current_token_index >= len(self.tokens):
            last_pos = [1, 1] if not self.tokens else self._get_location_from_last_token()
            return ['EOF', '', last_pos[0], last_pos[1]]

        token_str = self.tokens[self.current_token_index]
        parsed_token = self._parse_token_string(token_str)

        if parsed_token is None or (parsed_token is not None and parsed_token[0] == 'TOKEN_FORMAT_ERROR'):
            error_token = parsed_token if parsed_token is not None else ['TOKEN_FORMAT_ERROR', token_str, 0, 0]
            return error_token


        return parsed_token

    def _consume(self):
        """ Consume el token actual y devuelve el token parseado """
        if self.analysis_aborted:
             return ['EOF', '', 0, 0]

        token = self._peek()
        if token[0] == 'TOKEN_FORMAT_ERROR':
             self._handle_token_format_error(token)
             return ['EOF', '', 0, 0]


        if token[0] != 'EOF':
            self.current_token_index += 1
        return token

    def _get_location_from_last_token(self):
         if not self.tokens:
              return [1, 1]
         try:
              # Buscar el último token que no sea INDENT/DEDENT/EOF para una mejor estimación
              for i in range(len(self.tokens) - 1, -1, -1):
                   token_str = self.tokens[i]
                   parsed = self._parse_token_string(token_str)
                   if parsed and parsed[0] not in ('INDENT', 'DEDENT', 'EOF', 'TOKEN_FORMAT_ERROR'):
                        return [parsed[2], parsed[3] + (len(parsed[1]) if parsed[1] else 1)]
                   elif parsed and parsed[0] == 'EOF':
                        return [parsed[2], parsed[3]] 
              # Si solo hay INDENT/DEDENT/EOF o tokens inválidos
              return [1, 1]
         except Exception:
              return [1, 1]

    # Método para manejar errores de formato de token, lanza excepción
    def _handle_token_format_error(self, error_token_parsed):
        if not self.analysis_aborted:
             self.analysis_aborted = True
             line, col = error_token_parsed[2], error_token_parsed[3]
             original_string = error_token_parsed[1]
             self.error_info = f"<{line},{col}> Error lexico: formato de token invalido '{original_string}'."
             print(self.error_info)
        raise SyntaxError("Error de formato de token detectado")


    def _error(self, found_token_parsed, expected_description):
        """
        Registra el primer error sintáctico (tipo de token inesperado) y aborta.
        Recibe el token *encontrado* como argumento.
        """
        if not self.analysis_aborted:
            self.analysis_aborted = True
            line = found_token_parsed[2]
            col = found_token_parsed[3]
            found_type = found_token_parsed[0]
            found_lexeme = found_token_parsed[1]

            found_representation = found_lexeme if found_lexeme else found_type
            if found_type == 'TOKEN_FORMAT_ERROR':
                 found_representation = f"Token mal formado: '{found_lexeme}'"

            self.error_info = f"<{line},{col}> Error sintactico: se encontro: \"{found_representation}\"; se esperaba: \"{expected_description}\"."
            print(self.error_info)

        raise SyntaxError("Error de sintaxis detectado por el parser")


    def _match(self, expected_type):
        current_token = self._peek()
        current_type = current_token[0]

        # Verificar si peek encontró un error de formato
        if current_type == 'TOKEN_FORMAT_ERROR':
             self._handle_token_format_error(current_token)
             return ['EOF', '', 0, 0]

        if self.analysis_aborted:
            return ['EOF', '', 0, 0]

        if current_type == expected_type:
            return self._consume()
        else:
            self._error(current_token, f"'{expected_type}'")
            return None


    # --- Punto de Entrada del Parser ---
    def parse(self):
        """ Inicia el proceso de análisis sintáctico. """
        self.current_token_index = 0
        self.error_info = None
        self.analysis_aborted = False

        try:
            self._program()
            if not self.analysis_aborted:
                 final_token = self._peek()
                 if final_token[0] != 'EOF':
                      self._error(final_token, "Fin de archivo (EOF)")
                 else:
                      return "El analisis sintactico ha finalizado exitosamente."

        except SyntaxError:
            pass

        except Exception as e:
             if not self.analysis_aborted:
                  current_token = self._peek()
                  line, col = current_token[2], current_token[3]
                  self.error_info = f"<{line},{col}> Error interno inesperado del parser: {e}"
                  print(self.error_info)

        return self.error_info if self.error_info else "Error desconocido durante el analisis."


    # --- Métodos para las Reglas Gramaticales ---

    def _program(self):
        # program ::= statement* EOF
        while self._peek()[0] != 'EOF' and not self.analysis_aborted:
             self._statement()
        self._match('EOF')

    def _statement(self):
        # statement ::= assignment_stmt | if_stmt | while_stmt | def_stmt | return_stmt | print_stmt | pass_stmt | for_stmt
        if self.analysis_aborted: return

        token_type = self._peek()[0]

        if token_type == 'id':
             self._assignment_stmt()
        elif token_type == 'if':
             self._if_stmt()
        elif token_type == 'while':
             self._while_stmt()
        elif token_type == 'def':
             self._def_stmt()
        elif token_type == 'return':
             self._return_stmt()
        elif token_type == 'print':
             self._print_stmt()
        elif token_type == 'pass':
             self._pass_stmt()
        elif token_type == 'for':
             self._for_stmt()
        else:
             self._error(self._peek(), "Inicio de declaracion (id, if, while, def, return, print, pass, for, ...)")

    def _assignment_stmt(self):
        # assignment_stmt ::= IDENTIFIER '=' expression
        if self.analysis_aborted: return
        self._match('id')
        self._match('tk_asign')
        self._expression()

    def _if_stmt(self):
        # if_stmt ::= 'if' comparison ':' suite ('elif' comparison ':' suite)* ('else' ':' suite)?
        if self.analysis_aborted: return
        self._match('if')
        self._comparison()
        self._match('tk_dos_puntos')
        self._suite()

        while self._peek()[0] == 'elif' and not self.analysis_aborted:
            self._consume()
            self._comparison()
            self._match('tk_dos_puntos')
            self._suite()

        if self._peek()[0] == 'else' and not self.analysis_aborted:
            self._consume()
            self._match('tk_dos_puntos')
            self._suite()

    def _while_stmt(self):
        # while_stmt ::= 'while' comparison ':' suite
        if self.analysis_aborted: return
        self._match('while')
        self._comparison()
        self._match('tk_dos_puntos')
        self._suite()

    def _return_stmt(self):
        # return_stmt ::= 'return' expression?
        if self.analysis_aborted: return
        self._match('return')

        next_token_type = self._peek()[0]
        # Considerar NEWLINE si tu lexer lo emite antes de DEDENT o EOF para sentencias simples
        terminators = ('DEDENT', 'EOF')
        if next_token_type not in terminators:
            self._expression()

    def _def_stmt(self):
        # def_stmt ::= 'def' IDENTIFIER '(' ')' ':' suite
        if self.analysis_aborted: return
        self._match('def')
        self._match('id')
        self._match('tk_par_izq')
        self._match('tk_par_der')
        self._match('tk_dos_puntos')
        self._suite()

    def _print_stmt(self):
         # print_stmt ::= 'print' '(' expression ')'
         if self.analysis_aborted: return
         self._match('print')
         self._match('tk_par_izq')
         self._expression()
         self._match('tk_par_der')

    def _pass_stmt(self):
         # pass_stmt ::= 'pass'
         if self.analysis_aborted: return
         self._match('pass')

    def _for_stmt(self):
        # for_stmt ::= 'for' IDENTIFIER 'in' 'range' '(' expression ')' ':' suite
        if self.analysis_aborted: return
        self._match('for')
        self._match('id')
        self._match('in')
        self._match('range')
        self._match('tk_par_izq')
        self._expression()
        self._match('tk_par_der')
        self._match('tk_dos_puntos')
        self._suite() 


    def _suite(self):
        """ Parsea un bloque indentado: INDENT statement+ DEDENT """
        if self.analysis_aborted: return
        self._match('INDENT')

        while self._peek()[0] != 'DEDENT' and self._peek()[0] != 'EOF' and not self.analysis_aborted:
             self._statement()

        if self._peek()[0] == 'DEDENT':
             self._match('DEDENT')
        elif not self.analysis_aborted:
             self._match('DEDENT') 


    # --- Funciones para expresiones ---
    def _expression(self):
        # expression ::= term (('+' | '-') term)*
        if self.analysis_aborted: return
        self._term()
        while self._peek()[0] in ('tk_suma', 'tk_resta') and not self.analysis_aborted:
            self._consume()
            self._term()

    def _term(self):
         # term ::= factor (('*' | '/') factor)*
         if self.analysis_aborted: return
         self._factor()
         while self._peek()[0] in ('tk_mult', 'tk_div') and not self.analysis_aborted:
              self._consume()
              self._factor()

    def _factor(self):
        # factor ::= IDENTIFIER | INTEGER | STRING | '(' expression ')'
        if self.analysis_aborted: return
        token = self._peek()
        token_type = token[0]
        if token_type == 'id':
            self._consume()
        elif token_type == 'tk_entero':
            self._consume()
        elif token_type == 'tk_cadena':
            self._consume()
        elif token_type == 'tk_par_izq':
            self._consume()
            self._expression()
            self._match('tk_par_der')
        else:
            self._error(token, "Identificador, numero entero, cadena o '('")

    def _comparison(self):
        # comparison ::= expression ('>' | '<' | '==' | '!=' | '>=' | '<=') expression
        if self.analysis_aborted: return
        self._expression()
        op_type = self._peek()[0]
        comp_ops = ('tk_mayor', 'tk_menor', 'tk_igual', 'tk_dif',
                    'tk_mayor_igual', 'tk_menor_igual')
        if op_type in comp_ops:
            self._consume()
            self._expression()


# --- Bloque Principal de Ejecución ---

def main_analisis_sintactico(archivo_entrada_py, archivo_salida_txt):
    """ Función principal que orquesta el lexer y el parser. """

    print(f"Ejecutando análisis léxico para: {archivo_entrada_py}")
    lista_tokens = lexico.lexer(archivo_entrada_py)

    if lista_tokens and not lista_tokens[-1].startswith('<EOF'):
         print("Advertencia: El lexer no generó un token EOF explícito. Añadiendo uno.")
         last_line, last_col = 0, 0
         try:
              if lista_tokens:
                  temp_parser = ManualRecursiveParser([])
                  last_line, last_col = temp_parser._get_location_from_last_token()
         except Exception as e:
             print(f"Advertencia: No se pudo determinar la posición del último token para EOF: {e}")
             try:
                 with open(archivo_entrada_py, 'r', encoding='utf-8') as f:
                      last_line = len(f.readlines())
                 last_col = 1
             except Exception:
                  last_line, last_col = 1, 1 


         lista_tokens.append(f"<EOF,,{last_line},{last_col}>")
    elif not lista_tokens:
         print("Análisis léxico no generó tokens.")
         try:
              with open(archivo_entrada_py, 'r', encoding='utf-8') as f:
                   content = f.read()
              if len(content) > 0:
                   print("Asumiendo fallo léxico. Abortando análisis sintáctico.")
                   resultado_analisis = "Error durante el analisis lexico."
                   try:
                      with open(archivo_salida_txt, 'w', encoding='utf-8') as f_out:
                           f_out.write(resultado_analisis)
                   except IOError as e:
                       print(f"Error al escribir error léxico en archivo de salida: {e}")
                   return
              else:
                   lista_tokens = ["<EOF,,1,1>"]
                   print("Archivo vacío. Procediendo con EOF.")
         except FileNotFoundError:
             print(f"Error: Archivo de entrada '{archivo_entrada_py}' no encontrado.")
             resultado_analisis = f"Error: Archivo de entrada '{archivo_entrada_py}' no encontrado."
             try:
                 with open(archivo_salida_txt, 'w', encoding='utf-8') as f_out:
                      f_out.write(resultado_analisis)
             except IOError as e:
                  print(f"Error al escribir error léxico en archivo de salida: {e}")
             return
         except Exception as e:
             print(f"Error inesperado al leer archivo para verificar si está vacío: {e}")
             resultado_analisis = f"Error interno: {e}"
             try:
                 with open(archivo_salida_txt, 'w', encoding='utf-8') as f_out:
                      f_out.write(resultado_analisis)
             except IOError as e_io:
                  print(f"Error al escribir error interno en archivo de salida: {e_io}")
             return


    print(f"Análisis léxico completado ({len(lista_tokens)} tokens generados). Iniciando análisis sintáctico...")

    parser = ManualRecursiveParser(lista_tokens)

    resultado_analisis = parser.parse() 

    print(f"Resultado del análisis sintáctico: {resultado_analisis}")
    try:
        with open(archivo_salida_txt, "w", encoding="utf-8") as f_out:
            f_out.write(resultado_analisis)
        print(f"Resultado del análisis guardado en '{archivo_salida_txt}'")
    except IOError as e:
        print(f"Error: No se pudo escribir en el archivo de salida '{archivo_salida_txt}'. {e}")


if __name__ == "__main__":
     archivo_entrada = "ejemplo.py"
     archivo_salida = "salida.txt"

     existe = False
     try:
          with open(archivo_entrada, 'r'):
               existe = True
     except FileNotFoundError:
          print(f"Error: El archivo de entrada '{archivo_entrada}' no fue encontrado.")
     except Exception as e:
          print(f"Error al intentar abrir '{archivo_entrada}': {e}")


     if existe:
          try:
              lexico.KEYWORDS
              lexico.OPERATORS
              lexico.PUNCTUATION
          except AttributeError:
              print("Error: El módulo 'lexico' debe definir KEYWORDS, OPERATORS y PUNCTUATION.")
              exit()

          main_analisis_sintactico(archivo_entrada, archivo_salida)