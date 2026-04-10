import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLineEdit, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame)
from PyQt6.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    """
    Clase que define la interfaz gráfica de usuario (GUI) principal.
    
    Proporciona una estructura visual para el ingreso de sistemas de ecuaciones 3x3,
    controles de configuración de algoritmos y visualización de resultados tabulares.
    """

    def __init__(self):
        """
        Inicializa la ventana principal configurando el layout base y los componentes.
        """
        super().__init__()
        self.setWindowTitle("Gauss-Seidel Solver - Ingeniería de Sistemas")
        self.setMinimumSize(900, 700)
        
        # Inicialización del contenedor principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Inicialización secuencial de las secciones de la interfaz
        self.setup_special_buttons()
        self.setup_inputs()
        self.setup_results_area()

    def setup_special_buttons(self):
        """
        Configura el panel de funciones especiales (teclado matemático).
        
        Permite insertar símbolos como raíces, potencias y constantes directamente 
        en el campo de texto que tenga el foco actual.
        """
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(QLabel("Funciones Especiales:"))
        
        # Mapeo de etiquetas visuales y sus valores lógicos correspondientes
        funciones = [('½', '/'), ('√', 'sqrt()'), ('x²', '**2'), ('π', 'pi'), 
                 ('e', 'e'), ('(', '('), (')', ')'), ('CE', 'clear')]
        
        for label, val in funciones:
            btn = QPushButton(label)
            btn.setFixedWidth(50)
            
            # CRÍTICO: Se desactiva el FocusPolicy para evitar que el botón le robe
            # el foco al QLineEdit, permitiendo la inserción de texto fluida.
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
            
            # Conexión del evento con paso de parámetros mediante clausura (lambda)
            btn.clicked.connect(lambda checked, v=val: self.insert_math(v))
            buttons_layout.addWidget(btn)
        
        buttons_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)

    def setup_inputs(self):
        """
        Construye la cuadrícula de entrada para los coeficientes de la matriz.
        
        Organiza dinámicamente los QLineEdit para representar un sistema de 
        ecuaciones lineales de 3 incógnitas (x, y, z).
        """
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.Shape.StyledPanel)
        grid = QGridLayout(input_frame)

        self.coeffs = []  # Estructura matricial para los objetos QLineEdit de coeficientes
        self.results = [] # Lista para los objetos QLineEdit de los términos b
        
        for i in range(3):
            fila = []
            grid.addWidget(QLabel(f"Ec {i+1}:"), i, 0)
            
            # Generación de campos para variables x, y, z
            for j in range(3):
                edit = QLineEdit()
                edit.setPlaceholderText(f"{'xyz'[j]}")
                grid.addWidget(edit, i, j*2 + 1)
                fila.append(edit)
                if j < 2: 
                    grid.addWidget(QLabel("+"), i, j*2 + 2)
            
            # Campo para el término independiente (resultado de la ecuación)
            grid.addWidget(QLabel("="), i, 6)
            res_edit = QLineEdit()
            grid.addWidget(res_edit, i, 7)
            self.results.append(res_edit)
            self.coeffs.append(fila)

        # Configuración de parámetros de precisión y control algorítmico
        config_layout = QHBoxLayout()
        self.tol_input = QLineEdit("0.0001")
        self.iter_input = QLineEdit("100")
        
        config_layout.addWidget(QLabel("Tolerancia (%):"))
        config_layout.addWidget(self.tol_input)
        config_layout.addWidget(QLabel("Max Iteraciones:"))
        config_layout.addWidget(self.iter_input)
        
        # Botón disparador del proceso de cálculo
        self.btn_resolver = QPushButton("RESOLVER SISTEMA")
        self.btn_resolver.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            font-weight: bold; 
            height: 40px;
        """)

        self.main_layout.addWidget(input_frame)
        self.main_layout.addLayout(config_layout)
        self.main_layout.addWidget(self.btn_resolver)

    def setup_results_area(self):
        """
        Prepara el área de salida, incluyendo retroalimentación de estado 
        y la tabla detallada de iteraciones.
        """
        # Etiqueta para mensajes informativos y diagnóstico de errores
        self.lbl_estado = QLabel("Estado: Esperando entrada de datos...")
        self.lbl_estado.setWordWrap(True)
        self.lbl_estado.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.main_layout.addWidget(self.lbl_estado)

        # Acceso directo a la matriz de trabajo (A|b) procesada por el algoritmo
        self.btn_ver_matriz = QPushButton("🔍 Ver Matriz de Trabajo Ordenada [A|b]")
        self.btn_ver_matriz.setFixedWidth(300)
        self.btn_ver_matriz.setVisible(False) 
        self.btn_ver_matriz.setStyleSheet("""
            QPushButton { 
                background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px; 
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.main_layout.addWidget(self.btn_ver_matriz)

        # Configuración del componente de visualización tabular
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "Iter", "x", "y", "z", 
            "E_x (%)", "E_y (%)", "E_z (%)", "E_Max (%)"
        ])
        
        # Optimización del espacio horizontal de la tabla
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.main_layout.addWidget(self.tabla)

    def insert_math(self, val):
        """
        Gestor de inserción de caracteres especiales en el widget activo.
        
        Detecta el QLineEdit enfocado y aplica una traducción visual antes de 
        insertar el símbolo o limpiar el contenido.

        Args:
            val (str): El valor o comando enviado por el botón de funciones especiales.
        """
        focused_widget = self.focusWidget()
        
        if isinstance(focused_widget, QLineEdit):
            # Diccionario de traducción para mostrar símbolos matemáticos elegantes
            traduccion_visual = {
                'sqrt()': '√(',
                '**2': '²',
                '/': '÷',
                'pi': 'π'
            }
            
            simbolo = traduccion_visual.get(val, val)
            
            if val == 'clear':
                focused_widget.clear()
            else:
                # Inserta el símbolo en la posición actual del cursor
                focused_widget.insert(simbolo)
            
            # Devuelve el foco al widget para permitir seguir escribiendo inmediatamente
            focused_widget.setFocus()