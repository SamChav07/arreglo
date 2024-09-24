# eliminacionGauss/logic/matriz.py

class Matriz:
    """Clase que representa una matriz y permite realizar eliminación Gaussiana."""

    def __init__(self, entradas):
        """Inicializa la matriz con las entradas del usuario."""
        if not entradas:
            raise ValueError("La lista de entradas está vacía.")
        self.matriz = self.obtener_matriz(entradas)  # Obtener la matriz desde las entradas

    def obtener_matriz(self, entradas):
        """Convierte las entradas (instancias de Elim_Gauss) en una matriz."""
        try:
            # Crear una matriz vacía con dimensiones adecuadas
            max_row = max(entry.EG_NmEcuaciones for entry in entradas)
            max_col = max(entry.EG_NmIncognitas for entry in entradas)
            matriz = [[0.0 for _ in range(max_col)] for _ in range(max_row)]
            
            for entry in entradas:
                fila = entry.EG_NmEcuaciones - 1  # Ajustar a índice base 0
                columna = entry.EG_NmIncognitas - 1  # Ajustar a índice base 0
                matriz[fila][columna] = float(entry.EG_valor)  # Asignar el valor correspondiente
            
            return matriz
        except Exception as e:
            raise ValueError(f"Error al construir la matriz: {str(e)}")

    def imprimir_matriz(self, paso, operacion):
        """Genera un string que representa la matriz en un formato legible."""
        texto = f"Paso {paso} ({operacion}):\n"  
        for fila in self.matriz:
            texto += "  ".join(f"{valor:.2f}" for valor in fila) + "\n"  
        texto += "\n"
        return texto

    def eliminacion_gaussiana(self):
        """Realiza la eliminación Gaussiana para resolver el sistema de ecuaciones."""
        if not self.matriz:
            return "Matriz no válida."

        paso = 1
        resultado = ""
        filas, columnas = len(self.matriz), len(self.matriz[0])  
        fila_actual = 0

        for col in range(columnas - 1):
            if fila_actual >= filas:
                break  

            max_row = max(range(fila_actual, filas), key=lambda i: abs(self.matriz[i][col]))
            if abs(self.matriz[max_row][col]) < 1e-10:
                continue  

            if fila_actual != max_row:
                self.matriz[fila_actual], self.matriz[max_row] = self.matriz[max_row], self.matriz[fila_actual]
                resultado += self.imprimir_matriz(paso, f"Intercambio f{fila_actual + 1} <-> f{max_row + 1}")
                paso += 1

            pivote = self.matriz[fila_actual][col]  

            if abs(pivote) > 1e-10:
                self.matriz[fila_actual] = [elemento / pivote for elemento in self.matriz[fila_actual]]
                resultado += self.imprimir_matriz(paso, f"f{fila_actual + 1} -> (1/{pivote:.2f}) * f{fila_actual + 1}")
                paso += 1

            for i in range(filas):
                if i != fila_actual:
                    factor = self.matriz[i][col]
                    if abs(factor) > 1e-10:
                        self.matriz[i] = [self.matriz[i][k] - factor * self.matriz[fila_actual][k] for k in range(columnas)]
                        resultado += self.imprimir_matriz(paso, f"f{i + 1} -> f{i + 1} - ({factor:.2f}) * f{fila_actual + 1}")
                        paso += 1

            fila_actual += 1  

        resultado += self.interpretar_resultado()  
        return resultado

    def interpretar_resultado(self):
        """Interpreta la matriz reducida para expresar las soluciones y muestra las columnas pivote."""
        n, m = len(self.matriz), len(self.matriz[0]) - 1  
        pivotes = [-1] * m  
        resultado = "Solución del sistema:\n"
        soluciones = {}
        columnas_pivote = []  

        for j in range(m):
            for i in range(n):
                if abs(self.matriz[i][j] - 1) < 1e-10 and all(abs(self.matriz[k][j]) < 1e-10 for k in range(n) if k != i):
                    pivotes[j] = i
                    columnas_pivote.append(j + 1)  
                    break

        fila_inconsistente = [
            i for i, fila in enumerate(self.matriz)
            if all(abs(val) < 1e-10 for val in fila[:-1]) and abs(fila[-1]) > 1e-10
        ]
        
        inconsistente_var = set(f"x{i + 1}" for i in fila_inconsistente)

        for j in range(m):
            var_name = f"x{j + 1}"
            if var_name in inconsistente_var:
                soluciones[var_name] = f"{var_name} es inconsistente"
            elif pivotes[j] == -1:
                soluciones[var_name] = f"{var_name} es libre"
            else:
                fila = pivotes[j]
                constante = self.matriz[fila][-1]
                constante_str = (
                    f"{int(constante)}" if constante.is_integer() else f"{constante:.2f}"
                )

                terminos = []
                for k in range(m):
                    if k != j and pivotes[k] == -1 and abs(self.matriz[fila][k]) > 1e-10:
                        coef = -self.matriz[fila][k]
                        coef_str = (
                            f"{int(coef)}" if coef.is_integer() else f"{coef:.2f}"
                        )
                        if coef < 0:
                            terminos.append(f"{coef_str}x{k + 1}")
                        else:
                            terminos.append(f"+ {coef_str}x{k + 1}")

                ecuacion = ""
                if constante_str != "0":
                    ecuacion += constante_str

                if terminos:
                    if ecuacion and ecuacion != "0":
                        ecuacion += " " + " ".join(terminos)
                    else:
                        ecuacion = " ".join(terminos).lstrip("+ ").strip() 

                soluciones[var_name] = f"{var_name} = {ecuacion}".strip()

        for i in range(m):
            var_name = f"x{i + 1}"
            if var_name in soluciones:
                resultado += f"{soluciones[var_name]}\n"

        if inconsistente_var:
            resultado += "\nEl sistema es inconsistente y no tiene soluciones.\n"
        elif any(pivote == -1 for pivote in pivotes):
            resultado += "\nHay infinitas soluciones debido a variables libres.\n"
        else:
            resultado += "\nLa solución es única.\n"

        resultado += f"\nLas columnas pivote son: {', '.join(map(str, columnas_pivote))}.\n"

        return resultado