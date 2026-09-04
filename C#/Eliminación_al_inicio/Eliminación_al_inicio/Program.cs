using System;

class Program
{
    static int[] arreglo = { 10, 20, 30, 40 };
    static int n = 4;

    static void EliminarInicio()
    {
        for (int i = 0; i < n - 1; i++)
        {
            arreglo[i] = arreglo[i + 1];
        }
        n--;
    }

    static void Main(string[] args)
    {
        EliminarInicio();

        for (int i = 0; i < n; i++)
            Console.WriteLine(arreglo[i]);
    }
}