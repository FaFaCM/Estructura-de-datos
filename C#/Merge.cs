using System;
using System.Collections.Generic;

class Merge {
    static List<int> Mezclar(List<int> a, List<int> b) {
        List<int> resultado = new List<int>();
        int i = 0, j = 0;
        while (i < a.Count && j < b.Count) {
            if (a[i] <= b[j]) resultado.Add(a[i++]);
            else resultado.Add(b[j++]);
        }
        while (i < a.Count) resultado.Add(a[i++]);
        while (j < b.Count) resultado.Add(b[j++]);
        return resultado;
    }

    static List<int> MergeSort(List<int> arr) {
        if (arr.Count <= 1) return arr;
        int medio = arr.Count / 2;
        List<int> izquierda = MergeSort(arr.GetRange(0, medio));
        List<int> derecha = MergeSort(arr.GetRange(medio, arr.Count - medio));
        return Mezclar(izquierda, derecha);
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        List<int> resultado = MergeSort(numeros);
        Console.WriteLine("Después: " + string.Join(" ", resultado));
    }
}
