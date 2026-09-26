import java.util.ArrayList;
import java.util.List;

public class Merge {
    static List<Integer> mezclar(List<Integer> a, List<Integer> b) {
        List<Integer> resultado = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.size() && j < b.size()) {
            if (a.get(i) <= b.get(j)) resultado.add(a.get(i++));
            else resultado.add(b.get(j++));
        }
        while (i < a.size()) resultado.add(a.get(i++));
        while (j < b.size()) resultado.add(b.get(j++));
        return resultado;
    }

    static List<Integer> merge(List<Integer> arr) {
        if (arr.size() <= 1) return arr;
        int medio = arr.size() / 2;
        List<Integer> izquierda = merge(new ArrayList<>(arr.subList(0, medio)));
        List<Integer> derecha = merge(new ArrayList<>(arr.subList(medio, arr.size())));
        return mezclar(izquierda, derecha);
    }

    public static void main(String[] args) {
        List<Integer> numeros = new ArrayList<>(List.of(5, 3, 8, 1, 9, 2));
        System.out.println("Antes: " + numeros);
        System.out.println("Después: " + merge(numeros));
    }
}
