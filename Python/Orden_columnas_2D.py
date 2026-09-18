matriz2D = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

def orden_por_columnas(m):
    for j in range(len(m[0])):
        for i in range(len(m)):
            print(m[i][j], end=" ")
    print()

orden_por_columnas(matriz2D)