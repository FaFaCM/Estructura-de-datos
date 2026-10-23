using System;
using System.Collections.Generic;

class Shell {
    static void ShellSort(List<int> arr) {
        int n = arr.Count;
        int salto = n / 2;
        while (salto > 0) {
            for (int i = salto; i < n; i++) {
                int temp = arr[i];
                int j = i;
                while (j >= salto && arr[j - salto] > temp) {
                    arr[j] = arr[j - salto];
                    j -= salto;
                }
                arr[j] = temp;
            }
            salto /= 2;
        }
    }

    static void Main() {
        List<int> numeros = new List<int> {5, 3, 8, 1, 9, 2};
        Console.WriteLine("Antes: " + string.Join(" ", numeros));
        ShellSort(numeros);
        Console.WriteLine("Después: " + string.Join(" ", numeros));
    }
}
