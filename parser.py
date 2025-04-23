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
    def __init__(self, gramatica, simbolo_inicial):
        self.gramatica = gramatica
        self.inicial = simbolo_inicial
        self.primeros = defaultdict(set)
        self.siguientes = defaultdict(set)
        self.predicciones = defaultdict(list)

        self._calcular_primeros()
        self._calcular_siguientes()
        self._calcular_predicciones()

        self.tokens = []
        self.pos = 0
        for nt in self.gramatica:
            setattr(self, nt, self._crear_funcion(nt))

    def token_actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'

    def parse(self, tokens):
        self.tokens = tokens + ['EOF']
        self.pos = 0
        print("Tokens de entrada:", self.tokens)
        try:
            getattr(self, self.inicial)()
            if self.token_actual() == 'EOF':
                print("✔ Cadena aceptada")
            else:
                raise SyntaxError(f"❌ Sobran símbolos '{self.tokens[self.pos:]}' tras el análisis en la posición {self.pos}")
        except SyntaxError as e:
            print("Error de sintaxis:", e)
        except Exception as e:
            print(f"Ocurrió un error inesperado durante el análisis: {e}")

    def coincidir(self, terminal):
        actual = self.token_actual()
        if actual == terminal:
            print(f"✓ {terminal}")
            self.pos += 1
        else:
            raise SyntaxError(f"Error de coincidencia: Se esperaba '{terminal}', se encontró '{actual}' en la posición {self.pos}")

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
            token = self.token_actual()

            opcion_encontrada = False
            for produccion, pred in self.predicciones[nt]:
                if token in pred:
                    opcion_encontrada = True
                    print(f"{nt} → {' '.join(produccion) if produccion else 'ε'}")

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

            if not opcion_encontrada:
                 raise SyntaxError(f"Error de sintaxis en {nt}: token actual '{token}' no válido en la posición {self.pos}. Predicciones esperadas: {[list(pred) for _, pred in self.predicciones[nt]]}")

        funcion.__name__ = f"parse_{nt}"
        return funcion

    def mostrar_conjuntos(self):
        print("PRIMEROS:")
        for nt, s in self.primeros.items():
            print(f"  {nt}: {s}")
        print("\nSIGUIENTES:")
        for nt, s in self.siguientes.items():
            print(f"  {nt}: {s}")
        print("\nPREDICCIONES:")
        for nt, lista in self.predicciones.items():
            for produccion, pred in lista:
                print(f"  {nt} → {' '.join(produccion)}: {pred}")

def main_analisis_sintactico(archivo_entrada_py, archivo_salida_txt):
    print(f"Ejecutando análisis léxico para: {archivo_entrada_py}")

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
        print("Error: El análisis léxico no produjo tokens.")
        with open(archivo_salida_txt, "w", encoding="utf-8") as f:
            f.write("Error: Análisis léxico fallido o archivo vacío.")
        return

    tokens_parser = []
    for t in lista_tokens_crudos:
        if isinstance(t, str) and t.startswith('<') and ',' in t:
            try:
                tipo = t[1:].split(',')[0]
                tokens_parser.append(tipo)
            except IndexError:
                 print(f"Advertencia: Token crudo con formato inesperado '{t}'. Ignorando.")
        elif isinstance(t, str):
             tokens_parser.append(t)

    if not tokens_parser:
         print("Error: No se pudieron extraer tipos de tokens válidos del resultado del lexer.")
         with open(archivo_salida_txt, "w", encoding="utf-8") as f:
             f.write("Error: No se pudieron preparar tokens para el parser.")
         return

    try:
        print("\n--- Inicializando Parser ASDR ---")
        parser = ASDR(gramatica, simbolo_inicial='program')

        print("\n--- CONJUNTOS CALCULADOS ---")
        parser.mostrar_conjuntos()

        print("\n--- INICIANDO ANÁLISIS SINTÁCTICO ---")
        resultado = ""
        try:
             parser.parse(tokens_parser)
             resultado = "El análisis sintáctico ha finalizado exitosamente."
        except SyntaxError as e:
             resultado = f"Error de sintaxis: {e}"
        except Exception as e:
             resultado = f"Ocurrió un error inesperado durante el análisis: {e}"

    except Exception as e:
         resultado = f"Error durante la inicialización del parser: {e}"

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