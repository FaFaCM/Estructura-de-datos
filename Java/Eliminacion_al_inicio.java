public class Eliminacion_al_inicio {
    public static void main(String[] args) {
        int[] arreglo = {10, 20, 30, 40};
        int n = 4;

        for (int i = 0; i < n - 1; i++) {
            arreglo[i] = arreglo[i + 1];
        }
        n--;

        for (int i = 0; i < n; i++)
            System.out.print(arreglo[i] + " ");
    }
} 
