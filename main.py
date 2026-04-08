import sys
import os
from PyQt6.QtWidgets import QApplication
from views.ventana_principal import VentanaPrincipal
from controller.controlador_gs import ControladorGaussSeidel
import model.algoritmos as modelo

def cargar_estilos(app):
    """
    Carga y aplica la hoja de estilos global (QSS) a la aplicación.
    
    Busca el archivo de estilos en el directorio de vistas para separar
    la lógica de presentación de la estructura del código.

    Args:
        app (QApplication): Instancia principal de la aplicación PyQt6.
    """
    ruta_estilos = os.path.join("views", "estilos.qss")
    if os.path.exists(ruta_estilos):
        with open(ruta_estilos, "r") as f:
            # Aplicación del diseño visual mediante Qt Style Sheets
            app.setStyleSheet(f.read())

def main():
    """
    Punto de entrada principal del sistema (Entry Point).
    
    Orquesta la inicialización de los componentes del patrón MVC:
    1. Crea la instancia de la aplicación.
    2. Configura el diseño visual (Vista).
    3. Vincula la lógica algorítmica (Modelo) mediante el Controlador.
    4. Ejecuta el bucle principal de eventos.
    """
    # Inicialización del núcleo de Qt
    app = QApplication(sys.argv)
    
    # Carga de la configuración estética
    cargar_estilos(app)
    
    # Instanciación de la Interfaz Gráfica de Usuario
    vista = VentanaPrincipal()
    
    # Asignación de nombre de objeto para selectores específicos en el QSS
    vista.btn_resolver.setObjectName("btn_resolver")
    
    # Inyección de dependencias: se vincula la vista y el modelo al controlador
    controlador = ControladorGaussSeidel(vista, modelo)
    
    # Despliegue de la interfaz y ejecución del ciclo de vida de la aplicación
    vista.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # Asegura que el script solo se ejecute si es el módulo principal
    main()