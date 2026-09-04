using System;

class Program
{
    static int[] arreglo = { 10, 20, 30, 40, 50 };
    static int n = 5;

    static void EliminarPosicion(int pos)
    {
        for (int i = pos; i < n - 1; i++)
        {
            arreglo[i] = arreglo[i + 1];
        }
        n--;
    }

    static void Main(string[] args)
    {
        EliminarPosicion(2);

        for (int i = 0; i < n; i++)
            Console.WriteLine(arreglo[i]);
    }
}
