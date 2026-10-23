/*
 * Banco de pruebas de algoritmos de ordenamiento - JAVASCRIPT (Node.js)
 *
 * Ejecutar (necesita Node.js instalado):
 *   node algoritmos_js.js                     (lee los txt de CARPETA_DATOS, SIN limite de tiempo)
 *   node algoritmos_js.js --rapido            (solo tamanos 100 y 1000)
 *   node algoritmos_js.js --limite=300        (opcional: cancela las pruebas que pasen de 300 s -> TIMEOUT)
 *   node algoritmos_js.js --datos=RUTA        (otra carpeta con los txt)
 *   node algoritmos_js.js --tamanos=100,1000  (solo esos tamanos)
 *   node --expose-gc algoritmos_js.js         (opcional: fuerza una recoleccion de basura antes de cada prueba)
 *
 * Cada algoritmo ordena in-place un Int32Array y devuelve [comparaciones, intercambios].
 * Definicion de "intercambios" (igual que en Python, C++ y Java):
 *   - Burbuja, Seleccion, Quicksort, Heapsort: intercambios reales de 2 elementos.
 *   - Insercion, Shell, Merge, Bucket, Radix: movimientos/escrituras de elementos.
 *   - Radix no compara elementos entre si (comparaciones = 0).
 *
 * V8 (el motor de Node) optimiza el codigo mientras corre, asi que antes de medir se hace un
 * calentamiento (NO medido) de cada algoritmo con un arreglo pequeno.
 *
 * Por defecto NO hay limite de tiempo. Con --limite=SEG los algoritmos revisan el reloj una vez cada 256
 * vueltas de su bucle exterior (costo despreciable) y una prueba que pase del limite se cancela y se
 * marca TIMEOUT. El CSV se escribe fila por fila (no se pierde nada si se interrumpe el programa).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { performance } = require("perf_hooks");

// ======================================================================
//  CONTROL DE TIEMPO LIMITE
// ======================================================================
const TIMEOUT = { timeout: true };  // objeto centinela (no es Error: no captura stack trace)
let limiteMs = 0;
let tick = 0;

function chequear() {
  if ((++tick & 255) === 0 && performance.now() > limiteMs) throw TIMEOUT;
}

// ======================================================================
//  ALGORITMOS  (devuelven [comparaciones, intercambios])
// ======================================================================

function burbuja(a) {
  let cc = 0, ss = 0;
  const n = a.length;
  for (let i = 0; i < n - 1; i++) {
    chequear();
    for (let j = 0; j < n - 1 - i; j++) {
      cc++;
      if (a[j] > a[j + 1]) {
        const t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
        ss++;
      }
    }
  }
  return [cc, ss];
}

function insercion(a) {
  let cc = 0, ss = 0;
  const n = a.length;
  for (let i = 1; i < n; i++) {
    chequear();
    const actual = a[i];
    let j = i - 1;
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
    if (j + 1 !== i) {
      a[j + 1] = actual;
      ss++;
    }
  }
  return [cc, ss];
}

function seleccion(a) {
  let cc = 0, ss = 0;
  const n = a.length;
  for (let i = 0; i < n - 1; i++) {
    chequear();
    let menor = i;
    for (let j = i + 1; j < n; j++) {
      cc++;
      if (a[j] < a[menor]) menor = j;
    }
    if (menor !== i) {
      const t = a[i]; a[i] = a[menor]; a[menor] = t;
      ss++;
    }
  }
  return [cc, ss];
}

// Lomuto, pivote = ultimo elemento. Iterativo (pila explicita) para no desbordar la pila de
// llamadas con datos ordenados/inversos (la recursion llegaria a 1,000,000 de niveles).
function quicksort(a) {
  let cc = 0, ss = 0;
  let pilaI = new Int32Array(64);
  let pilaF = new Int32Array(64);
  let tope = 0;
  if (a.length > 1) {
    pilaI[0] = 0;
    pilaF[0] = a.length - 1;
    tope = 1;
  }
  while (tope > 0) {
    chequear();
    tope--;
    const inicio = pilaI[tope], fin = pilaF[tope];
    const pivote = a[fin];
    let i = inicio - 1;
    for (let j = inicio; j < fin; j++) {
      cc++;
      if (a[j] <= pivote) {
        i++;
        const t = a[i]; a[i] = a[j]; a[j] = t;
        ss++;
      }
    }
    const t = a[i + 1]; a[i + 1] = a[fin]; a[fin] = t;
    ss++;
    const p = i + 1;
    if (tope + 2 > pilaI.length) {
      const nI = new Int32Array(pilaI.length * 2); nI.set(pilaI); pilaI = nI;
      const nF = new Int32Array(pilaF.length * 2); nF.set(pilaF); pilaF = nF;
    }
    if (inicio < p - 1) { pilaI[tope] = inicio; pilaF[tope] = p - 1; tope++; }
    if (p + 1 < fin)    { pilaI[tope] = p + 1;  pilaF[tope] = fin;   tope++; }
  }
  return [cc, ss];
}

function heapify(a, n, i, ct) {
  let cc = ct[0], ss = ct[1];
  for (;;) {
    let mayor = i;
    const izq = 2 * i + 1;
    const der = 2 * i + 2;
    if (izq < n) {
      cc++;
      if (a[izq] > a[mayor]) mayor = izq;
    }
    if (der < n) {
      cc++;
      if (a[der] > a[mayor]) mayor = der;
    }
    if (mayor === i) break;
    const t = a[i]; a[i] = a[mayor]; a[mayor] = t;
    ss++;
    i = mayor;
  }
  ct[0] = cc; ct[1] = ss;
}

function heapsort(a) {
  const ct = [0, 0];
  const n = a.length;
  for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
    chequear();
    heapify(a, n, i, ct);
  }
  for (let i = n - 1; i > 0; i--) {
    chequear();
    const t = a[0]; a[0] = a[i]; a[i] = t;
    ct[1]++;
    heapify(a, i, 0, ct);
  }
  return ct;
}

function merge(a, l, m, r, ct) {
  chequear();
  const L = a.slice(l, m + 1);
  const R = a.slice(m + 1, r + 1);
  const n1 = L.length, n2 = R.length;
  let i = 0, j = 0, k = l;
  let cc = 0, ss = 0;
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

function mergesortRec(a, l, r, ct) {
  if (l < r) {
    const m = l + Math.floor((r - l) / 2);
    mergesortRec(a, l, m, ct);
    mergesortRec(a, m + 1, r, ct);
    merge(a, l, m, r, ct);
  }
}

function mergesort(a) {
  const ct = [0, 0];
  mergesortRec(a, 0, a.length - 1, ct);
  return ct;
}

function shellsort(a) {
  let cc = 0, ss = 0;
  const n = a.length;
  for (let gap = Math.floor(n / 2); gap > 0; gap = Math.floor(gap / 2)) {
    for (let j = gap; j < n; j++) {
      chequear();
      const val = a[j];
      let k = j;
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
      if (k !== j) {
        a[k] = val;
        ss++;
      }
    }
  }
  return [cc, ss];
}

// Datos enteros >= 0: se normalizan a [0,1) con (x-min)/(max-min+1) para repartir en n cubetas.
function bucketsort(a) {
  let cc = 0, ss = 0;
  const n = a.length;
  if (n < 2) return [0, 0];
  let mn = a[0], mx = a[0];
  for (let i = 1; i < n; i++) {
    if (a[i] < mn) mn = a[i];
    if (a[i] > mx) mx = a[i];
  }
  const rango = mx - mn + 1;
  const cub = new Array(n);
  for (let i = 0; i < n; i++) {
    chequear();
    const x = a[i];
    const b = Math.floor((n * (x - mn)) / rango);
    if (cub[b] === undefined) cub[b] = [x]; else cub[b].push(x);
    ss++;
  }
  for (let b = 0; b < n; b++) {
    chequear();
    const v = cub[b];
    if (v === undefined) continue;
    const m = v.length;
    for (let i = 1; i < m; i++) {
      const val = v[i];
      let k = i - 1;
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
      if (k + 1 !== i) {
        v[k + 1] = val;
        ss++;
      }
    }
  }
  let idx = 0;
  for (let b = 0; b < n; b++) {
    chequear();
    const v = cub[b];
    if (v === undefined) continue;
    for (let i = 0; i < v.length; i++) {
      a[idx++] = v[i];
      ss++;
    }
  }
  return [cc, ss];
}

// LSD base 10, solo enteros >= 0. No compara elementos entre si.
function radixsort(a) {
  let ss = 0;
  const n = a.length;
  if (n === 0) return [0, 0];
  let maxVal = a[0];
  for (let i = 1; i < n; i++) if (a[i] > maxVal) maxVal = a[i];
  const salida = new Int32Array(n);
  for (let exp = 1; Math.floor(maxVal / exp) > 0; exp *= 10) {
    chequear();
    const cuenta = new Int32Array(10);
    for (let i = 0; i < n; i++) cuenta[Math.floor(a[i] / exp) % 10]++;
    for (let i = 1; i < 10; i++) cuenta[i] += cuenta[i - 1];
    for (let i = n - 1; i >= 0; i--) {
      const d = Math.floor(a[i] / exp) % 10;
      cuenta[d]--;
      salida[cuenta[d]] = a[i];
      ss++;
    }
    a.set(salida);  // copia de vuelta (no se cuenta, igual que en Python/C++/Java)
  }
  return [0, ss];
}

const ALGORITMOS = [
  ["Burbuja", burbuja],
  ["Insercion", insercion],
  ["Seleccion", seleccion],
  ["Quicksort", quicksort],
  ["Heapsort", heapsort],
  ["Mergesort", mergesort],
  ["Shellsort", shellsort],
  ["Bucketsort", bucketsort],
  ["Radixsort", radixsort],
];

// ======================================================================
//  CONFIGURACION DE LA PRUEBA
// ======================================================================
const TAMANOS = [100, 1000, 10000, 100000, 1000000];
const CASOS = ["aleatorio", "ordenado", "inverso"];
const CARPETA_DATOS = "arreglos_txt";  // --datos=RUTA para cambiarla
const LIMITE_TIEMPO_S = 0;  // 0 = SIN LIMITE (cada prueba corre hasta terminar). --limite=SEG para cancelar las lentas
const ARCHIVO_CSV = "resultados_js.txt";

// Hardware de la maquina donde se corre la prueba (se escribe en el encabezado del CSV)
const HW_PROCESADOR = "AMD Ryzen 5 7535HS (3.30 GHz)";
const HW_RAM = "16 GB";
const HW_GRAFICA = "NVIDIA GeForce RTX 4050 Laptop GPU (6 GB)";

function cargar(n, caso, carpeta) {
  const ruta = path.join(carpeta, `${caso}_${n}.txt`);
  const bytes = fs.readFileSync(ruta);
  const out = new Int32Array(n);
  let cuenta = 0, v = 0, enNumero = false;
  for (let i = 0; i < bytes.length; i++) {
    const b = bytes[i];
    if (b >= 48 && b <= 57) {
      v = v * 10 + (b - 48);
      enNumero = true;
    } else if (enNumero) {
      if (cuenta < n) out[cuenta] = v;
      cuenta++;
      v = 0;
      enNumero = false;
    }
  }
  if (enNumero) {
    if (cuenta < n) out[cuenta] = v;
    cuenta++;
  }
  if (cuenta !== n) throw new Error(`${ruta}: se esperaban ${n} datos y hay ${cuenta}`);
  return out;
}

function iguales(x, y) {
  if (x.length !== y.length) return false;
  for (let i = 0; i < x.length; i++) if (x[i] !== y[i]) return false;
  return true;
}

function calentar() {
  // Calentamiento del JIT: NO se mide. Ejecuta cada algoritmo varias veces con 2000 datos.
  let semilla = 12345;
  const base = new Int32Array(2000);
  for (let i = 0; i < base.length; i++) {
    semilla = (semilla * 1103515245 + 12345) & 0x7fffffff;
    base[i] = semilla % 2001;
  }
  limiteMs = performance.now() + 60000;
  for (let rep = 0; rep < 20; rep++) {
    for (const [, fn] of ALGORITMOS) fn(Int32Array.from(base));
  }
}

function main() {
  let carpeta = CARPETA_DATOS;
  let limite = LIMITE_TIEMPO_S;
  let tamanos = TAMANOS;
  for (const arg of process.argv.slice(2)) {
    if (arg.startsWith("--datos=")) carpeta = arg.slice(8);
    else if (arg.startsWith("--limite=")) limite = parseFloat(arg.slice(9));
    else if (arg.startsWith("--tamanos=")) tamanos = arg.slice(10).split(",").map((x) => parseInt(x, 10));
    else if (arg === "--rapido") tamanos = [100, 1000];
  }

  const runtime = `Node.js ${process.version} (V8 ${process.versions.v8})`;
  const sistema = `${process.platform} ${require("os").release()}`;
  console.log(`Hardware: ${HW_PROCESADOR} | ${HW_RAM} | ${HW_GRAFICA}`);
  console.log(`Runtime: ${runtime} | Sistema: ${sistema}`);
  console.log(`Limite de tiempo por prueba: ${limite > 0 ? limite + " s" : "SIN LIMITE"}`);
  console.log("Calentando JIT...");
  calentar();

  // El CSV se escribe fila por fila: si se interrumpe el programa (Ctrl+C) no se pierde lo ya medido.
  const txtLimite = limite > 0 ? String(limite) : "sin_limite";
  fs.writeFileSync(ARCHIVO_CSV, [
    "# lenguaje,JavaScript",
    `# runtime,${runtime}`,
    `# sistema,${sistema}`,
    `# procesador,${HW_PROCESADOR}`,
    `# ram,${HW_RAM}`,
    `# grafica,${HW_GRAFICA}`,
    `# limite_tiempo_s,${txtLimite}`,
    "algoritmo,n,caso,estado,tiempo_s,comparaciones,intercambios",
  ].join("\n") + "\n", "utf8");
  const guardar = (fila) => fs.appendFileSync(ARCHIVO_CSV, fila.join(",") + "\n", "utf8");
  const agotados = new Set();  // "algoritmo|caso" que ya hizo timeout con un n menor

  for (const n of tamanos) {
    for (const caso of CASOS) {
      let datos = null, esperado = null;
      for (const [nombre, fn] of ALGORITMOS) {
        const etiqueta = `${nombre.padEnd(11)} n=${String(n).padEnd(9)} ${caso.padEnd(10)}`;
        const clave = `${nombre}|${caso}`;

        if (agotados.has(clave)) {
          guardar([nombre, n, caso, "TIMEOUT", "", "", ""]);
          console.log(`${etiqueta} TIMEOUT (inferido: ya agoto el limite con un n menor)`);
          continue;
        }
        if (datos === null) {
          datos = cargar(n, caso, carpeta);
          esperado = Int32Array.from(datos).sort();  // Int32Array.sort() ordena numericamente
        }
        const copia = Int32Array.from(datos);
        if (global.gc) global.gc();  // fuera del tiempo medido (solo con --expose-gc)
        tick = 0;
        let r = null, t = 0, agoto = false;
        try {
          const t0 = performance.now();
          limiteMs = limite > 0 ? t0 + limite * 1000 : Infinity;
          r = fn(copia);
          t = (performance.now() - t0) / 1000;
        } catch (e) {
          if (e === TIMEOUT) agoto = true; else throw e;
        }
        if (agoto) {
          agotados.add(clave);
          guardar([nombre, n, caso, "TIMEOUT", "", "", ""]);
          console.log(`${etiqueta} TIMEOUT (> ${limite} s)`);
        } else if (!iguales(copia, esperado)) {
          guardar([nombre, n, caso, "ERROR", "", "", ""]);
          console.log(`${etiqueta} ERROR: no ordeno correctamente`);
        } else {
          guardar([nombre, n, caso, "OK", t.toFixed(6), r[0], r[1]]);
          console.log(`${etiqueta} ${t.toFixed(4).padStart(10)}s  comp=${String(r[0]).padEnd(14)} interc=${r[1]}`);
        }
      }
    }
  }

  console.log(`Resultados guardados en ${ARCHIVO_CSV}`);
}

main();
