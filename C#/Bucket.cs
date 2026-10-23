using System;
using System.Collections.Generic;

class Bucket {
    static List<int> BucketSort(List<int> arr) {
        List<List<int>> cubetas = new List<List<int>>();
        for (int i = 0; i < 10; i++) cubetas.Add(new List<int>());
        foreach (int x in arr) cubetas[x / 10].Add(x);
        List<int> resultado = new List<int>();
        foreach (List<int> c in cubetas) {
            c.Sort();
            resultado.AddRange(c);
        }
        return resultado;
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        List<int> resultado = BucketSort(numeros);
        Console.WriteLine("Después: " + string.Join(" ", resultado));
    }
}
