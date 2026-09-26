import java.util.Arrays;

public class Seleccion {
    static void seleccion(int[] arr) {
        int n = arr.length;
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

    public static void main(String[] args) {
        int[] numeros = {5, 3, 8, 1, 9, 2};
        System.out.println("Antes: " + Arrays.toString(numeros));
        seleccion(numeros);
        System.out.println("Después: " + Arrays.toString(numeros));
    }
}
