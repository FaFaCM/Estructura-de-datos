using System;

class Program
{
    static int[] arreglo = { 3, 8, 15, 23, 42, 56, 70 };

    static int BusquedaBinaria(int valor)
    {
        int izquierda = 0;
        int derecha = arreglo.Length - 1;

        while (izquierda <= derecha)
        {
            int medio = (izquierda + derecha) / 2;

            if (arreglo[medio] == valor)
            {
                return medio;
            }
            else if (arreglo[medio] < valor)
            {
                izquierda = medio + 1;
            }
            else
            {
                derecha = medio - 1;
            }
        }
        return -1;
    }

    static void Main(string[] args)
    {
        Console.WriteLine(BusquedaBinaria(23));
    }
}
