def burbuja(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", burbuja(numeros))
