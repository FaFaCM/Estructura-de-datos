using System;

class Program
{
    static int[] arreglo = { 10, 20, 30, 40 };
    static int n = 4;

    static void EliminarFinal()
    {
        n--;
    }

    static void Main(string[] args)
    {
        EliminarFinal();

        for (int i = 0; i < n; i++)
            Console.WriteLine(arreglo[i]);
    }
}
