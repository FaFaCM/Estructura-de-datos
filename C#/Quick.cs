using System;
using System.Collections.Generic;
using System.Linq;

class Quick {
    static List<int> QuickSort(List<int> arr) {
        if (arr.Count <= 1) return arr;
        int pivote = arr[arr.Count / 2];
        List<int> menores = arr.Where(x => x < pivote).ToList();
        List<int> iguales = arr.Where(x => x == pivote).ToList();
        List<int> mayores = arr.Where(x => x > pivote).ToList();
        List<int> resultado = new List<int>(QuickSort(menores));
        resultado.AddRange(iguales);
        resultado.AddRange(QuickSort(mayores));
        return resultado;
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        List<int> resultado = QuickSort(numeros);
        Console.WriteLine("Después: " + string.Join(" ", resultado));
    }
}
