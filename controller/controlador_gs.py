from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from sympy import sympify

class ControladorGaussSeidel:
    """
    Clase controladora para el método iterativo de Gauss-Seidel.
    
    Actúa como intermediario entre la interfaz gráfica (Vista) y la lógica de 
    negocio (Modelo), gestionando la entrada de datos, la validación de 
    convergencia y la actualización de los componentes visuales.
    """

    def __init__(self, vista, modelo):
        """
        Inicializa el controlador estableciendo la conexión entre vista y modelo.

        Args:
            vista (QWidget): Instancia de la interfaz de usuario.
            modelo (Objeto): Instancia que contiene el algoritmo de Gauss-Seidel.
        """
        self.vista = vista
        self.modelo = modelo
        
        # Conexión del evento click del botón principal para iniciar el procesamiento
        self.vista.btn_resolver.clicked.connect(self.procesar_sistema)

    def limpiar_texto_matematico(self, texto):
        """
        Normaliza expresiones matemáticas ingresadas como texto.
        
        Sustituye caracteres especiales y símbolos visuales por operadores 
        compatibles con el motor de evaluación SymPy.

        Args:
            texto (str): Cadena de texto proveniente de los inputs de la interfaz.

        Returns:
            str: Cadena formateada lista para ser evaluada matemáticamente.
        """
        reemplazos = {
        '√': 'sqrt',
        '÷': '/',
        '²': '**2',
        'π': 'pi',
        'e': 'E'  # SymPy reconoce 'E' (mayúscula) como la constante de Euler
    }
        for visual, codigo in reemplazos.items():
            texto = texto.replace(visual, codigo)
        return texto

    def procesar_sistema(self):
        """
        Orquesta el flujo principal de la aplicación: captura, validación y ejecución.
        
        1. Recupera los datos de los QLineEdit de la vista.
        2. Realiza el parseo matemático de los coeficientes y resultados.
        3. Ejecuta el algoritmo a través del modelo.
        4. Gestiona las excepciones de entrada y estados de convergencia.
        """
        try:
            # 1. Extracción y conversión de la Matriz de Coeficientes (A)
            A = []
            for fila_edit in self.vista.coeffs:
                fila_numerica = []
                for edit in fila_edit:
                    texto_limpio = self.limpiar_texto_matematico(edit.text())
                    # Evaluación simbólica para soportar expresiones (e.g., pi/2, sqrt(3))
                    valor = float(sympify(texto_limpio))
                    fila_numerica.append(valor)
                A.append(fila_numerica)
            
            # 2. Extracción y conversión del Vector de Términos Independientes (b)
            b = []
            for res_edit in self.vista.results:
                texto_limpio = self.limpiar_texto_matematico(res_edit.text())
                b.append(float(sympify(texto_limpio)))
            
            # 3. Recuperación de la tolerancia definida por el usuario
            tol = float(self.vista.tol_input.text())
            
            # 4. Invocación del núcleo algorítmico en la capa del modelo
            pasos, exito, info = self.modelo.resolver_gauss_seidel(A, b, tol)
            
            # 5. Validación de la integridad de la solución
            # Si el algoritmo no converge o no se generaron iteraciones, se detiene el flujo.
            if not exito and len(pasos) <= 1:
                self.manejar_error_convergencia()
                return

            # 6. Actualización del estado visual de éxito
            self.vista.lbl_estado.setText("✅ Cálculo finalizado. El sistema convergió.")
            self.vista.lbl_estado.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 14px;")
            
            # Configuración dinámica del botón para previsualizar la matriz procesada
            self.vista.btn_ver_matriz.setVisible(True)
            try: 
                self.vista.btn_ver_matriz.clicked.disconnect()
            except: 
                pass 
            self.vista.btn_ver_matriz.clicked.connect(lambda: self.mostrar_popup_matriz(info))
            
            # Renderizado de los resultados iterativos en la tabla principal
            self.actualizar_tabla_resultados(pasos)

        except Exception as e:
            # Manejo de errores de entrada de datos (campos vacíos, caracteres no numéricos)
            self.vista.lbl_estado.setText(f"⚠️ Error: Verifique los datos ingresados.")
            self.vista.lbl_estado.setStyleSheet("color: #ff4444; font-weight: bold;")
            self.vista.tabla.setRowCount(0)
            self.vista.btn_ver_matriz.setVisible(False)

    def manejar_error_convergencia(self):
        """
        Notifica al usuario mediante la UI y un cuadro de diálogo sobre la falta 
        de diagonal dominancia en la matriz, lo que impide garantizar la convergencia.
        """
        self.vista.lbl_estado.setText("❌ ERROR: La matriz no es diagonal dominante.")
        self.vista.lbl_estado.setStyleSheet("color: #ff4444; font-weight: bold;")
        self.vista.tabla.setRowCount(0)
        self.vista.btn_ver_matriz.setVisible(False)
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Fallo de Convergencia")
        msg.setText("El sistema no cumple con el criterio de diagonal dominante y no pudo ser reordenado automáticamente. "
                   "El método de Gauss-Seidel podría no encontrar una solución válida.")
        msg.exec()

    def mostrar_popup_matriz(self, info):
        """
        Despliega un cuadro de diálogo con la representación textual de la 
        matriz aumentada final utilizada por el algoritmo tras el reordenamiento.

        Args:
            info (dict): Diccionario que contiene 'matriz_final' y 'vector_final'.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Matriz de Trabajo (Ordenada)")
        
        matriz = info['matriz_final']
        vector = info['vector_final']
        
        texto = "Esta es la configuración de filas que garantiza la solución:\n\n"
        for i in range(3):
            f = matriz[i]
            # Formateo de columnas para alineación visual correcta
            texto += f"| {f[0]:>8.4f}  {f[1]:>8.4f}  {f[2]:>8.4f} |   | {vector[i]:>8.4f} |\n"
        
        msg.setText(texto)
        msg.setStyleSheet("font-family: 'Courier New';")  # Aplicación de fuente monoespaciada
        msg.exec()

    def actualizar_tabla_resultados(self, pasos):
        """
        Puebla el widget QTableWidget de la vista con los resultados de cada iteración.
        
        Los valores numéricos se formatean con una precisión de 4 decimales.

        Args:
            pasos (list): Lista de diccionarios con la traza de cada iteración del método.
        """
        self.vista.tabla.setRowCount(0)
        
        for p in pasos:
            row = self.vista.tabla.rowCount()
            self.vista.tabla.insertRow(row)
            
            def fmt(val):
                """Aplica formato decimal fijo o marcador de posición si es nulo."""
                return f"{val:.4f}" if val is not None else " ---- "

            # Mapeo de datos a las columnas de la tabla (Iteración, Variables, Errores)
            self.vista.tabla.setItem(row, 0, QTableWidgetItem(str(p['iter'])))
            self.vista.tabla.setItem(row, 1, QTableWidgetItem(fmt(p['x'][0])))
            self.vista.tabla.setItem(row, 2, QTableWidgetItem(fmt(p['x'][1])))
            self.vista.tabla.setItem(row, 3, QTableWidgetItem(fmt(p['x'][2])))
            
            ex, ey, ez = p['errores']
            self.vista.tabla.setItem(row, 4, QTableWidgetItem(fmt(ex)))
            self.vista.tabla.setItem(row, 5, QTableWidgetItem(fmt(ey)))
            self.vista.tabla.setItem(row, 6, QTableWidgetItem(fmt(ez)))
            self.vista.tabla.setItem(row, 7, QTableWidgetItem(fmt(p['e_max'])))