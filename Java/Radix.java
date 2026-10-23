import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Radix {
    static void radix(int[] arr) {
        int mayor = Arrays.stream(arr).max().getAsInt();
        for (int exp = 1; mayor / exp > 0; exp *= 10) {
            List<List<Integer>> cubetas = new ArrayList<>();
            for (int i = 0; i < 10; i++) cubetas.add(new ArrayList<>());
            for (int x : arr) cubetas.get((x / exp) % 10).add(x);
            int k = 0;
            for (List<Integer> c : cubetas)
                for (int x : c) arr[k++] = x;
        }
    }

    public static void main(String[] args) {
        int[] numeros = {5, 3, 8, 1, 9, 2};
        System.out.println("Antes: " + Arrays.toString(numeros));
        radix(numeros);
        System.out.println("Después: " + Arrays.toString(numeros));
    }
}
