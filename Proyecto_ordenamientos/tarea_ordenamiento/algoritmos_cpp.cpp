/*
 * Banco de pruebas de algoritmos de ordenamiento - C++
 *
 * Compilar (elige UNA):
 *   g++ -O2 -std=c++17 -o algoritmos_cpp algoritmos_cpp.cpp          (MinGW / g++)
 *   cl /O2 /EHsc /std:c++17 algoritmos_cpp.cpp                        (Visual Studio, "Developer Command Prompt")
 *
 * Ejecutar:
 *   algoritmos_cpp                      (lee los txt de CARPETA_DATOS, SIN limite de tiempo)
 *   algoritmos_cpp --rapido             (solo tamanos 100 y 1000)
 *   algoritmos_cpp --limite=300         (opcional: cancela las pruebas que pasen de 300 s -> TIMEOUT)
 *   algoritmos_cpp --datos=RUTA         (otra carpeta con los txt)
 *   algoritmos_cpp --tamanos=100,1000   (solo esos tamanos)
 *
 * Cada algoritmo ordena in-place un vector<int> y cuenta (comparaciones, intercambios).
 * Definicion de "intercambios" (igual que en la version de Python):
 *   - Burbuja, Seleccion, Quicksort, Heapsort: intercambios reales de 2 elementos.
 *   - Insercion, Shell, Merge, Bucket, Radix: movimientos/escrituras de elementos.
 *   - Radix no compara elementos entre si (comparaciones = 0).
 *
 * Por defecto NO hay limite de tiempo. Con --limite=SEG, los algoritmos revisan el reloj de forma
 * muy espaciada (una vez cada 256 vueltas de su bucle exterior) y una prueba que pase del limite se
 * cancela y se marca TIMEOUT. El CSV se escribe fila por fila (no se pierde nada si se interrumpe).
 */
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using Clock = std::chrono::steady_clock;
using i64 = long long;
using Vec = std::vector<int>;

// ======================================================================
//  CONTROL DE TIEMPO LIMITE
// ======================================================================
struct Timeout {};
static Clock::time_point g_limite;
static unsigned g_tick = 0;

static inline void chequear() {
    if ((++g_tick & 255u) == 0 && Clock::now() > g_limite) throw Timeout();
}

// ======================================================================
//  ALGORITMOS  (reciben el vector, devuelven comparaciones y intercambios por referencia)
// ======================================================================

static void burbuja(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    int n = (int)a.size();
    for (int i = 0; i < n - 1; i++) {
        chequear();
        for (int j = 0; j < n - 1 - i; j++) {
            cc++;
            if (a[j] > a[j + 1]) {
                std::swap(a[j], a[j + 1]);
                ss++;
            }
        }
    }
    c = cc; s = ss;
}

static void insercion(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    int n = (int)a.size();
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
    c = cc; s = ss;
}

static void seleccion(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    int n = (int)a.size();
    for (int i = 0; i < n - 1; i++) {
        chequear();
        int menor = i;
        for (int j = i + 1; j < n; j++) {
            cc++;
            if (a[j] < a[menor]) menor = j;
        }
        if (menor != i) {
            std::swap(a[i], a[menor]);
            ss++;
        }
    }
    c = cc; s = ss;
}

// Lomuto, pivote = ultimo elemento. Iterativo (pila explicita) para no desbordar la pila
// de llamadas con datos ordenados/inversos.
static void quicksort(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    std::vector<std::pair<int, int>> pila;
    pila.push_back({0, (int)a.size() - 1});
    while (!pila.empty()) {
        chequear();
        std::pair<int, int> r = pila.back();
        pila.pop_back();
        int inicio = r.first, fin = r.second;
        if (inicio >= fin) continue;
        int pivote = a[fin];
        int i = inicio - 1;
        for (int j = inicio; j < fin; j++) {
            cc++;
            if (a[j] <= pivote) {
                i++;
                std::swap(a[i], a[j]);
                ss++;
            }
        }
        std::swap(a[i + 1], a[fin]);
        ss++;
        int p = i + 1;
        pila.push_back({inicio, p - 1});
        pila.push_back({p + 1, fin});
    }
    c = cc; s = ss;
}

static void heapify(Vec& a, int n, int i, i64& cc, i64& ss) {
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
        if (mayor == i) return;
        std::swap(a[i], a[mayor]);
        ss++;
        i = mayor;
    }
}

static void heapsort(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    int n = (int)a.size();
    for (int i = n / 2 - 1; i >= 0; i--) {
        chequear();
        heapify(a, n, i, cc, ss);
    }
    for (int i = n - 1; i > 0; i--) {
        chequear();
        std::swap(a[0], a[i]);
        ss++;
        heapify(a, i, 0, cc, ss);
    }
    c = cc; s = ss;
}

static void merge_(Vec& a, int l, int m, int r, i64& cc, i64& ss) {
    chequear();
    Vec L(a.begin() + l, a.begin() + m + 1);
    Vec R(a.begin() + m + 1, a.begin() + r + 1);
    int n1 = (int)L.size(), n2 = (int)R.size();
    int i = 0, j = 0, k = l;
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
}

static void mergesort_(Vec& a, int l, int r, i64& cc, i64& ss) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergesort_(a, l, m, cc, ss);
        mergesort_(a, m + 1, r, cc, ss);
        merge_(a, l, m, r, cc, ss);
    }
}

static void mergesort(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    mergesort_(a, 0, (int)a.size() - 1, cc, ss);
    c = cc; s = ss;
}

static void shellsort(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    int n = (int)a.size();
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
    c = cc; s = ss;
}

// Datos enteros >= 0: se normalizan a [0,1) con (x-min)/(max-min+1) para repartir en n cubetas.
static void bucketsort(Vec& a, i64& c, i64& s) {
    i64 cc = 0, ss = 0;
    int n = (int)a.size();
    if (n < 2) { c = 0; s = 0; return; }
    int mn = *std::min_element(a.begin(), a.end());
    int mx = *std::max_element(a.begin(), a.end());
    i64 rango = (i64)mx - mn + 1;
    std::vector<Vec> cubetas(n);
    for (int x : a) {
        chequear();
        cubetas[(size_t)(((i64)n * ((i64)x - mn)) / rango)].push_back(x);
        ss++;
    }
    for (Vec& b : cubetas) {
        chequear();
        int m = (int)b.size();
        for (int i = 1; i < m; i++) {
            int val = b[i];
            int k = i - 1;
            while (k >= 0) {
                cc++;
                if (b[k] > val) {
                    b[k + 1] = b[k];
                    ss++;
                    k--;
                } else {
                    break;
                }
            }
            if (k + 1 != i) {
                b[k + 1] = val;
                ss++;
            }
        }
    }
    size_t idx = 0;
    for (const Vec& b : cubetas) {
        chequear();
        for (int x : b) {
            a[idx++] = x;
            ss++;
        }
    }
    c = cc; s = ss;
}

// LSD base 10, solo enteros >= 0. No compara elementos entre si.
static void radixsort(Vec& a, i64& c, i64& s) {
    i64 ss = 0;
    int n = (int)a.size();
    if (n == 0) { c = 0; s = 0; return; }
    int max_val = *std::max_element(a.begin(), a.end());
    Vec salida(n);
    for (i64 exp = 1; max_val / exp > 0; exp *= 10) {
        chequear();
        i64 cuenta[10] = {0};
        for (int i = 0; i < n; i++) cuenta[(a[i] / exp) % 10]++;
        for (int i = 1; i < 10; i++) cuenta[i] += cuenta[i - 1];
        for (int i = n - 1; i >= 0; i--) {
            int d = (int)((a[i] / exp) % 10);
            cuenta[d]--;
            salida[(size_t)cuenta[d]] = a[i];
            ss++;
        }
        a = salida;  // copia de vuelta (no se cuenta como intercambio, igual que en Python)
    }
    c = 0; s = ss;
}

typedef void (*Algoritmo)(Vec&, i64&, i64&);
struct Entrada { const char* nombre; Algoritmo fn; };
static const Entrada ALGORITMOS[] = {
    {"Burbuja", burbuja},     {"Insercion", insercion}, {"Seleccion", seleccion},
    {"Quicksort", quicksort}, {"Heapsort", heapsort},   {"Mergesort", mergesort},
    {"Shellsort", shellsort}, {"Bucketsort", bucketsort}, {"Radixsort", radixsort},
};

// ======================================================================
//  CONFIGURACION DE LA PRUEBA
// ======================================================================
static const i64 TAMANOS[] = {100, 1000, 10000, 100000, 1000000};
static const char* CASOS[] = {"aleatorio", "ordenado", "inverso"};
static std::string CARPETA_DATOS = "arreglos_txt";  // carpeta con los txt (relativa a donde ejecutas el programa). --datos=RUTA para cambiarla
static double LIMITE_TIEMPO_S = 0;  // 0 = SIN LIMITE (cada prueba corre hasta terminar). --limite=SEG para cancelar las lentas
static const char* ARCHIVO_CSV = "resultados_cpp.txt";

// Hardware de la maquina donde se corre la prueba (se escribe en el encabezado del CSV)
static const char* HW_PROCESADOR = "AMD Ryzen 5 7535HS (3.30 GHz)";
static const char* HW_RAM = "16 GB";
static const char* HW_GRAFICA = "NVIDIA GeForce RTX 4050 Laptop GPU (6 GB)";

static bool cargar(i64 n, const std::string& caso, const std::string& carpeta, Vec& out) {
    std::string ruta = carpeta + "/" + caso + "_" + std::to_string(n) + ".txt";
    std::ifstream f(ruta, std::ios::binary);
    if (!f) {
        std::cerr << "No se pudo abrir: " << ruta << "\n";
        return false;
    }
    std::string txt((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
    out.clear();
    out.reserve((size_t)n);
    long long v = 0;
    bool en_numero = false;
    for (char ch : txt) {
        if (ch >= '0' && ch <= '9') {
            v = v * 10 + (ch - '0');
            en_numero = true;
        } else if (en_numero) {
            out.push_back((int)v);
            v = 0;
            en_numero = false;
        }
    }
    if (en_numero) out.push_back((int)v);
    if ((i64)out.size() != n) {
        std::cerr << ruta << ": se esperaban " << n << " datos y hay " << out.size() << "\n";
        return false;
    }
    return true;
}

static std::string sistema() {
#if defined(_WIN32)
    return "Windows";
#elif defined(__linux__)
    return "Linux";
#elif defined(__APPLE__)
    return "macOS";
#else
    return "desconocido";
#endif
}

static std::string compilador() {
#if defined(_MSC_VER)
    return "MSVC " + std::to_string(_MSC_VER);
#elif defined(__clang__)
    return std::string("clang ") + __clang_version__;
#elif defined(__GNUC__)
    return std::string("g++ ") + __VERSION__;
#else
    return "desconocido";
#endif
}

struct Fila {
    std::string alg;
    i64 n;
    std::string caso;
    std::string estado;
    double t;
    i64 c, s;
};

int main(int argc, char** argv) {
    std::string carpeta = CARPETA_DATOS;
    double limite = LIMITE_TIEMPO_S;  // 0 = sin limite
    std::vector<i64> tamanos(std::begin(TAMANOS), std::end(TAMANOS));
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg.rfind("--datos=", 0) == 0) {
            carpeta = arg.substr(8);
        } else if (arg.rfind("--limite=", 0) == 0) {
            limite = std::atof(arg.c_str() + 9);
        } else if (arg.rfind("--tamanos=", 0) == 0) {
            tamanos.clear();
            std::stringstream ss(arg.substr(10));
            std::string tok;
            while (std::getline(ss, tok, ',')) tamanos.push_back(std::atoll(tok.c_str()));
        } else if (arg == "--rapido") {
            tamanos = {100, 1000};
        }
    }
    const bool hay_limite = limite > 0;
    const std::string txt_limite = hay_limite ? std::to_string(limite) : std::string("sin_limite");

#if defined(__GNUC__) && !defined(__OPTIMIZE__)
    std::cerr << "AVISO: compilado SIN optimizacion. Usa -O2 para tiempos representativos.\n";
#endif

    std::cout << "Hardware: " << HW_PROCESADOR << " | " << HW_RAM << " | " << HW_GRAFICA << "\n";
    std::cout << "Compilador: " << compilador() << "\n";
    std::cout << "Limite de tiempo por prueba: " << (hay_limite ? txt_limite + " s" : std::string("SIN LIMITE")) << "\n";

    // El CSV se escribe fila por fila: si se interrumpe el programa (Ctrl+C) no se pierde lo ya medido.
    std::ofstream out(ARCHIVO_CSV);
    out << "# lenguaje,C++\n";
    out << "# compilador," << compilador() << "\n";
    out << "# sistema," << sistema() << "\n";
    out << "# procesador," << HW_PROCESADOR << "\n";
    out << "# ram," << HW_RAM << "\n";
    out << "# grafica," << HW_GRAFICA << "\n";
    out << "# limite_tiempo_s," << txt_limite << "\n";
    out << "algoritmo,n,caso,estado,tiempo_s,comparaciones,intercambios\n";
    out.flush();

    auto guardar = [&out](const Fila& f) {
        out << f.alg << "," << f.n << "," << f.caso << "," << f.estado << ",";
        if (f.estado == "OK") {
            char buf[64];
            std::snprintf(buf, sizeof buf, "%.6f", f.t);
            out << buf << "," << f.c << "," << f.s << "\n";
        } else {
            out << ",,\n";
        }
        out.flush();
    };

    std::set<std::pair<std::string, std::string>> agotados;  // (algoritmo, caso) con timeout en un n menor (solo con --limite)

    for (i64 n : tamanos) {
        for (const char* caso : CASOS) {
            Vec datos, esperado;
            bool cargado = false;
            for (const Entrada& e : ALGORITMOS) {
                char etiqueta[128];
                std::snprintf(etiqueta, sizeof etiqueta, "%-11s n=%-9lld %-10s", e.nombre, n, caso);
                auto clave = std::make_pair(std::string(e.nombre), std::string(caso));

                if (agotados.count(clave)) {
                    guardar({e.nombre, n, caso, "TIMEOUT", 0, 0, 0});
                    std::cout << etiqueta << " TIMEOUT (inferido: ya agoto el limite con un n menor)\n" << std::flush;
                    continue;
                }
                if (!cargado) {
                    if (!cargar(n, caso, carpeta, datos)) return 1;
                    esperado = datos;
                    std::sort(esperado.begin(), esperado.end());
                    cargado = true;
                }
                Vec copia = datos;
                i64 c = 0, s = 0;
                g_tick = 0;
                bool agoto = false;
                double t = 0;
                try {
                    auto t0 = Clock::now();
                    g_limite = hay_limite
                        ? t0 + std::chrono::duration_cast<Clock::duration>(std::chrono::duration<double>(limite))
                        : Clock::time_point::max();
                    e.fn(copia, c, s);
                    auto t1 = Clock::now();
                    t = std::chrono::duration<double>(t1 - t0).count();
                } catch (const Timeout&) {
                    agoto = true;
                }
                if (agoto) {
                    agotados.insert(clave);
                    guardar({e.nombre, n, caso, "TIMEOUT", 0, 0, 0});
                    std::cout << etiqueta << " TIMEOUT (> " << limite << " s)\n" << std::flush;
                } else if (copia != esperado) {
                    guardar({e.nombre, n, caso, "ERROR", 0, 0, 0});
                    std::cout << etiqueta << " ERROR: no ordeno correctamente\n" << std::flush;
                } else {
                    guardar({e.nombre, n, caso, "OK", t, c, s});
                    std::printf("%s %10.4fs  comp=%-14lld interc=%lld\n", etiqueta, t, c, s);
                    std::fflush(stdout);
                }
            }
        }
    }
    std::cout << "Resultados guardados en " << ARCHIVO_CSV << "\n";
    return 0;
}
