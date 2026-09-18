using System;

class Orden_filas_2D {
    static void Main() {
        int[,] matriz2D = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        for (int i = 0; i < matriz2D.GetLength(0); i++)
            for (int j = 0; j < matriz2D.GetLength(1); j++)
                Console.Write(matriz2D[i, j] + " ");
        Console.WriteLine();
    }
}
