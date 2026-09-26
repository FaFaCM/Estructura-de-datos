def seleccion(arr):
    n = len(arr)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if arr[j] < arr[menor]:
                menor = j
        arr[i], arr[menor] = arr[menor], arr[i]
    return arr

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", seleccion(numeros))
