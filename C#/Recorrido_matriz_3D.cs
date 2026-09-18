using System;

class Recorrido_matriz_3D {
    static void Main() {
        int[,,] matriz3D = {
            {{1, 2}, {3, 4}},
            {{5, 6}, {7, 8}}
        };

        for (int k = 0; k < matriz3D.GetLength(0); k++)
            for (int i = 0; i < matriz3D.GetLength(1); i++)
                for (int j = 0; j < matriz3D.GetLength(2); j++)
                    Console.Write(matriz3D[k, i, j] + " ");
        Console.WriteLine();
    }
}
