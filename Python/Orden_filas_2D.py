matriz2D = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

def orden_por_filas(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(m[i][j], end=" ")
    print()

orden_por_filas(matriz2D)