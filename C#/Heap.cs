using System;
using System.Collections.Generic;

class Heap {
    static void Heapify(List<int> arr, int n, int i) {
        int mayor = i;
        int izq = 2 * i + 1;
        int der = 2 * i + 2;
        if (izq < n && arr[izq] > arr[mayor]) mayor = izq;
        if (der < n && arr[der] > arr[mayor]) mayor = der;
        if (mayor != i) {
            int temp = arr[i];
            arr[i] = arr[mayor];
            arr[mayor] = temp;
            Heapify(arr, n, mayor);
        }
    }

    static void HeapSort(List<int> arr) {
        int n = arr.Count;
        for (int i = n / 2 - 1; i >= 0; i--) Heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            Heapify(arr, i, 0);
        }
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        HeapSort(numeros);
        Console.WriteLine("Después: " + string.Join(" ", numeros));
    }
}
