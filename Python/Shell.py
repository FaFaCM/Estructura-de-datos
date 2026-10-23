def shell(arr):
    n = len(arr)
    salto = n // 2
    while salto > 0:
        for i in range(salto, n):
            temp = arr[i]
            j = i
            while j >= salto and arr[j - salto] > temp:
                arr[j] = arr[j - salto]
                j -= salto
            arr[j] = temp
        salto //= 2
    return arr

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", shell(numeros))
