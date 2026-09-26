using System;
using System.Collections.Generic;

class Bubble {
    static void Burbuja(List<int> arr) {
        int n = arr.Count;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        Burbuja(numeros);
        Console.WriteLine("Después: " + string.Join(" ", numeros));
    }
}
