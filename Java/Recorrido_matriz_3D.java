public class Recorrido_matriz_3D {
    public static void main(String[] args) {
        int[][][] matriz3D = {
            {{1, 2}, {3, 4}},
            {{5, 6}, {7, 8}}
        };

        for (int[][] capa : matriz3D)
            for (int[] fila : capa)
                for (int elemento : fila)
                    System.out.print(elemento + " ");
        System.out.println();
    }
}
