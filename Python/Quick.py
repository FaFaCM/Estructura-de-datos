def quick(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    menores = [x for x in arr if x < pivote]
    iguales = [x for x in arr if x == pivote]
    mayores = [x for x in arr if x > pivote]
    return quick(menores) + iguales + quick(mayores)

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", quick(numeros))
