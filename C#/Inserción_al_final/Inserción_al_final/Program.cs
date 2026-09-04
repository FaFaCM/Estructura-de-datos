using System;

class Program
{
    static int[] arreglo = new int[10] { 10, 20, 30, 0, 0, 0, 0, 0, 0, 0 };
    static int n = 3;

    static void InsertarFinal(int valor)
    {
        arreglo[n] = valor;
        n++;
    }

    static void Main(string[] args)
    {
        InsertarFinal(40);

        for (int i = 0; i < n; i++)
            Console.WriteLine(arreglo[i]);
    }
}