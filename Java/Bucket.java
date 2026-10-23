import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Bucket {
    static List<Integer> bucket(int[] arr) {
        List<List<Integer>> cubetas = new ArrayList<>();
        for (int i = 0; i < 10; i++) cubetas.add(new ArrayList<>());
        for (int x : arr) cubetas.get(x / 10).add(x);
        List<Integer> resultado = new ArrayList<>();
        for (List<Integer> c : cubetas) {
            Collections.sort(c);
            resultado.addAll(c);
        }
        return resultado;
    }

    public static void main(String[] args) {
        int[] numeros = {5, 3, 8, 1, 9, 2};
        System.out.println("Antes: " + Arrays.toString(numeros));
        System.out.println("Después: " + bucket(numeros));
    }
}
