/*
 * Banco de pruebas de algoritmos de ordenamiento - JAVA
 *
 * Compilar y ejecutar (el archivo debe llamarse AlgoritmosJava.java):
 *   javac AlgoritmosJava.java
 *   java AlgoritmosJava                      (lee los txt de CARPETA_DATOS, SIN limite de tiempo)
 *   java AlgoritmosJava --rapido             (solo tamanos 100 y 1000)
 *   java AlgoritmosJava --limite=300         (opcional: cancela las pruebas que pasen de 300 s -> TIMEOUT)
 *   java AlgoritmosJava --datos=RUTA         (otra carpeta con los txt)
 *   java AlgoritmosJava --tamanos=100,1000   (solo esos tamanos)
 *
 * Cada algoritmo ordena in-place un int[] y devuelve {comparaciones, intercambios}.
 * Definicion de "intercambios" (igual que en Python y C++):
 *   - Burbuja, Seleccion, Quicksort, Heapsort: intercambios reales de 2 elementos.
 *   - Insercion, Shell, Merge, Bucket, Radix: movimientos/escrituras de elementos.
 *   - Radix no compara elementos entre si (comparaciones = 0).
 *
 * Java compila a bytecode y el JIT optimiza mientras corre, asi que antes de medir se hace un
 * calentamiento (NO medido) de cada algoritmo con un arreglo pequeno.
 *
 * Por defecto NO hay limite de tiempo. Con --limite=SEG los algoritmos revisan el reloj una vez cada 256
 * vueltas de su bucle exterior (costo despreciable) y una prueba que pase del limite se cancela y se
 * marca TIMEOUT. El CSV se escribe fila por fila (no se pierde nada si se interrumpe el programa).
 */
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.Set;

public class AlgoritmosJava {

    // ==================================================================
    //  CONTROL DE TIEMPO LIMITE
    // ==================================================================
    static final class Timeout extends RuntimeException {
        Timeout() { super(null, null, false, false); }  // sin stack trace: barato de lanzar
    }

    static long limiteNs;
    static int tick;

    static void chequear() {
        if ((++tick & 255) == 0 && System.nanoTime() - limiteNs > 0) throw new Timeout();
    }

    // ==================================================================
    //  ALGORITMOS  (devuelven {comparaciones, intercambios})
    // ==================================================================

    static long[] burbuja(int[] a) {
        long cc = 0, ss = 0;
        int n = a.length;
        for (int i = 0; i < n - 1; i++) {
            chequear();
            for (int j = 0; j < n - 1 - i; j++) {
                cc++;
                if (a[j] > a[j + 1]) {
                    int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                    ss++;
                }
            }
        }
        return new long[]{cc, ss};
    }

    static long[] insercion(int[] a) {
        long cc = 0, ss = 0;
        int n = a.length;
        for (int i = 1; i < n; i++) {
            chequear();
            int actual = a[i];
            int j = i - 1;
            while (j >= 0) {
                cc++;
                if (a[j] > actual) {
                    a[j + 1] = a[j];
                    ss++;
                    j--;
                } else {
                    break;
                }
            }
            if (j + 1 != i) {
                a[j + 1] = actual;
                ss++;
            }
        }
        return new long[]{cc, ss};
    }

    static long[] seleccion(int[] a) {
        long cc = 0, ss = 0;
        int n = a.length;
        for (int i = 0; i < n - 1; i++) {
            chequear();
            int menor = i;
            for (int j = i + 1; j < n; j++) {
                cc++;
                if (a[j] < a[menor]) menor = j;
            }
            if (menor != i) {
                int t = a[i]; a[i] = a[menor]; a[menor] = t;
                ss++;
            }
        }
        return new long[]{cc, ss};
    }

    // Lomuto, pivote = ultimo elemento. Iterativo (pila explicita) para no desbordar la pila de
    // llamadas con datos ordenados/inversos (la recursion llegaria a 1,000,000 de niveles).
    static long[] quicksort(int[] a) {
        long cc = 0, ss = 0;
        int[] pilaI = new int[64];
        int[] pilaF = new int[64];
        int tope = 0;
        if (a.length > 1) {
            pilaI[0] = 0;
            pilaF[0] = a.length - 1;
            tope = 1;
        }
        while (tope > 0) {
            chequear();
            tope--;
            int inicio = pilaI[tope], fin = pilaF[tope];
            int pivote = a[fin];
            int i = inicio - 1;
            for (int j = inicio; j < fin; j++) {
                cc++;
                if (a[j] <= pivote) {
                    i++;
                    int t = a[i]; a[i] = a[j]; a[j] = t;
                    ss++;
                }
            }
            int t = a[i + 1]; a[i + 1] = a[fin]; a[fin] = t;
            ss++;
            int p = i + 1;
            if (tope + 2 > pilaI.length) {
                pilaI = Arrays.copyOf(pilaI, pilaI.length * 2);
                pilaF = Arrays.copyOf(pilaF, pilaF.length * 2);
            }
            if (inicio < p - 1) { pilaI[tope] = inicio; pilaF[tope] = p - 1; tope++; }
            if (p + 1 < fin)    { pilaI[tope] = p + 1;  pilaF[tope] = fin;   tope++; }
        }
        return new long[]{cc, ss};
    }

    static void heapify(int[] a, int n, int i, long[] ct) {
        long cc = ct[0], ss = ct[1];
        while (true) {
            int mayor = i;
            int izq = 2 * i + 1;
            int der = 2 * i + 2;
            if (izq < n) {
                cc++;
                if (a[izq] > a[mayor]) mayor = izq;
            }
            if (der < n) {
                cc++;
                if (a[der] > a[mayor]) mayor = der;
            }
            if (mayor == i) break;
            int t = a[i]; a[i] = a[mayor]; a[mayor] = t;
            ss++;
            i = mayor;
        }
        ct[0] = cc; ct[1] = ss;
    }

    static long[] heapsort(int[] a) {
        long[] ct = new long[2];
        int n = a.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            chequear();
            heapify(a, n, i, ct);
        }
        for (int i = n - 1; i > 0; i--) {
            chequear();
            int t = a[0]; a[0] = a[i]; a[i] = t;
            ct[1]++;
            heapify(a, i, 0, ct);
        }
        return ct;
    }

    static void merge(int[] a, int l, int m, int r, long[] ct) {
        chequear();
        int[] L = Arrays.copyOfRange(a, l, m + 1);
        int[] R = Arrays.copyOfRange(a, m + 1, r + 1);
        int n1 = L.length, n2 = R.length;
        int i = 0, j = 0, k = l;
        long cc = 0, ss = 0;
        while (i < n1 && j < n2) {
            cc++;
            if (L[i] <= R[j]) {
                a[k] = L[i];
                i++;
            } else {
                a[k] = R[j];
                j++;
            }
            ss++;
            k++;
        }
        while (i < n1) { a[k] = L[i]; i++; k++; ss++; }
        while (j < n2) { a[k] = R[j]; j++; k++; ss++; }
        ct[0] += cc; ct[1] += ss;
    }

    static void mergesortRec(int[] a, int l, int r, long[] ct) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergesortRec(a, l, m, ct);
            mergesortRec(a, m + 1, r, ct);
            merge(a, l, m, r, ct);
        }
    }

    static long[] mergesort(int[] a) {
        long[] ct = new long[2];
        mergesortRec(a, 0, a.length - 1, ct);
        return ct;
    }

    static long[] shellsort(int[] a) {
        long cc = 0, ss = 0;
        int n = a.length;
        for (int gap = n / 2; gap > 0; gap /= 2) {
            for (int j = gap; j < n; j++) {
                chequear();
                int val = a[j];
                int k = j;
                while (k >= gap) {
                    cc++;
                    if (a[k - gap] > val) {
                        a[k] = a[k - gap];
                        ss++;
                        k -= gap;
                    } else {
                        break;
                    }
                }
                if (k != j) {
                    a[k] = val;
                    ss++;
                }
            }
        }
        return new long[]{cc, ss};
    }

    // Datos enteros >= 0: se normalizan a [0,1) con (x-min)/(max-min+1) para repartir en n cubetas.
    // Cada cubeta es un int[] que crece al doble cuando se llena (equivalente a vector/lista).
    static long[] bucketsort(int[] a) {
        long cc = 0, ss = 0;
        int n = a.length;
        if (n < 2) return new long[]{0, 0};
        int mn = a[0], mx = a[0];
        for (int x : a) { if (x < mn) mn = x; if (x > mx) mx = x; }
        long rango = (long) mx - mn + 1;
        int[][] cub = new int[n][];
        int[] tam = new int[n];
        for (int x : a) {
            chequear();
            int b = (int) (((long) n * ((long) x - mn)) / rango);
            if (cub[b] == null) {
                cub[b] = new int[2];
            } else if (tam[b] == cub[b].length) {
                cub[b] = Arrays.copyOf(cub[b], tam[b] * 2);
            }
            cub[b][tam[b]++] = x;
            ss++;
        }
        for (int b = 0; b < n; b++) {
            chequear();
            int[] v = cub[b];
            int m = tam[b];
            for (int i = 1; i < m; i++) {
                int val = v[i];
                int k = i - 1;
                while (k >= 0) {
                    cc++;
                    if (v[k] > val) {
                        v[k + 1] = v[k];
                        ss++;
                        k--;
                    } else {
                        break;
                    }
                }
                if (k + 1 != i) {
                    v[k + 1] = val;
                    ss++;
                }
            }
        }
        int idx = 0;
        for (int b = 0; b < n; b++) {
            chequear();
            for (int i = 0; i < tam[b]; i++) {
                a[idx++] = cub[b][i];
                ss++;
            }
        }
        return new long[]{cc, ss};
    }

    // LSD base 10, solo enteros >= 0. No compara elementos entre si.
    static long[] radixsort(int[] a) {
        long ss = 0;
        int n = a.length;
        if (n == 0) return new long[]{0, 0};
        int maxVal = a[0];
        for (int x : a) if (x > maxVal) maxVal = x;
        int[] salida = new int[n];
        for (long exp = 1; maxVal / exp > 0; exp *= 10) {
            chequear();
            int[] cuenta = new int[10];
            for (int i = 0; i < n; i++) cuenta[(int) ((a[i] / exp) % 10)]++;
            for (int i = 1; i < 10; i++) cuenta[i] += cuenta[i - 1];
            for (int i = n - 1; i >= 0; i--) {
                int d = (int) ((a[i] / exp) % 10);
                cuenta[d]--;
                salida[cuenta[d]] = a[i];
                ss++;
            }
            System.arraycopy(salida, 0, a, 0, n);  // copia de vuelta (no se cuenta, igual que en Python/C++)
        }
        return new long[]{0, ss};
    }

    interface Algoritmo { long[] ejecutar(int[] a); }

    static final String[] NOMBRES = {
        "Burbuja", "Insercion", "Seleccion", "Quicksort", "Heapsort",
        "Mergesort", "Shellsort", "Bucketsort", "Radixsort"
    };
    static final Algoritmo[] FUNCIONES = {
        AlgoritmosJava::burbuja, AlgoritmosJava::insercion, AlgoritmosJava::seleccion,
        AlgoritmosJava::quicksort, AlgoritmosJava::heapsort, AlgoritmosJava::mergesort,
        AlgoritmosJava::shellsort, AlgoritmosJava::bucketsort, AlgoritmosJava::radixsort
    };

    // ==================================================================
    //  CONFIGURACION DE LA PRUEBA
    // ==================================================================
    static final int[] TAMANOS = {100, 1000, 10000, 100000, 1000000};
    static final String[] CASOS = {"aleatorio", "ordenado", "inverso"};
    static final String CARPETA_DATOS = "arreglos_txt";  // --datos=RUTA para cambiarla
    static final double LIMITE_TIEMPO_S = 0;  // 0 = SIN LIMITE (cada prueba corre hasta terminar). --limite=SEG para cancelar las lentas
    static final String ARCHIVO_CSV = "resultados_java.txt";

    // Hardware de la maquina donde se corre la prueba (se escribe en el encabezado del CSV)
    static final String HW_PROCESADOR = "AMD Ryzen 5 7535HS (3.30 GHz)";
    static final String HW_RAM = "16 GB";
    static final String HW_GRAFICA = "NVIDIA GeForce RTX 4050 Laptop GPU (6 GB)";

    static int[] cargar(int n, String caso, String carpeta) throws IOException {
        Path ruta = Paths.get(carpeta, caso + "_" + n + ".txt");
        byte[] bytes = Files.readAllBytes(ruta);
        int[] out = new int[n];
        int cuenta = 0;
        long v = 0;
        boolean enNumero = false;
        for (byte b : bytes) {
            if (b >= '0' && b <= '9') {
                v = v * 10 + (b - '0');
                enNumero = true;
            } else if (enNumero) {
                if (cuenta < n) out[cuenta] = (int) v;
                cuenta++;
                v = 0;
                enNumero = false;
            }
        }
        if (enNumero) {
            if (cuenta < n) out[cuenta] = (int) v;
            cuenta++;
        }
        if (cuenta != n) throw new IOException(ruta + ": se esperaban " + n + " datos y hay " + cuenta);
        return out;
    }

    static void guardar(BufferedWriter w, String[] fila) throws IOException {
        w.write(String.join(",", fila) + "\n");
        w.flush();
    }

    static void calentar() {
        // Calentamiento del JIT: NO se mide. Ejecuta cada algoritmo varias veces con 2000 datos.
        Random rnd = new Random(1);
        int[] base = new int[2000];
        for (int i = 0; i < base.length; i++) base[i] = rnd.nextInt(2001);
        limiteNs = System.nanoTime() + 60_000_000_000L;
        for (int rep = 0; rep < 20; rep++) {
            for (Algoritmo f : FUNCIONES) f.ejecutar(base.clone());
        }
    }

    public static void main(String[] args) throws Exception {
        String carpeta = CARPETA_DATOS;
        double limite = LIMITE_TIEMPO_S;
        int[] tamanos = TAMANOS;
        for (String arg : args) {
            if (arg.startsWith("--datos=")) {
                carpeta = arg.substring(8);
            } else if (arg.startsWith("--limite=")) {
                limite = Double.parseDouble(arg.substring(9));
            } else if (arg.startsWith("--tamanos=")) {
                String[] partes = arg.substring(10).split(",");
                tamanos = new int[partes.length];
                for (int i = 0; i < partes.length; i++) tamanos[i] = Integer.parseInt(partes[i].trim());
            } else if (arg.equals("--rapido")) {
                tamanos = new int[]{100, 1000};
            }
        }

        String jvm = System.getProperty("java.vm.name") + " " + System.getProperty("java.version");
        String sistema = System.getProperty("os.name") + " " + System.getProperty("os.version");
        System.out.println("Hardware: " + HW_PROCESADOR + " | " + HW_RAM + " | " + HW_GRAFICA);
        System.out.println("Java: " + jvm + " | Sistema: " + sistema);
        System.out.println("Limite de tiempo por prueba: " + (limite > 0 ? limite + " s" : "SIN LIMITE"));
        System.out.println("Calentando JIT...");
        calentar();

        String txtLimite = limite > 0 ? String.valueOf(limite) : "sin_limite";
        // El CSV se escribe fila por fila: si se interrumpe el programa (Ctrl+C) no se pierde lo ya medido.
        BufferedWriter w = Files.newBufferedWriter(Paths.get(ARCHIVO_CSV), StandardCharsets.UTF_8);
        w.write("# lenguaje,Java\n");
        w.write("# jvm," + jvm + "\n");
        w.write("# sistema," + sistema + "\n");
        w.write("# procesador," + HW_PROCESADOR + "\n");
        w.write("# ram," + HW_RAM + "\n");
        w.write("# grafica," + HW_GRAFICA + "\n");
        w.write("# limite_tiempo_s," + txtLimite + "\n");
        w.write("algoritmo,n,caso,estado,tiempo_s,comparaciones,intercambios\n");
        w.flush();
        Set<String> agotados = new HashSet<>();  // "algoritmo|caso" que ya hizo timeout con un n menor

        for (int n : tamanos) {
            for (String caso : CASOS) {
                int[] datos = null;
                int[] esperado = null;
                for (int k = 0; k < NOMBRES.length; k++) {
                    String nombre = NOMBRES[k];
                    String etiqueta = String.format(Locale.ROOT, "%-11s n=%-9d %-10s", nombre, n, caso);
                    String clave = nombre + "|" + caso;

                    if (agotados.contains(clave)) {
                        guardar(w, new String[]{nombre, "" + n, caso, "TIMEOUT", "", "", ""});
                        System.out.println(etiqueta + " TIMEOUT (inferido: ya agoto el limite con un n menor)");
                        continue;
                    }
                    if (datos == null) {
                        datos = cargar(n, caso, carpeta);
                        esperado = datos.clone();
                        Arrays.sort(esperado);
                    }
                    int[] copia = datos.clone();
                    System.gc();  // fuera del tiempo medido, para empezar con el heap limpio
                    tick = 0;
                    boolean agoto = false;
                    long[] r = null;
                    double t = 0;
                    try {
                        long t0 = System.nanoTime();
                        limiteNs = (limite > 0) ? t0 + (long) (limite * 1e9) : t0 + (Long.MAX_VALUE >> 1);  // sin limite: ~146 anios
                        r = FUNCIONES[k].ejecutar(copia);
                        long t1 = System.nanoTime();
                        t = (t1 - t0) / 1e9;
                    } catch (Timeout e) {
                        agoto = true;
                    }
                    if (agoto) {
                        agotados.add(clave);
                        guardar(w, new String[]{nombre, "" + n, caso, "TIMEOUT", "", "", ""});
                        System.out.println(etiqueta + " TIMEOUT (> " + limite + " s)");
                    } else if (!Arrays.equals(copia, esperado)) {
                        guardar(w, new String[]{nombre, "" + n, caso, "ERROR", "", "", ""});
                        System.out.println(etiqueta + " ERROR: no ordeno correctamente");
                    } else {
                        guardar(w, new String[]{nombre, "" + n, caso, "OK",
                            String.format(Locale.ROOT, "%.6f", t), "" + r[0], "" + r[1]});
                        System.out.println(String.format(Locale.ROOT, "%s %10.4fs  comp=%-14d interc=%d",
                            etiqueta, t, r[0], r[1]));
                    }
                }
            }
        }

        w.close();
        System.out.println("Resultados guardados en " + ARCHIVO_CSV);
    }
}
