public class Recorrido_inverso {
    public static void main(String[] args) {
        int[] arreglo = {10, 20, 30, 40, 50};
        int n = 5;

        for (int i = n - 1; i >= 0; i--) {
            System.out.println("Posición " + i + ": " + arreglo[i]);
        }
    }
}