import java.util.ArrayList;
import java.util.List;

public class Quick {
    static List<Integer> quick(List<Integer> arr) {
        if (arr.size() <= 1) return arr;
        int pivote = arr.get(arr.size() / 2);
        List<Integer> menores = new ArrayList<>();
        List<Integer> iguales = new ArrayList<>();
        List<Integer> mayores = new ArrayList<>();
        for (int x : arr) {
            if (x < pivote) menores.add(x);
            else if (x == pivote) iguales.add(x);
            else mayores.add(x);
        }
        List<Integer> resultado = new ArrayList<>(quick(menores));
        resultado.addAll(iguales);
        resultado.addAll(quick(mayores));
        return resultado;
    }

    public static void main(String[] args) {
        List<Integer> numeros = new ArrayList<>(List.of(5, 3, 8, 1, 9, 2));
        System.out.println("Antes: " + numeros);
        System.out.println("Después: " + quick(numeros));
    }
}
