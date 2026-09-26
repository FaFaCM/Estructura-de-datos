import java.util.Arrays;

public class Bubble {
    static void burbuja(int[] arr) {
        int n = arr.length;
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

    public static void main(String[] args) {
        int[] numeros = {5, 3, 8, 1, 9, 2};
        System.out.println("Antes: " + Arrays.toString(numeros));
        burbuja(numeros);
        System.out.println("Después: " + Arrays.toString(numeros));
    }
}
