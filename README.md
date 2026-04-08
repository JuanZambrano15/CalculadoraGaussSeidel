<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/PyQt6-6.x-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
<img src="https://img.shields.io/badge/SymPy-1.x-3B5526?style=for-the-badge&logo=sympy&logoColor=white" />
<img src="https://img.shields.io/badge/Patrón-MVC-FF6B35?style=for-the-badge" />
<img src="https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge" />

<br/><br/>

# 🔢 Gauss-Seidel Solver

### Resolución iterativa de sistemas de ecuaciones lineales 3×3

*Aplicación de escritorio con interfaz gráfica, construida sobre el patrón MVC en Python + PyQt6.*

<br/>

[✨ Características](#-características) · [🚀 Instalación](#-instalación) · [🧭 Uso](#-uso) · [🏗️ Arquitectura](#%EF%B8%8F-arquitectura) · [📐 Algoritmo](#-algoritmo) · [📖 Documentación](#-documentación)

---

</div>

## ✨ Características

| Funcionalidad | Descripción |
|---|---|
| 🔄 **Método de Gauss-Seidel** | Implementación iterativa completa con actualización inmediata de valores |
| 🧮 **Evaluación simbólica** | Acepta expresiones como `π/2`, `√3`, `2**3` gracias a SymPy |
| 📐 **Diagonal dominancia** | Verifica y reordena automáticamente la matriz para garantizar convergencia |
| 📊 **Tabla de iteraciones** | Visualiza `x`, `y`, `z` y errores relativos `(%)` por cada iteración |
| 🎛️ **Teclado matemático** | Botones para insertar `√`, `²`, `π`, `÷` directamente en los campos |
| 🔍 **Matriz de trabajo** | Muestra la configuración `[A|b]` usada tras el reordenamiento |
| ⚙️ **Tolerancia configurable** | El usuario define el umbral de error y el máximo de iteraciones |

---

## 📸 Vista previa

> La interfaz permite ingresar el sistema, ejecutar el algoritmo y visualizar la convergencia iteración por iteración.

```
┌─────────────────────────────────────────────────────────────┐
│  Funciones Especiales:  ½   √   x²   π   (   )   CE        │
├─────────────────────────────────────────────────────────────┤
│  Ec 1:  [ 10 ]  +  [ -1 ]  +  [  2 ]  =  [  6 ]           │
│  Ec 2:  [ -1 ]  +  [  11]  +  [ -1 ]  =  [ 25 ]           │
│  Ec 3:  [  2 ]  +  [ -1 ]  +  [ 10 ]  =  [-11 ]           │
├─────────────────────────────────────────────────────────────┤
│  Tolerancia (%): [0.0001]   Max Iteraciones: [100]          │
│                     [ RESOLVER SISTEMA ]                    │
├──────┬────────┬────────┬────────┬────────┬────────┬────────┤
│ Iter │   x    │   y    │   z    │  E_x % │  E_y % │ E_max  │
│  0   │ 0.0000 │ 0.0000 │ 0.0000 │  ----  │  ----  │  ----  │
│  1   │ 0.6000 │ 2.3273 │-0.9873 │100.000 │100.000 │100.000 │
│  2   │ 1.0302 │ 2.0369 │-1.0147 │  41.95 │  14.36 │  41.95 │
│ ...  │  ...   │  ...   │  ...   │  ...   │  ...   │  ...   │
└──────┴────────┴────────┴────────┴────────┴────────┴────────┘
```

---

## 🚀 Instalación

### Prerrequisitos

- Python `3.10` o superior
- `pip` actualizado

### Clonar el repositorio

```bash
git clone https://github.com/JuanZambrano15/CalculadoraGaussSeidel.git
cd CalculadoraGaussSeidel
```

### Instalar dependencias

```bash
pip install PyQt6 sympy
```

> **Nota:** No se requieren dependencias adicionales. La librería `itertools` es parte de la biblioteca estándar de Python.

---

## 🧭 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Paso a paso

1. **Ingresar los coeficientes** de la matriz `A` en los campos de la cuadrícula (Ec 1, Ec 2, Ec 3).
2. **Ingresar los términos independientes** `b` en la columna `=`.
3. *(Opcional)* Usar el **teclado matemático** para insertar `π`, `√(...)`, etc.
4. **Configurar** la tolerancia de error y el máximo de iteraciones.
5. Presionar **RESOLVER SISTEMA**.
6. Analizar la **tabla de convergencia** y, si lo deseas, consultar la **Matriz de Trabajo [A|b]**.

### Ejemplo de sistema compatible

```
10x  -  y  + 2z =   6
-x  + 11y  -  z =  25
 2x  -  y  + 10z = -11
```

> ✅ Este sistema es diagonal dominante y converge en pocas iteraciones.

### Interpretación de resultados

| Columna | Descripción |
|---|---|
| `Iter` | Número de la iteración actual (0 = estado inicial) |
| `x`, `y`, `z` | Valor aproximado de cada variable en esa iteración |
| `E_x (%)`, `E_y (%)`, `E_z (%)` | Error relativo porcentual de cada variable respecto a la iteración anterior |
| `E_Max (%)` | Error máximo de la iteración — usado como criterio de parada |

> Cuando `E_Max < Tolerancia`, el método **converge** y la solución es válida.

---

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC (Modelo–Vista–Controlador)** para separar responsabilidades:

```
gauss-seidel-solver/
│
├── main.py                      ← Punto de entrada (Entry Point)
│
├── model/
│   └── algoritmos.py            ← Lógica matemática (Modelo)
│
├── controller/
│   └── controlador_gs.py        ← Orquestación y validación (Controlador)
│
└── views/
    ├── ventana_principal.py     ← Interfaz gráfica PyQt6 (Vista)
    └── estilos.qss              ← Hoja de estilos Qt (opcional)
```

### Responsabilidades por capa

```
┌──────────────────────────────────────────────────────────────┐
│  VISTA (ventana_principal.py)                                │
│  • Renderiza la interfaz gráfica                             │
│  • Gestiona inputs del usuario                               │
│  • Actualiza componentes visuales (tabla, labels, botones)   │
└───────────────────────┬──────────────────────────────────────┘
                        │ eventos / datos
┌───────────────────────▼──────────────────────────────────────┐
│  CONTROLADOR (controlador_gs.py)                             │
│  • Captura y valida los datos de entrada                     │
│  • Parsea expresiones simbólicas con SymPy                   │
│  • Invoca el modelo y gestiona los resultados                │
│  • Maneja errores de convergencia y de entrada               │
└───────────────────────┬──────────────────────────────────────┘
                        │ llamadas al algoritmo
┌───────────────────────▼──────────────────────────────────────┐
│  MODELO (algoritmos.py)                                      │
│  • Implementa el método de Gauss-Seidel                      │
│  • Verifica y reordena la diagonal dominancia                │
│  • Retorna traza detallada de cada iteración                 │
└──────────────────────────────────────────────────────────────┘
```

---

## 📐 Algoritmo

### Método de Gauss-Seidel

El método de Gauss-Seidel resuelve sistemas `Ax = b` actualizando **inmediatamente** cada variable con el valor calculado en la misma iteración:

$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)$$

### Flujo del algoritmo implementado

```
Entrada: A, b, tolerancia, max_iteraciones
        │
        ▼
┌─────────────────────────────┐
│ ¿A es diagonal dominante?   │──NO──► Buscar permutación válida
└──────────────┬──────────────┘         │
               │ SÍ           ◄─────────┘
               ▼
        x⁰ = [0, 0, 0]   (semilla inicial)
               │
        ┌──────▼──────┐
        │  Iteración k │
        │  Para i=0..n │
        │   x[i] = (b[i] - Σ a[i][j]*x[j]) / a[i][i]
        │   e[i] = |x[i] - x_ant[i]| / |x[i]| * 100
        └──────┬───────┘
               │
        ¿E_max < tolerancia?
          │           │
         SÍ           NO (k < max_iter)
          │           │
          ▼           └──► k = k + 1
      CONVERGENCIA
```

### Criterio de parada

$$E_{max} = \max_i \left| \frac{x_i^{(k)} - x_i^{(k-1)}}{x_i^{(k)}} \right| \times 100 < \varepsilon$$

### Condición de convergencia

La matriz `A` debe ser **estrictamente diagonal dominante** por filas:

$$|a_{ii}| > \sum_{j \neq i} |a_{ij}| \quad \forall i$$

Si no se cumple, el algoritmo intenta automáticamente una **reordenación de filas** usando permutaciones (`itertools.permutations`). Si ninguna permutación satisface la condición, el proceso se detiene y se notifica al usuario.

---

## 📖 Documentación

### Documentación interna

Todos los módulos cuentan con **docstrings descriptivos** que explican propósito, argumentos y retornos:

```python
def resolver_gauss_seidel(A_orig, b_orig, tolerancia, max_iteraciones=100):
    """
    Ejecuta el método iterativo de Gauss-Seidel para resolver sistemas
    de ecuaciones lineales.

    Args:
        A_orig (list): Matriz de coeficientes de entrada.
        b_orig (list): Vector de resultados de entrada.
        tolerancia (float): Umbral de error máximo permitido.
        max_iteraciones (int): Límite de seguridad.

    Returns:
        tuple: (Lista de pasos, Booleano de éxito, Diccionario de metadatos)
    """
```

### Funciones principales

#### `model/algoritmos.py`

| Función | Descripción |
|---|---|
| `redondear_valor(valor)` | Redondea a 4 decimales para consistencia numérica |
| `calcular_error(actual, anterior)` | Error relativo porcentual entre iteraciones |
| `es_diagonal_dominante(A)` | Verifica la condición de convergencia |
| `ordenar_para_diagonal_dominante(A, b)` | Permuta filas para lograr diagonal dominancia |
| `resolver_gauss_seidel(A, b, tol, max_iter)` | Núcleo del método iterativo |

#### `controller/controlador_gs.py`

| Función | Descripción |
|---|---|
| `limpiar_texto_matematico(texto)` | Normaliza símbolos visuales (`√`, `π`, `²`) a sintaxis Python |
| `procesar_sistema()` | Orquesta captura → validación → ejecución → renderizado |
| `manejar_error_convergencia()` | Notifica fallo de diagonal dominancia |
| `mostrar_popup_matriz(info)` | Muestra la matriz `[A|b]` usada tras el reordenamiento |
| `actualizar_tabla_resultados(pasos)` | Puebla el `QTableWidget` con la traza iterativa |

### Manejo de errores

| Situación | Respuesta del sistema |
|---|---|
| Campo vacío o texto no numérico | `⚠️ Error: Verifique los datos ingresados.` |
| Matriz no diagonal dominante | `❌ ERROR: La matriz no es diagonal dominante.` + popup explicativo |
| Sin convergencia tras max iteraciones | Tabla parcial con las iteraciones registradas |

---

## 🧩 Dependencias

```
PyQt6>=6.4.0
sympy>=1.12
```

Instalar con:

```bash
pip install -r requirements.txt
```

---

## 👤 Autor
Juan José Zambrano Manzano (192327)  

Desarrollado como proyecto académico para el curso de **Métodos Numéricos** — Ingeniería de Sistemas.

---

<div align="center">

*"La convergencia no es un accidente — es una condición."*

⭐ Si este proyecto te fue útil, dale una estrella al repositorio.

</div>
