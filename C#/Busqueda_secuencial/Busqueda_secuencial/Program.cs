using System;

class Program
{
    static int[] arreglo = { 15, 3, 42, 8, 23 };

    static int BusquedaSecuencial(int valor)
    {
        for (int i = 0; i < arreglo.Length; i++)
        {
            if (arreglo[i] == valor)
            {
                return i;
            }
        }
        return -1;
    }

    static void Main(string[] args)
    {
        Console.WriteLine(BusquedaSecuencial(42));
    }
}