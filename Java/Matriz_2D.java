public class Matriz_2D {
    public static void main(String[] args) {
        int[][] matriz2D = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        for (int[] fila : matriz2D)
            for (int elemento : fila)
                System.out.print(elemento + " ");
        System.out.println();
    }
}
