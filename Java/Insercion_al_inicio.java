public class Insercion_al_inicio {
    public static void main(String[] args) {
        int[] arreglo = new int[10];
        arreglo[0] = 10;
        arreglo[1] = 20;
        arreglo[2] = 30;
        int n = 3;
        int valor = 1;

        for (int i = n; i > 0; i--) {
            arreglo[i] = arreglo[i - 1];
        }
        arreglo[0] = valor;
        n++;

        for (int i = 0; i < n; i++)
            System.out.print(arreglo[i] + " ");
    }
}