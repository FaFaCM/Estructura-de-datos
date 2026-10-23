def radix(arr):
    mayor = max(arr)
    exp = 1
    while mayor // exp > 0:
        cubetas = [[] for _ in range(10)]
        for x in arr:
            cubetas[(x // exp) % 10].append(x)
        arr = [x for c in cubetas for x in c]
        exp *= 10
    return arr

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", radix(numeros))
