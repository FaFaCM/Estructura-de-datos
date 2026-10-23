import java.util.Arrays;

public class Shell {
    static void shell(int[] arr) {
        int n = arr.length;
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

    public static void main(String[] args) {
        int[] numeros = {5, 3, 8, 1, 9, 2};
        System.out.println("Antes: " + Arrays.toString(numeros));
        shell(numeros);
        System.out.println("Después: " + Arrays.toString(numeros));
    }
}
