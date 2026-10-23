"""
Banco de pruebas de algoritmos de ordenamiento - PYTHON
Cada algoritmo recibe una lista, la ordena in-place y devuelve (comparaciones, intercambios).

Definicion de "intercambios" (para que sea comparable entre algoritmos):
  - Burbuja, Seleccion, Quicksort, Heapsort: intercambios reales de 2 elementos.
  - Insercion, Shell, Merge, Bucket, Radix: movimientos/escrituras de elementos
    (no hacen swaps reales, se cuenta cada vez que un elemento se escribe en una posicion).
  - Radix no compara elementos entre si, por eso sus comparaciones son 0.
"""
import csv
import multiprocessing
import os
import platform
import sys
import time

# ======================================================================
#  ALGORITMOS
# ======================================================================

def burbuja(a):
    c = s = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            c += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                s += 1
    return c, s


def insercion(a):
    c = s = 0
    for i in range(1, len(a)):
        actual = a[i]
        j = i - 1
        while j >= 0:
            c += 1
            if a[j] > actual:
                a[j + 1] = a[j]
                s += 1
                j -= 1
            else:
                break
        if j + 1 != i:
            a[j + 1] = actual
            s += 1
    return c, s


def seleccion(a):
    c = s = 0
    n = len(a)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            c += 1
            if a[j] < a[menor]:
                menor = j
        if menor != i:
            a[i], a[menor] = a[menor], a[i]
            s += 1
    return c, s


def quicksort(a):
    """Lomuto, pivote = ultimo elemento (como el original).
    Version iterativa (pila explicita) para evitar RecursionError en arreglos ordenados."""
    c = s = 0
    pila = [(0, len(a) - 1)]
    while pila:
        inicio, fin = pila.pop()
        if inicio >= fin:
            continue
        pivote = a[fin]
        i = inicio - 1
        for j in range(inicio, fin):
            c += 1
            if a[j] <= pivote:
                i += 1
                a[i], a[j] = a[j], a[i]
                s += 1
        a[i + 1], a[fin] = a[fin], a[i + 1]
        s += 1
        p = i + 1
        pila.append((inicio, p - 1))
        pila.append((p + 1, fin))
    return c, s


def heapsort(a):
    c = s = 0
    n = len(a)

    def heapify(n, i):
        nonlocal c, s
        while True:
            mayor = i
            izq = 2 * i + 1
            der = 2 * i + 2
            if izq < n:
                c += 1
                if a[izq] > a[mayor]:
                    mayor = izq
            if der < n:
                c += 1
                if a[der] > a[mayor]:
                    mayor = der
            if mayor == i:
                return
            a[i], a[mayor] = a[mayor], a[i]
            s += 1
            i = mayor

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        s += 1
        heapify(i, 0)
    return c, s


def mergesort(a):
    c = s = 0

    def merge(l, m, r):
        nonlocal c, s
        L = a[l:m + 1]
        R = a[m + 1:r + 1]
        n1, n2 = len(L), len(R)
        i = j = 0
        k = l
        while i < n1 and j < n2:
            c += 1
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            s += 1
            k += 1
        while i < n1:
            a[k] = L[i]
            i += 1
            k += 1
            s += 1
        while j < n2:
            a[k] = R[j]
            j += 1
            k += 1
            s += 1

    def sort(l, r):
        if l < r:
            m = l + (r - l) // 2
            sort(l, m)
            sort(m + 1, r)
            merge(l, m, r)

    sort(0, len(a) - 1)
    return c, s


def shellsort(a):
    c = s = 0
    n = len(a)
    gap = n // 2
    while gap > 0:
        for j in range(gap, n):
            val = a[j]
            k = j
            while k >= gap:
                c += 1
                if a[k - gap] > val:
                    a[k] = a[k - gap]
                    s += 1
                    k -= gap
                else:
                    break
            if k != j:
                a[k] = val
                s += 1
        gap //= 2
    return c, s


def bucketsort(a):
    """Los datos son enteros >= 0, asi que se normalizan al rango [0,1) con (x-min)/(max-min+1)
    para poder usar el mismo reparto de cubetas del original (int(n * valor_normalizado))."""
    c = s = 0
    n = len(a)
    if n < 2:
        return c, s
    mn, mx = min(a), max(a)
    rango = mx - mn + 1
    cubetas = [[] for _ in range(n)]
    for x in a:
        cubetas[n * (x - mn) // rango].append(x)
        s += 1
    for b in cubetas:
        # insercion dentro de cada cubeta
        for i in range(1, len(b)):
            val = b[i]
            k = i - 1
            while k >= 0:
                c += 1
                if b[k] > val:
                    b[k + 1] = b[k]
                    s += 1
                    k -= 1
                else:
                    break
            if k + 1 != i:
                b[k + 1] = val
                s += 1
    idx = 0
    for b in cubetas:
        for x in b:
            a[idx] = x
            idx += 1
            s += 1
    return c, s


def radixsort(a):
    """LSD base 10, solo enteros >= 0. No compara elementos entre si (comparaciones = 0)."""
    c = s = 0
    if not a:
        return c, s
    n = len(a)
    max_val = max(a)
    exp = 1
    while max_val // exp > 0:
        salida = [0] * n
        cuenta = [0] * 10
        for x in a:
            cuenta[(x // exp) % 10] += 1
        for i in range(1, 10):
            cuenta[i] += cuenta[i - 1]
        for i in range(n - 1, -1, -1):
            d = (a[i] // exp) % 10
            cuenta[d] -= 1
            salida[cuenta[d]] = a[i]
            s += 1
        a[:] = salida
        exp *= 10
    return c, s


ALGORITMOS = {
    "Burbuja": burbuja,
    "Insercion": insercion,
    "Seleccion": seleccion,
    "Quicksort": quicksort,
    "Heapsort": heapsort,
    "Mergesort": mergesort,
    "Shellsort": shellsort,
    "Bucketsort": bucketsort,
    "Radixsort": radixsort,
}

# ======================================================================
#  CONFIGURACION DE LA PRUEBA
# ======================================================================
TAMANOS = [100, 1_000, 10_000, 100_000, 1_000_000]
CASOS = ["aleatorio", "ordenado", "inverso"]
CARPETA_DATOS = r"arreglos_txt"  # --datos=RUTA para cambiarla
# Limite de tiempo por prueba (segundos). None = SIN LIMITE: cada prueba corre hasta terminar de ordenar.
# Opcional: --limite=SEGUNDOS para cancelar (y marcar TIMEOUT) las pruebas que pasen de ese tiempo.
LIMITE_TIEMPO_S = None


def cargar(n, caso, carpeta):
    """Lee los datos desde <carpeta>/<caso>_<n>.txt (numeros separados por comas).
    Todos los lenguajes leen los MISMOS archivos, asi la comparacion es justa."""
    ruta = os.path.join(carpeta, f"{caso}_{n}.txt")
    with open(ruta, encoding="utf-8") as f:
        datos = [int(x) for x in f.read().strip().split(",")]
    if len(datos) != n:
        raise ValueError(f"{ruta}: se esperaban {n} datos y hay {len(datos)}")
    return datos


# Hardware de la maquina donde se corre la prueba (se escribe en el encabezado del CSV)
HARDWARE_MANUAL = {
    "procesador": "AMD Ryzen 5 7535HS (3.30 GHz)",
    "ram": "16 GB",
    "grafica": "NVIDIA GeForce RTX 4050 Laptop GPU (6 GB)",
}


def hardware():
    info = {
        "sistema": f"{platform.system()} {platform.release()}",
        "arquitectura": platform.machine(),
        "python": platform.python_version(),
        "nucleos_logicos": os.cpu_count(),
    }
    info.update(HARDWARE_MANUAL)
    return info


def _trabajador(nombre, n, caso, carpeta, conn):
    """Corre UNA prueba en un proceso aparte. El tiempo se mide solo alrededor del algoritmo
    (no incluye leer el txt ni verificar el resultado), y el proceso puede ser cancelado
    por el padre si pasa del limite, sin agregar ningun costo dentro de los algoritmos."""
    try:
        datos = cargar(n, caso, carpeta)
        esperado = sorted(datos)
        fn = ALGORITMOS[nombre]
        t0 = time.perf_counter()
        comp, interc = fn(datos)
        t = time.perf_counter() - t0
        if datos != esperado:
            conn.send(("ERROR", "el algoritmo no ordeno correctamente"))
        else:
            conn.send(("OK", t, comp, interc))
    except BaseException as e:  # noqa
        conn.send(("ERROR", repr(e)))
    finally:
        conn.close()


def correr_prueba(nombre, n, caso, carpeta, limite):
    ctx = multiprocessing.get_context("spawn")
    padre, hijo = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=_trabajador, args=(nombre, n, caso, carpeta, hijo))
    proc.start()
    hijo.close()
    proc.join(limite)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return ("TIMEOUT",)
    if padre.poll():
        return padre.recv()
    return ("ERROR", f"el proceso termino sin resultado (codigo {proc.exitcode})")


def ejecutar(tamanos, casos, limite, archivo_csv, carpeta):
    hw = hardware()
    print("Hardware:", hw)
    print("Limite de tiempo por prueba:", "SIN LIMITE" if limite is None else f"{limite} s")
    agotados = set()  # (algoritmo, caso) que ya hicieron timeout en un tamano menor (solo con --limite)

    # El CSV se escribe fila por fila: si se interrumpe el programa (Ctrl+C) no se pierde lo ya medido.
    with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for k, v in hw.items():
            w.writerow([f"# {k}", v])
        w.writerow(["# limite_tiempo_s", "sin_limite" if limite is None else limite])
        w.writerow(["algoritmo", "n", "caso", "estado", "tiempo_s", "comparaciones", "intercambios"])
        f.flush()

        def guardar(fila):
            w.writerow(fila)
            f.flush()

        for n in tamanos:
            for caso in casos:
                for nombre in ALGORITMOS:
                    etiqueta = f"{nombre:11} n={n:<9} {caso:10}"
                    if (nombre, caso) in agotados:
                        guardar([nombre, n, caso, "TIMEOUT", "", "", ""])
                        print(f"{etiqueta} TIMEOUT (inferido: ya agoto el limite con un n menor)")
                        continue
                    r = correr_prueba(nombre, n, caso, carpeta, limite)
                    if r[0] == "OK":
                        _, t, comp, interc = r
                        guardar([nombre, n, caso, "OK", f"{t:.6f}", comp, interc])
                        print(f"{etiqueta} {t:10.4f}s  comp={comp:<14} interc={interc}", flush=True)
                    elif r[0] == "TIMEOUT":
                        agotados.add((nombre, caso))
                        guardar([nombre, n, caso, "TIMEOUT", "", "", ""])
                        print(f"{etiqueta} TIMEOUT (> {limite} s)")
                    else:
                        guardar([nombre, n, caso, "ERROR", "", "", ""])
                        print(f"{etiqueta} ERROR: {r[1]}")
    print("Resultados guardados en", archivo_csv)


if __name__ == "__main__":
    carpeta = CARPETA_DATOS
    limite = LIMITE_TIEMPO_S
    tamanos = TAMANOS
    for arg in sys.argv[1:]:
        if arg.startswith("--datos="):
            carpeta = arg.split("=", 1)[1]
        elif arg.startswith("--limite="):
            limite = float(arg.split("=", 1)[1])
        elif arg.startswith("--tamanos="):
            tamanos = [int(x) for x in arg.split("=", 1)[1].split(",")]
    if "--rapido" in sys.argv:        # prueba de humo
        tamanos = [100, 1_000]
    ejecutar(tamanos, CASOS, limite, "resultados_python.txt", carpeta)
