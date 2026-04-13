# model/algoritmos.py
import itertools

def redondear_valor(valor):
    """
    Aplica un redondeo estándar a 4 decimales.
    
    Asegura la consistencia numérica en los cálculos iterativos según 
    el requerimiento de precisión de la aplicación.
    """
    return round(valor, 4)

def calcular_error(actual, anterior):
    """
    Calcula el error relativo porcentual entre la iteración actual y la anterior.
    
    Args:
        actual (float): Valor obtenido en la iteración presente.
        anterior (float): Valor obtenido en la iteración previa.
        
    Returns:
        float: Error relativo porcentual redondeado a 4 decimales.
    """
    if actual == 0: 
        return 100.0
    return redondear_valor(abs((actual - anterior) / actual) * 100)

def es_diagonal_dominante(A):
    """
    Verifica si una matriz cumple con el criterio de diagonal dominancia.
    
    Este criterio es una condición suficiente (aunque no necesaria) para 
    garantizar la convergencia del método de Gauss-Seidel.
    
    Args:
        A (list): Matriz de coeficientes.
        
    Returns:
        bool: True si es estrictamente dominante por filas, False en caso contrario.
    """
    n = len(A)
    for i in range(n):
        suma_fila = 0.0
        for j in range(n):
            if i != j:
                suma_fila = suma_fila + abs(A[i][j])
        valor_diagonal = abs(A[i][i])
        if valor_diagonal <= suma_fila:
            return False      
    return True

def ordenar_para_diagonal_dominante(A, b):
    """
    Busca una permutación de filas que haga la matriz diagonal dominante.
    
    Evalúa todas las combinaciones posibles de filas para encontrar una 
    configuración que asegure la convergencia del método.
    
    Args:
        A (list): Matriz de coeficientes original.
        b (list): Vector de términos independientes original.
        
    Returns:
        tuple: (Matriz reordenada, Vector reordenado, Estado de éxito).
    """
    n = len(A)
    indices = list(range(n))
    # Exploración de permutaciones para optimizar la convergencia
    for p in itertools.permutations(indices):
        A_perm = [A[i] for i in p]
        b_perm = [b[i] for i in p]
        if es_diagonal_dominante(A_perm):
            return A_perm, b_perm, True
    return A, b, False

def resolver_gauss_seidel(A_orig, b_orig, tolerancia,indice_criterio, max_iteraciones=100):
    """
    Ejecuta el método iterativo de Gauss-Seidel para resolver sistemas de ecuaciones lineales.
    
    El proceso incluye pre-procesamiento de la matriz para asegurar convergencia, 
    cálculo de iteraciones con redondeo controlado y seguimiento de errores relativos.

    Args:
        A_orig (list): Matriz de coeficientes de entrada.
        b_orig (list): Vector de resultados de entrada.
        tolerancia (float): Umbral de error máximo permitido para detener el proceso.
        max_iteraciones (int): Límite de seguridad para evitar bucles infinitos.

    Returns:
        tuple: (Lista de pasos detallados, Booleano de éxito, Diccionario de metadatos del proceso).
    """
    # 1. Fase de Pre-procesamiento: Intento de reordenamiento de filas
    A_ord, b_ord, fue_ordenada = ordenar_para_diagonal_dominante(A_orig, b_orig)
    
    # Verificación de seguridad previa a la ejecución
    if not es_diagonal_dominante(A_ord):
        return [], False, {"mensaje": "La matriz no converge: No es diagonal dominante.", "ordenada": False}

    # 2. Inicialización de estructuras de control y registro
    info_proceso = {
        "matriz_final": A_ord,
        "vector_final": b_ord,
        "ordenada": fue_ordenada
    }
    
    n = len(A_ord)
    x = [0.0] * n  # Vector de aproximación inicial (semilla)
    pasos = []
    
    # Registro de la Iteración 0 (Estado inicial)
    pasos.append({
        'iter': 0,
        'x': x[:],
        'errores': [None] * n,
        'e_max': None
    })

    # 3. Núcleo iterativo del algoritmo
    for k in range(1, max_iteraciones + 1):
        x_ant = x[:]
        errores_step = []
        
        for i in range(n):
            # Cálculo de la sumatoria de los términos conocidos en la fila i
            suma = sum(A_ord[i][j] * x[j] for j in range(n) if i != j)
            
            # Actualización inmediata del valor x[i] (Propiedad distintiva de Gauss-Seidel)
            x[i] = redondear_valor((b_ord[i] - suma) / A_ord[i][i])
            
            # Evaluación del error relativo local
            errores_step.append(calcular_error(x[i], x_ant[i]))

        # Evaluación del criterio de parada basado en el error máximo de la iteración
        if indice_criterio == 0: # "Todas"
            e_comparacion = max(errores_step)
        elif indice_criterio == 1: # "Solo x"
            e_comparacion = errores_step[0]
        elif indice_criterio == 2: # "Solo y"
            e_comparacion = errores_step[1]
        else: # "Solo z"
            e_comparacion = errores_step[2]
        pasos.append({
            'iter': k,
            'x': x[:],
            'errores': errores_step,
            'e_max': e_comparacion
        })
        
        # Condición de salida por convergencia exitosa
        if e_comparacion < tolerancia:
            return pasos, True, info_proceso

    # Retorno en caso de alcanzar el máximo de iteraciones sin converger
    return pasos, False, info_proceso