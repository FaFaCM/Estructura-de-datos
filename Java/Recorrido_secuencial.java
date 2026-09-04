public class Recorrido_secuencial {
    public static void main(String[] args) {
        int[] arreglo = {10, 20, 30, 40, 50};
        int n = 5;

        for (int i = 0; i < n; i++) {
            System.out.println("Posición " + i + ": " + arreglo[i]);
        }
    }
}