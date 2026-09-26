def mezclar(a, b):
    resultado = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1
    resultado.extend(a[i:])
    resultado.extend(b[j:])
    return resultado

def merge(arr):
    if len(arr) <= 1:
        return arr
    medio = len(arr) // 2
    izquierda = merge(arr[:medio])
    derecha = merge(arr[medio:])
    return mezclar(izquierda, derecha)

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", merge(numeros))
