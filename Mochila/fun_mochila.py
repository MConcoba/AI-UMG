


def mochila_fracionaria(capacidad, valores):
    """    
    :parametro capacidad: Capacidad máxima de la mochila
    :parametro valores: Lista de tuplas (valor, peso) de cada objeto
    :devuelve: Máximo beneficio y los objetos seleccionados con sus fracciones
    """
    # Ordenar los objetos en base a la mejor relación valor/peso (descendente)
    valores.sort(key=lambda x: x[0] / x[1], reverse=True)

    print(valores)
    
    total_beneficio = 0  
    contenido_mochila = [] 
    
    for beneficio, peso in valores:
        if capacidad >= peso:  
            # Si el objeto cabe completo, lo tomamos
            contenido_mochila.append((beneficio, peso, 1))  # Se toma el 100% (1)
            total_beneficio += beneficio
            capacidad -= peso
        else:
            # Si no cabe completo, tomamos la fracción que cabe
            fraccion = capacidad / peso
            contenido_mochila.append((beneficio, peso, fraccion))  
            total_beneficio += beneficio * fraccion
            break 
    
    return total_beneficio, contenido_mochila

capacidad = 20
objetos = [(25, 18), (24, 15), (15, 10)]  # (Beneficio, Peso)

max_value, valores_seleccionados = mochila_fracionaria(capacidad, objetos)

print(f"Máximo beneficio posible: {max_value}")
print("Objetos seleccionados:")
for beneficio, peso, fraccion in valores_seleccionados:
    print(f" - Valor: {beneficio}, Peso: {peso}, Fracción tomada: {fraccion:.2f}")