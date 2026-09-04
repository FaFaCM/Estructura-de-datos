arreglo = [2, 6, 23, 45, 67, 88]

def bus_bin(valor):
    izquierda = 0
    derecha = len(arreglo) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha ) // 2
        if arreglo[medio] == valor:
            return medio 
        elif arreglo[medio] < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

print(bus_bin(88))