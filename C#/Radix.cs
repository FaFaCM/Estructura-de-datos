using System;
using System.Collections.Generic;
using System.Linq;

class Radix {
    static void RadixSort(List<int> arr) {
        int mayor = arr.Max();
        for (int exp = 1; mayor / exp > 0; exp *= 10) {
            List<List<int>> cubetas = new List<List<int>>();
            for (int i = 0; i < 10; i++) cubetas.Add(new List<int>());
            foreach (int x in arr) cubetas[(x / exp) % 10].Add(x);
            int k = 0;
            foreach (List<int> c in cubetas)
                foreach (int x in c) arr[k++] = x;
        }
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        RadixSort(numeros);
        Console.WriteLine("Después: " + string.Join(" ", numeros));
    }
}
