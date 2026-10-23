def bucket(arr):
    cubetas = [[] for _ in range(10)]
    for x in arr:
        cubetas[x // 10].append(x)
    resultado = []
    for c in cubetas:
        c.sort()
        resultado.extend(c)
    return resultado

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]
    print("Antes:", numeros)
    print("Después:", bucket(numeros))
