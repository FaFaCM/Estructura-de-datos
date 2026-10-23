/*
 * Banco de pruebas de algoritmos de ordenamiento - C# (.NET)
 *
 * Poner Program.cs y AlgoritmosCs.csproj JUNTOS en una carpeta propia y, desde ahi:
 *   dotnet run -c Release                              (lee los txt de CARPETA_DATOS, SIN limite de tiempo)
 *   dotnet run -c Release -- --rapido                  (solo tamanos 100 y 1000)
 *   dotnet run -c Release -- --limite=300              (opcional: cancela las pruebas que pasen de 300 s -> TIMEOUT)
 *   dotnet run -c Release -- --datos=RUTA              (otra carpeta con los txt)
 *   dotnet run -c Release -- --tamanos=100,1000        (solo esos tamanos)
 * IMPORTANTE: usar siempre -c Release (en Debug los tiempos no son representativos).
 *
 * Cada algoritmo ordena in-place un int[] y devuelve {comparaciones, intercambios}.
 * Definicion de "intercambios" (igual que en Python, C++, Java y JavaScript):
 *   - Burbuja, Seleccion, Quicksort, Heapsort: intercambios reales de 2 elementos.
 *   - Insercion, Shell, Merge, Bucket, Radix: movimientos/escrituras de elementos.
 *   - Radix no compara elementos entre si (comparaciones = 0).
 *
 * .NET compila con JIT mientras corre, asi que antes de medir se hace un calentamiento
 * (NO medido) de cada algoritmo con un arreglo pequeno.
 *
 * Por defecto NO hay limite de tiempo. Con --limite=SEG los algoritmos revisan el reloj una vez cada 256
 * vueltas de su bucle exterior (costo despreciable) y una prueba que pase del limite se cancela y se
 * marca TIMEOUT. El CSV se escribe fila por fila (no se pierde nada si se interrumpe el programa).
 */
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Text;

static class Program
{
    // ==================================================================
    //  CONTROL DE TIEMPO LIMITE
    // ==================================================================
    sealed class LimiteExcedido : Exception { }

    static long limiteTicks;
    static int tick;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    static void Chequear()
    {
        if ((++tick & 255) == 0 && Stopwatch.GetTimestamp() > limiteTicks) throw new LimiteExcedido();
    }

    // ==================================================================
    //  ALGORITMOS  (devuelven {comparaciones, intercambios})
    // ==================================================================

    static long[] Burbuja(int[] a)
    {
        long cc = 0, ss = 0;
        int n = a.Length;
        for (int i = 0; i < n - 1; i++)
        {
            Chequear();
            for (int j = 0; j < n - 1 - i; j++)
            {
                cc++;
                if (a[j] > a[j + 1])
                {
                    int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                    ss++;
                }
            }
        }
        return new long[] { cc, ss };
    }

    static long[] Insercion(int[] a)
    {
        long cc = 0, ss = 0;
        int n = a.Length;
        for (int i = 1; i < n; i++)
        {
            Chequear();
            int actual = a[i];
            int j = i - 1;
            while (j >= 0)
            {
                cc++;
                if (a[j] > actual)
                {
                    a[j + 1] = a[j];
                    ss++;
                    j--;
                }
                else break;
            }
            if (j + 1 != i)
            {
                a[j + 1] = actual;
                ss++;
            }
        }
        return new long[] { cc, ss };
    }

    static long[] Seleccion(int[] a)
    {
        long cc = 0, ss = 0;
        int n = a.Length;
        for (int i = 0; i < n - 1; i++)
        {
            Chequear();
            int menor = i;
            for (int j = i + 1; j < n; j++)
            {
                cc++;
                if (a[j] < a[menor]) menor = j;
            }
            if (menor != i)
            {
                int t = a[i]; a[i] = a[menor]; a[menor] = t;
                ss++;
            }
        }
        return new long[] { cc, ss };
    }

    // Lomuto, pivote = ultimo elemento. Iterativo (pila explicita) para no desbordar la pila de
    // llamadas con datos ordenados/inversos (la recursion llegaria a 1,000,000 de niveles).
    static long[] Quicksort(int[] a)
    {
        long cc = 0, ss = 0;
        int[] pilaI = new int[64];
        int[] pilaF = new int[64];
        int tope = 0;
        if (a.Length > 1)
        {
            pilaI[0] = 0;
            pilaF[0] = a.Length - 1;
            tope = 1;
        }
        while (tope > 0)
        {
            Chequear();
            tope--;
            int inicio = pilaI[tope], fin = pilaF[tope];
            int pivote = a[fin];
            int i = inicio - 1;
            for (int j = inicio; j < fin; j++)
            {
                cc++;
                if (a[j] <= pivote)
                {
                    i++;
                    int t1 = a[i]; a[i] = a[j]; a[j] = t1;
                    ss++;
                }
            }
            int t = a[i + 1]; a[i + 1] = a[fin]; a[fin] = t;
            ss++;
            int p = i + 1;
            if (tope + 2 > pilaI.Length)
            {
                Array.Resize(ref pilaI, pilaI.Length * 2);
                Array.Resize(ref pilaF, pilaF.Length * 2);
            }
            if (inicio < p - 1) { pilaI[tope] = inicio; pilaF[tope] = p - 1; tope++; }
            if (p + 1 < fin) { pilaI[tope] = p + 1; pilaF[tope] = fin; tope++; }
        }
        return new long[] { cc, ss };
    }

    static void Heapify(int[] a, int n, int i, ref long cc, ref long ss)
    {
        while (true)
        {
            int mayor = i;
            int izq = 2 * i + 1;
            int der = 2 * i + 2;
            if (izq < n)
            {
                cc++;
                if (a[izq] > a[mayor]) mayor = izq;
            }
            if (der < n)
            {
                cc++;
                if (a[der] > a[mayor]) mayor = der;
            }
            if (mayor == i) return;
            int t = a[i]; a[i] = a[mayor]; a[mayor] = t;
            ss++;
            i = mayor;
        }
    }

    static long[] Heapsort(int[] a)
    {
        long cc = 0, ss = 0;
        int n = a.Length;
        for (int i = n / 2 - 1; i >= 0; i--)
        {
            Chequear();
            Heapify(a, n, i, ref cc, ref ss);
        }
        for (int i = n - 1; i > 0; i--)
        {
            Chequear();
            int t = a[0]; a[0] = a[i]; a[i] = t;
            ss++;
            Heapify(a, i, 0, ref cc, ref ss);
        }
        return new long[] { cc, ss };
    }

    static void Merge(int[] a, int l, int m, int r, long[] ct)
    {
        Chequear();
        int n1 = m - l + 1, n2 = r - m;
        int[] L = new int[n1];
        int[] R = new int[n2];
        Array.Copy(a, l, L, 0, n1);
        Array.Copy(a, m + 1, R, 0, n2);
        int i = 0, j = 0, k = l;
        long cc = 0, ss = 0;
        while (i < n1 && j < n2)
        {
            cc++;
            if (L[i] <= R[j]) { a[k] = L[i]; i++; }
            else { a[k] = R[j]; j++; }
            ss++;
            k++;
        }
        while (i < n1) { a[k] = L[i]; i++; k++; ss++; }
        while (j < n2) { a[k] = R[j]; j++; k++; ss++; }
        ct[0] += cc; ct[1] += ss;
    }

    static void MergesortRec(int[] a, int l, int r, long[] ct)
    {
        if (l < r)
        {
            int m = l + (r - l) / 2;
            MergesortRec(a, l, m, ct);
            MergesortRec(a, m + 1, r, ct);
            Merge(a, l, m, r, ct);
        }
    }

    static long[] Mergesort(int[] a)
    {
        long[] ct = new long[2];
        MergesortRec(a, 0, a.Length - 1, ct);
        return ct;
    }

    static long[] Shellsort(int[] a)
    {
        long cc = 0, ss = 0;
        int n = a.Length;
        for (int gap = n / 2; gap > 0; gap /= 2)
        {
            for (int j = gap; j < n; j++)
            {
                Chequear();
                int val = a[j];
                int k = j;
                while (k >= gap)
                {
                    cc++;
                    if (a[k - gap] > val)
                    {
                        a[k] = a[k - gap];
                        ss++;
                        k -= gap;
                    }
                    else break;
                }
                if (k != j)
                {
                    a[k] = val;
                    ss++;
                }
            }
        }
        return new long[] { cc, ss };
    }

    // Datos enteros >= 0: se normalizan a [0,1) con (x-min)/(max-min+1) para repartir en n cubetas.
    // Cada cubeta es un int[] que crece al doble cuando se llena (equivalente a vector/lista).
    static long[] Bucketsort(int[] a)
    {
        long cc = 0, ss = 0;
        int n = a.Length;
        if (n < 2) return new long[] { 0, 0 };
        int mn = a[0], mx = a[0];
        foreach (int x in a) { if (x < mn) mn = x; if (x > mx) mx = x; }
        long rango = (long)mx - mn + 1;
        int[][] cub = new int[n][];
        int[] tam = new int[n];
        foreach (int x in a)
        {
            Chequear();
            int b = (int)(((long)n * ((long)x - mn)) / rango);
            if (cub[b] == null) cub[b] = new int[2];
            else if (tam[b] == cub[b].Length) Array.Resize(ref cub[b], tam[b] * 2);
            cub[b][tam[b]++] = x;
            ss++;
        }
        for (int b = 0; b < n; b++)
        {
            Chequear();
            int[] v = cub[b];
            int m = tam[b];
            for (int i = 1; i < m; i++)
            {
                int val = v[i];
                int k = i - 1;
                while (k >= 0)
                {
                    cc++;
                    if (v[k] > val)
                    {
                        v[k + 1] = v[k];
                        ss++;
                        k--;
                    }
                    else break;
                }
                if (k + 1 != i)
                {
                    v[k + 1] = val;
                    ss++;
                }
            }
        }
        int idx = 0;
        for (int b = 0; b < n; b++)
        {
            Chequear();
            for (int i = 0; i < tam[b]; i++)
            {
                a[idx++] = cub[b][i];
                ss++;
            }
        }
        return new long[] { cc, ss };
    }

    // LSD base 10, solo enteros >= 0. No compara elementos entre si.
    static long[] Radixsort(int[] a)
    {
        long ss = 0;
        int n = a.Length;
        if (n == 0) return new long[] { 0, 0 };
        int maxVal = a[0];
        foreach (int x in a) if (x > maxVal) maxVal = x;
        int[] salida = new int[n];
        for (long exp = 1; maxVal / exp > 0; exp *= 10)
        {
            Chequear();
            int[] cuenta = new int[10];
            for (int i = 0; i < n; i++) cuenta[(int)((a[i] / exp) % 10)]++;
            for (int i = 1; i < 10; i++) cuenta[i] += cuenta[i - 1];
            for (int i = n - 1; i >= 0; i--)
            {
                int d = (int)((a[i] / exp) % 10);
                cuenta[d]--;
                salida[cuenta[d]] = a[i];
                ss++;
            }
            Array.Copy(salida, a, n);  // copia de vuelta (no se cuenta, igual que en los otros lenguajes)
        }
        return new long[] { 0, ss };
    }

    static readonly (string Nombre, Func<int[], long[]> Fn)[] ALGORITMOS =
    {
        ("Burbuja", Burbuja),
        ("Insercion", Insercion),
        ("Seleccion", Seleccion),
        ("Quicksort", Quicksort),
        ("Heapsort", Heapsort),
        ("Mergesort", Mergesort),
        ("Shellsort", Shellsort),
        ("Bucketsort", Bucketsort),
        ("Radixsort", Radixsort),
    };

    // ==================================================================
    //  CONFIGURACION DE LA PRUEBA
    // ==================================================================
    static readonly int[] TAMANOS = { 100, 1000, 10000, 100000, 1000000 };
    static readonly string[] CASOS = { "aleatorio", "ordenado", "inverso" };
    const string CARPETA_DATOS = @"arreglos_txt";  // --datos=RUTA para cambiarla
    const double LIMITE_TIEMPO_S = 0;  // 0 = SIN LIMITE (cada prueba corre hasta terminar). --limite=SEG para cancelar las lentas
    const string ARCHIVO_CSV = "resultados_cs.txt";

    // Hardware de la maquina donde se corre la prueba (se escribe en el encabezado del CSV)
    const string HW_PROCESADOR = "AMD Ryzen 5 7535HS (3.30 GHz)";
    const string HW_RAM = "16 GB";
    const string HW_GRAFICA = "NVIDIA GeForce RTX 4050 Laptop GPU (6 GB)";

    static int[] Cargar(int n, string caso, string carpeta)
    {
        string ruta = Path.Combine(carpeta, caso + "_" + n + ".txt");
        byte[] bytes = File.ReadAllBytes(ruta);
        int[] outp = new int[n];
        int cuenta = 0;
        long v = 0;
        bool enNumero = false;
        foreach (byte b in bytes)
        {
            if (b >= (byte)'0' && b <= (byte)'9')
            {
                v = v * 10 + (b - '0');
                enNumero = true;
            }
            else if (enNumero)
            {
                if (cuenta < n) outp[cuenta] = (int)v;
                cuenta++;
                v = 0;
                enNumero = false;
            }
        }
        if (enNumero)
        {
            if (cuenta < n) outp[cuenta] = (int)v;
            cuenta++;
        }
        if (cuenta != n) throw new IOException(ruta + ": se esperaban " + n + " datos y hay " + cuenta);
        return outp;
    }

    static void Calentar()
    {
        // Calentamiento del JIT: NO se mide. Ejecuta cada algoritmo varias veces con 2000 datos.
        int[] baseArr = new int[2000];
        uint semilla = 12345;
        for (int i = 0; i < baseArr.Length; i++)
        {
            semilla = semilla * 1103515245u + 12345u;
            baseArr[i] = (int)((semilla >> 8) % 2001);
        }
        limiteTicks = Stopwatch.GetTimestamp() + 60 * Stopwatch.Frequency;
        for (int rep = 0; rep < 20; rep++)
            foreach (var alg in ALGORITMOS) alg.Fn((int[])baseArr.Clone());
    }

    static string F(double d) => d.ToString("F6", CultureInfo.InvariantCulture);

    static int Main(string[] args)
    {
        string carpeta = CARPETA_DATOS;
        double limite = LIMITE_TIEMPO_S;
        int[] tamanos = TAMANOS;
        foreach (string arg in args)
        {
            if (arg.StartsWith("--datos=")) carpeta = arg.Substring(8);
            else if (arg.StartsWith("--limite="))
                limite = double.Parse(arg.Substring(9), CultureInfo.InvariantCulture);
            else if (arg.StartsWith("--tamanos="))
                tamanos = Array.ConvertAll(arg.Substring(10).Split(','), s => int.Parse(s.Trim()));
            else if (arg == "--rapido") tamanos = new[] { 100, 1000 };
        }

        string runtime = RuntimeInformation.FrameworkDescription;
        string sistema = RuntimeInformation.OSDescription;
        var inv = CultureInfo.InvariantCulture;
        Console.WriteLine("Hardware: " + HW_PROCESADOR + " | " + HW_RAM + " | " + HW_GRAFICA);
        Console.WriteLine("Runtime: " + runtime + " | Sistema: " + sistema);
        Console.WriteLine("Limite de tiempo por prueba: " + (limite > 0 ? limite.ToString(inv) + " s" : "SIN LIMITE"));
#if DEBUG
        Console.Error.WriteLine("AVISO: compilado en Debug. Usa 'dotnet run -c Release' para tiempos representativos.");
#endif
        Console.WriteLine("Calentando JIT...");
        Calentar();

        // El CSV se escribe fila por fila: si se interrumpe el programa (Ctrl+C) no se pierde lo ya medido.
        string txtLimite = limite > 0 ? limite.ToString(inv) : "sin_limite";
        var csv = new StreamWriter(ARCHIVO_CSV, false, new UTF8Encoding(false)) { AutoFlush = true, NewLine = "\n" };
        csv.WriteLine("# lenguaje,C#");
        csv.WriteLine("# runtime," + runtime);
        csv.WriteLine("# sistema," + sistema);
        csv.WriteLine("# procesador," + HW_PROCESADOR);
        csv.WriteLine("# ram," + HW_RAM);
        csv.WriteLine("# grafica," + HW_GRAFICA);
        csv.WriteLine("# limite_tiempo_s," + txtLimite);
        csv.WriteLine("algoritmo,n,caso,estado,tiempo_s,comparaciones,intercambios");
        var agotados = new HashSet<string>();  // "algoritmo|caso" que ya hizo timeout con un n menor

        foreach (int n in tamanos)
        {
            foreach (string caso in CASOS)
            {
                int[] datos = null, esperado = null;
                foreach (var alg in ALGORITMOS)
                {
                    string etiqueta = alg.Nombre.PadRight(11) + " n=" + n.ToString().PadRight(9) + " " + caso.PadRight(10);
                    string clave = alg.Nombre + "|" + caso;

                    if (agotados.Contains(clave))
                    {
                        csv.WriteLine(string.Join(",", new[] { alg.Nombre, n.ToString(), caso, "TIMEOUT", "", "", "" }));
                        Console.WriteLine(etiqueta + " TIMEOUT (inferido: ya agoto el limite con un n menor)");
                        continue;
                    }
                    if (datos == null)
                    {
                        datos = Cargar(n, caso, carpeta);
                        esperado = (int[])datos.Clone();
                        Array.Sort(esperado);
                    }
                    int[] copia = (int[])datos.Clone();
                    GC.Collect();
                    GC.WaitForPendingFinalizers();  // fuera del tiempo medido
                    tick = 0;
                    bool agoto = false;
                    long[] r = null;
                    double t = 0;
                    try
                    {
                        long t0 = Stopwatch.GetTimestamp();
                        limiteTicks = limite > 0 ? t0 + (long)(limite * Stopwatch.Frequency) : long.MaxValue;
                        r = alg.Fn(copia);
                        long t1 = Stopwatch.GetTimestamp();
                        t = (double)(t1 - t0) / Stopwatch.Frequency;
                    }
                    catch (LimiteExcedido)
                    {
                        agoto = true;
                    }
                    if (agoto)
                    {
                        agotados.Add(clave);
                        csv.WriteLine(string.Join(",", new[] { alg.Nombre, n.ToString(), caso, "TIMEOUT", "", "", "" }));
                        Console.WriteLine(etiqueta + " TIMEOUT (> " + limite.ToString(inv) + " s)");
                    }
                    else if (!copia.AsSpan().SequenceEqual(esperado))
                    {
                        csv.WriteLine(string.Join(",", new[] { alg.Nombre, n.ToString(), caso, "ERROR", "", "", "" }));
                        Console.WriteLine(etiqueta + " ERROR: no ordeno correctamente");
                    }
                    else
                    {
                        csv.WriteLine(string.Join(",", new[] { alg.Nombre, n.ToString(), caso, "OK", F(t),
                                          r[0].ToString(inv), r[1].ToString(inv) }));
                        Console.WriteLine(etiqueta + " " + t.ToString("F4", inv).PadLeft(10) + "s  comp="
                                          + r[0].ToString(inv).PadRight(14) + " interc=" + r[1].ToString(inv));
                    }
                }
            }
        }

        csv.Close();
        Console.WriteLine("Resultados guardados en " + ARCHIVO_CSV);
        return 0;
    }
}
