using System;

class Program
{
    static void Main(string[] args)
    {
        int[] arreglo = { 10, 20, 30, 40, 50 };

        for (int i = arreglo.Length - 1; i >= 0; i--)
        {
            Console.WriteLine($"Posición {i}: {arreglo[i]}");
        }
    }
}
