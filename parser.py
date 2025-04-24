import lexico
from collections import defaultdict

gramatica = {
    'program': [
        ['statement', 'program'],
        ['EOF']
    ],
    'statement': [
        ['id', 'statement_after_id'],
        ['if_statement'],
        ['while', 'comparison', 'tk_dos_puntos', 'suite'],
        ['def', 'id', 'tk_par_izq', 'param_list', 'tk_par_der', 'tk_dos_puntos', 'suite'],
        ['return', 'expression'],
        ['print', 'tk_par_izq', 'expression', 'tk_par_der'],
        ['pass'],
        ['for', 'id', 'in', 'range', 'tk_par_izq', 'argument_list', 'tk_par_der', 'tk_dos_puntos', 'suite']
    ],
    'statement_after_id': [
        ['asig'],
        ['llamada']
    ],
    'if_statement': [
        ['if', 'comparison', 'tk_dos_puntos', 'suite', 'else_part']
    ],
    'else_part': [
        ['elif', 'comparison', 'tk_dos_puntos', 'suite', 'else_part'],
        ['else', 'tk_dos_puntos', 'suite'],
        []
    ],
    'asig': [
        ['tk_asign', 'expression'],
        ['tk_suma_asig', 'expression'],
        ['tk_resta_asig', 'expression'],
        ['tk_mult_asig', 'expression'],
        ['tk_div_asig', 'expression'],
        ['tk_div_ent_asig', 'expression'],
        ['tk_mod_asig', 'expression'],
        ['tk_pot_asig', 'expression'],
        ['tk_and_bin_asig', 'expression'],
        ['tk_or_bin_asig', 'expression'],
        ['tk_xor_bin_asig', 'expression'],
        ['tk_despl_izq_asig', 'expression'],
        ['tk_despl_der_asig', 'expression']
    ],
    'param_list': [
        ['id', 'param_list_cont'],
        []
    ],
    'param_list_cont': [
        ['tk_coma', 'id', 'param_list_cont'],
        []
    ],
    'argument_list': [
        ['expression', 'argument_list_cont'],
        []
    ],
    'argument_list_cont': [
        ['tk_coma', 'expression', 'argument_list_cont'],
        []
    ],
    'suite': [
        ['INDENT', 'statement', 'suite_cont']
    ],
    'suite_cont': [
        ['statement', 'suite_cont'],
        ['DEDENT']
    ],
    'expression': [
        ['term', "expression'"]
    ],
    "expression'": [
        ['tk_suma', 'term', "expression'"],
        ['tk_resta', 'term', "expression'"],
        []
    ],
    'term': [
        ['factor', "term'"]
    ],
    "term'": [
        ['tk_mult', 'factor', "term'"],
        ['tk_div', 'factor', "term'"],
        []
    ],
    'factor': [
        ['tk_resta', 'factor'],
        ['id', 'llamada'],
        ['tk_entero'],
        ['tk_cadena'],
        ['tk_par_izq', 'expression', 'tk_par_der'],
        ['list_literal']
    ],
    'llamada': [
        ['tk_par_izq', 'argument_list', 'tk_par_der'],
        ['tk_punto', 'func_call'],
        []
    ],
    'func_call': [
        ['id', 'llamada'],
        ['tk_par_izq', 'argument_list', 'tk_par_der', 'llamada']
    ],
    'comparison': [
        ['expression', 'op_comparacion', 'expression']
    ],
    'op_comparacion': [
        ['tk_mayor'],
        ['tk_menor'],
        ['tk_igual'],
        ['tk_dif'],
        ['tk_mayor_igual'],
        ['tk_menor_igual']
    ],
    'list_literal': [
        ['tk_cor_izq', 'optional_expression_list', 'tk_cor_der']
    ],
    'optional_expression_list': [
        ['expression_list'],
        []
    ],
    'expression_list': [
        ['expression', 'expression_list_cont']
    ],
    'expression_list_cont': [
        ['tk_coma', 'expression', 'expression_list_cont'],
        []
    ]
}

class ASDR:
    def __init__(self, gramatica, simbolo_inicial, tokens_types, tokens_info):
        self.gramatica = gramatica
        self.inicial = simbolo_inicial
        self.primeros = defaultdict(set)
        self.siguientes = defaultdict(set)
        self.predicciones = defaultdict(list)
        self._calcular_primeros()
        self._calcular_siguientes()
        self._calcular_predicciones()
        self.tokens = tokens_types
        self.token_info = tokens_info
        self.pos = 0
        for nt in self.gramatica:
            setattr(self, nt, self._crear_funcion(nt))

    def token_actual_type(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'

    def token_actual_info(self):
        return self.token_info[self.pos] if self.pos < len(self.token_info) else ('', 0, 0)

    def parse(self):
        try:
            getattr(self, self.inicial)()
            if self.token_actual_type() == 'EOF':
                pass
            else:
                value, row, col = self.token_actual_info()
                found_str = f"“{self.token_actual_type()}”"
                if value:
                     found_str = f"“{self.token_actual_type()} ({value})”"
                raise SyntaxError(f"<{row},{col}> Error sintactico: Sobran símbolos tras el análisis. Se encontró: {found_str}.")
        except SyntaxError as e:
            raise e
        except Exception as e:
            value, row, col = self.token_actual_info()
            raise SyntaxError(f"<{row},{col}> Error interno del parser: {e}")

    def coincidir(self, terminal):
        actual_type = self.token_actual_type()
        value, row, col = self.token_actual_info()
        if actual_type == terminal:
            self.pos += 1
        else:
            expected_str = f"“{terminal}”"
            found_str = f"“{actual_type}”"
            if value:
                 found_str = f"“{actual_type} ({value})”"
            raise SyntaxError(f"<{row},{col}> Error sintactico: Se esperaba: {expected_str}; se encontró: {found_str}.")

    def es_terminal(self, simbolo):
        return simbolo not in self.gramatica and simbolo != '[]'

    def _calcular_primeros(self):
        cambiado = True
        while cambiado:
            cambiado = False
            for nt, producciones in self.gramatica.items():
                for prod in producciones:
                    if prod == []:
                        if 'ε' not in self.primeros[nt]:
                            self.primeros[nt].add('ε')
                            cambiado = True
                        continue
                    i = 0
                    bloque_deriva_epsilon = True
                    while i < len(prod) and bloque_deriva_epsilon:
                        simbolo = prod[i]
                        bloque_deriva_epsilon = False
                        if self.es_terminal(simbolo):
                            if simbolo not in self.primeros[nt]:
                                self.primeros[nt].add(simbolo)
                                cambiado = True
                            break
                        else:
                            antes = len(self.primeros[nt])
                            self.primeros[nt].update(self.primeros[simbolo] - {'ε'})
                            if len(self.primeros[nt]) > antes:
                                cambiado = True
                            if 'ε' in self.primeros[simbolo]:
                                bloque_deriva_epsilon = True
                                i += 1
                            else:
                                break
                    if i == len(prod) and bloque_deriva_epsilon:
                        if 'ε' not in self.primeros[nt]:
                            self.primeros[nt].add('ε')
                            cambiado = True

    def _calcular_siguientes(self):
        cambiado = True
        self.siguientes[self.inicial].add('EOF')
        while cambiado:
            cambiado = False
            for nt, producciones in self.gramatica.items():
                for prod in producciones:
                    len_prod = len(prod)
                    for i, simbolo_actual in enumerate(prod):
                        if simbolo_actual in self.gramatica:
                            siguientes_en_prod = set()
                            j = i + 1
                            puede_derivar_epsilon_cola = True
                            while j < len_prod and puede_derivar_epsilon_cola:
                                siguiente_simbolo = prod[j]
                                puede_derivar_epsilon_cola = False
                                if self.es_terminal(siguiente_simbolo):
                                    if siguiente_simbolo not in siguientes_en_prod:
                                        siguientes_en_prod.add(siguiente_simbolo)
                                    break
                                else:
                                    antes = len(siguientes_en_prod)
                                    siguientes_en_prod.update(self.primeros[siguiente_simbolo] - {'ε'})
                                    if len(siguientes_en_prod) > antes:
                                         pass
                                    if 'ε' in self.primeros[siguiente_simbolo]:
                                        puede_derivar_epsilon_cola = True
                                        j += 1
                                    else:
                                        break
                            antes = len(self.siguientes[simbolo_actual])
                            self.siguientes[simbolo_actual].update(siguientes_en_prod)
                            if len(self.siguientes[simbolo_actual]) > antes:
                                cambiado = True
                            if j == len_prod and puede_derivar_epsilon_cola:
                                antes = len(self.siguientes[simbolo_actual])
                                self.siguientes[simbolo_actual].update(self.siguientes[nt])
                                if len(self.siguientes[simbolo_actual]) > antes:
                                    cambiado = True

    def _calcular_predicciones(self):
        for nt, producciones in self.gramatica.items():
            for prod in producciones:
                pred = set()
                if prod == []:
                    pred.update(self.siguientes[nt])
                else:
                    i = 0
                    deriva_epsilon_prefijo = True
                    while i < len(prod) and deriva_epsilon_prefijo:
                        simbolo = prod[i]
                        deriva_epsilon_prefijo = False
                        if self.es_terminal(simbolo):
                            if simbolo not in pred:
                                pred.add(simbolo)
                            break
                        else:
                            pred.update(self.primeros[simbolo] - {'ε'})
                            if 'ε' in self.primeros[simbolo]:
                                deriva_epsilon_prefijo = True
                                i += 1
                            else:
                                break
                    if i == len(prod) and deriva_epsilon_prefijo:
                        pred.update(self.siguientes[nt])
                self.predicciones[nt].append((prod, pred))

    def _crear_funcion(self, nt):
        def funcion():
            actual_type = self.token_actual_type()
            value, row, col = self.token_actual_info()
            opcion_encontrada = False
            expected_tokens = set()
            for produccion, pred in self.predicciones[nt]:
                expected_tokens.update(pred)
                if actual_type in pred:
                    opcion_encontrada = True
                    try:
                        for s in produccion:
                            if s == '[]':
                                pass
                            elif self.es_terminal(s):
                                self.coincidir(s)
                            else:
                                getattr(self, s)()
                        return
                    except SyntaxError as e:
                         raise e
                    except Exception as e:
                         raise SyntaxError(f"<{row},{col}> Error interno procesando producción {nt} → {' '.join(produccion) if produccion else 'ε'}: {e}")
            if not opcion_encontrada:
                 found_str = f"“{actual_type}”"
                 if value:
                      found_str = f"“{actual_type} ({value})”"
                 expected_str_list = [f"“{t}”" for t in sorted(list(expected_tokens))]
                 expected_str = ", ".join(expected_str_list)
                 raise SyntaxError(f"<{row},{col}> Error sintactico: Se encontró: {found_str}; se esperaba uno de: {expected_str}.")
        funcion.__name__ = f"parse_{nt}"
        return funcion

    def mostrar_conjuntos(self):
        print("PRIMEROS:")
        for nt, s in sorted(self.primeros.items()):
            print(f"  {nt}: {sorted(list(s))}")
        print("\nSIGUIENTES:")
        for nt, s in sorted(self.siguientes.items()):
            print(f"  {nt}: {sorted(list(s))}")
        print("\nPREDICCIONES:")
        for nt, lista in sorted(self.predicciones.items()):
            for produccion, pred in lista:
                print(f"  {nt} → {' '.join(produccion) if produccion else 'ε'}: {sorted(list(pred))}")

def main_analisis_sintactico(archivo_entrada_py, archivo_salida_txt):
    try:
        lista_tokens_crudos = lexico.lexer(archivo_entrada_py)
    except FileNotFoundError:
         print(f"Error: No se encontró el archivo de entrada '{archivo_entrada_py}'.")
         with open(archivo_salida_txt, "w", encoding="utf-8") as f:
             f.write(f"Error: Archivo '{archivo_entrada_py}' no encontrado.")
         return
    except AttributeError:
         print(f"Error: El módulo 'lexico' no tiene una función 'lexer'.")
         with open(archivo_salida_txt, "w", encoding="utf-8") as f:
             f.write("Error: Función lexer no encontrada en el módulo lexico.")
         return
    except Exception as e:
         print(f"Error inesperado durante el análisis léxico: {e}")
         with open(archivo_salida_txt, "w", encoding="utf-8") as f:
             f.write(f"Error durante el análisis léxico: {e}")
         return

    if not lista_tokens_crudos:
        print("Error: El análisis léxico no produjo tokens o el archivo está vacío.")
        with open(archivo_salida_txt, "w", encoding="utf-8") as f:
            f.write("Error: Análisis léxico fallido o archivo vacío.")
        return

    tokens_parser_types = []
    tokens_parser_info = []

    for t in lista_tokens_crudos:
        if isinstance(t, str) and t.startswith('<') and t.endswith('>'):
            try:
                inner_content = t[1:-1]
                last_comma_index = inner_content.rfind(',')
                second_last_comma_index = inner_content.rfind(',', 0, last_comma_index)

                if last_comma_index != -1 and second_last_comma_index != -1:
                    row_str = inner_content[second_last_comma_index + 1 : last_comma_index].strip()
                    col_str = inner_content[last_comma_index + 1 :].strip()
                    type_and_value_str = inner_content[:second_last_comma_index]
                    first_comma_index_in_type_value = type_and_value_str.find(',')

                    if first_comma_index_in_type_value != -1:
                        actual_type = type_and_value_str[:first_comma_index_in_type_value].strip()
                        actual_value_str = type_and_value_str[first_comma_index_in_type_value + 1 :].strip()
                    else:
                        actual_type = type_and_value_str.strip().rstrip(',')
                        actual_value_str = ""

                    row = int(row_str) if row_str.isdigit() else 0
                    col = int(col_str) if col_str.isdigit() else 0

                    if actual_value_str.startswith('"') and actual_value_str.endswith('"'):
                        actual_value = actual_value_str[1:-1]
                    elif actual_value_str.startswith("'") and actual_value_str.endswith("'"):
                        actual_value = actual_value_str[1:-1]
                    else:
                         actual_value = actual_value_str

                    tokens_parser_types.append(actual_type)
                    tokens_parser_info.append((actual_value, row, col))

                else:
                    processed_type = inner_content.split(',')[0].strip() if inner_content else t.strip()
                    tokens_parser_types.append(processed_type or 'UNKNOWN_TOKEN')
                    tokens_parser_info.append(('', 0, 0))
                    print(f"    -> Type: '{processed_type or 'UNKNOWN_TOKEN'}', Pos: <0,0> (dummy)")

            except Exception as e:
                 processed_type = t[1:-1].split(',')[0].strip() if isinstance(t, str) and t.startswith('<') and t.endswith('>') and t[1:-1].find(',') != -1 else str(t).strip()
                 tokens_parser_types.append(processed_type or 'PROCESSING_ERROR_TOKEN')
                 tokens_parser_info.append(('', 0, 0))
                 print(f"    -> Type: '{processed_type or 'PROCESSING_ERROR_TOKEN'}', Pos: <0,0> (error)")

        elif isinstance(t, str) and t.strip():
             tokens_parser_types.append(t.strip())
             tokens_parser_info.append(('', 0, 0))
             print(f"    -> Type: '{t.strip()}', Pos: <0,0> (dummy)")
        else:
             if t:
                print(f"  Advertencia: Ignorando item no válido o vacío de la salida del lexer: {t}")

    if not tokens_parser_types or tokens_parser_types[-1] != 'EOF':
         tokens_parser_types.append('EOF')
         last_row, last_col = (tokens_parser_info[-1][1], tokens_parser_info[-1][2] + 1) if tokens_parser_info else (0, 0)
         tokens_parser_info.append(('', last_row, last_col))
         print(f"    -> Type: 'EOF', Pos: <{last_row},{last_col}> (manual)")

    try:       
        parser = ASDR(gramatica, simbolo_inicial='program', tokens_types=tokens_parser_types, tokens_info=tokens_parser_info)
        resultado = ""
        try:
             parser.parse()
             if parser.token_actual_type() == 'EOF':
                 print("\n✔ Cadena aceptada: Análisis realizado exitosamente.")
                 resultado = "✔ Cadena aceptada: Análisis realizado exitosamente. Consulta la salida de la consola para el rastreo."
             else:
                 value, row, col = parser.token_actual_info()
                 err_msg = f"<{row},{col}> Error sintactico: Análisis completado antes de consumir todos los símbolos restantes. Se encontró: “{parser.token_actual_type()}”.";
                 print(f"\n❌ {err_msg}")
                 resultado = f"❌ {err_msg}"

        except SyntaxError as e:
             print(f"\n❌ {e}")
             resultado = f"❌ Error sintáctico: {e}"
        except Exception as e:
             value, row, col = parser.token_actual_info()
             err_msg = f"Ocurrió un error inesperado durante el análisis en <{row},{col}>: {e}"
             print(f"\n❌ {err_msg}")
             resultado = f"❌ {err_msg}"

    except Exception as e:
         err_msg = f"Error durante la inicialización del parser: {e}"
         print(f"\n❌ {err_msg}")
         resultado = f"❌ {err_msg}"

    try:
        with open(archivo_salida_txt, "w", encoding="utf-8") as f:
            f.write(resultado)
        print(f"\nResultado del análisis guardado en '{archivo_salida_txt}'")
    except IOError as e:
        print(f"Error al escribir en el archivo de salida '{archivo_salida_txt}': {e}")

if __name__ == "__main__":
    archivo_entrada = "ejemplo.py"
    archivo_salida = "salida_sintactico.txt"
    main_analisis_sintactico(archivo_entrada, archivo_salida)