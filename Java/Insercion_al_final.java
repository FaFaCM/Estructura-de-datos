public class Insercion_al_final {
    public static void main(String[] args) {
        int[] arreglo = new int[10];
        arreglo[0] = 10;
        arreglo[1] = 20;
        arreglo[2] = 30;
        int n = 3;
        int valor = 40;

        arreglo[n] = valor;
        n++;

        for (int i = 0; i < n; i++)
            System.out.print(arreglo[i] + " ");
    }
}