using System;

class Program
{
    static int[] arreglo = new int[10] { 10, 20, 30, 0, 0, 0, 0, 0, 0, 0 };
    static int n = 3;

    static void InsertarInicio(int valor)
    {
        for (int i = n; i > 0; i--)
        {
            arreglo[i] = arreglo[i - 1];
        }
        arreglo[0] = valor;
        n++;
    }

    static void Main(string[] args)
    {
        InsertarInicio(1);

        for (int i = 0; i < n; i++)
            Console.WriteLine(arreglo[i]);
    }
}
