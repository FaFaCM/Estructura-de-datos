using System;
using System.Collections.Generic;

class Seleccion {
    static void Seleccion_(List<int> arr) {
        int n = arr.Count;
        for (int i = 0; i < n - 1; i++) {
            int menor = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[menor]) menor = j;
            }
            int temp = arr[i];
            arr[i] = arr[menor];
            arr[menor] = temp;
        }
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        Seleccion_(numeros);
        Console.WriteLine("Después: " + string.Join(" ", numeros));
    }
}
