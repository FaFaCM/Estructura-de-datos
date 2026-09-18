matriz2D = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

def recorrido_2d(m):
    for fila in m:
        for elemento in fila:
            print(elemento, end=" ")
    print()

recorrido_2d(matriz2D)