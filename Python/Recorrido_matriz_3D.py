matriz3D = [
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
]

def recorrido_3d(m):
    for capa in m:
        for fila in capa:
            for elemento in fila:
                print(elemento, end=" ")
    print()

recorrido_3d(matriz3D)