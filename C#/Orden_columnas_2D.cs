using System;

class Orden_columnas_2D {
    static void Main() {
        int[,] matriz2D = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        for (int j = 0; j < matriz2D.GetLength(1); j++)
            for (int i = 0; i < matriz2D.GetLength(0); i++)
                Console.Write(matriz2D[i, j] + " ");
        Console.WriteLine();
    }
}
