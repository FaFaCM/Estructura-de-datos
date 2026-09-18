public class Orden_columnas_2D {
    public static void main(String[] args) {
        int[][] matriz2D = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        for (int j = 0; j < matriz2D[0].length; j++)
            for (int i = 0; i < matriz2D.length; i++)
                System.out.print(matriz2D[i][j] + " ");
        System.out.println();
    }
}
