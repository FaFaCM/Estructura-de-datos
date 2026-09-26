using System;
using System.Collections.Generic;

class Insercion {
    static void Insercion_(List<int> arr) {
        for (int i = 1; i < arr.Count; i++) {
            int actual = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > actual) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = actual;
        }
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        Insercion_(numeros);
        Console.WriteLine("Después: " + string.Join(" ", numeros));
    }
}
