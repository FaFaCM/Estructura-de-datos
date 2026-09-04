public class Eliminacion_elegida {
    public static void main(String[] args) {
        int[] arreglo = {10, 20, 30, 40, 50};
        int n = 5;
        int pos = 2;

        for (int i = pos; i < n - 1; i++) {
            arreglo[i] = arreglo[i + 1];
        }
        n--;

        for (int i = 0; i < n; i++)
            System.out.print(arreglo[i] + " ");
    }
}