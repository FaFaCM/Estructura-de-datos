#!/usr/bin/env python3
"""
GESTOR - compara los resultados de los 5 lenguajes (solo texto).

Lee estos archivos .txt (generados por cada programa; tambien acepta los .csv con el mismo nombre) y escribe reporte_final.txt:
    resultados_python.txt   resultados_cpp.txt   resultados_java.txt
    resultados_js.txt       resultados_cs.txt

Uso:
    python gestor.py                      (busca los CSV en la carpeta donde esta gestor.py)
    python gestor.py --carpeta=RUTA       (otra carpeta con los CSV)
    python gestor.py --sin-detalle        (omite la seccion 6, las matrices completas)

Criterios:
  - Lenguaje mas rapido: se comparan SOLO las pruebas (algoritmo, n, caso) que TODOS los
    lenguajes presentes completaron (estado OK). Metrica principal: media geometrica de
    "veces mas lento que el mejor lenguaje en esa prueba" (1.00x = el mejor).
  - Algoritmo mas rapido: en cada lenguaje y cada (n, caso) donde los 9 algoritmos tienen
    resultado (OK o TIMEOUT), se ordenan por tiempo; un TIMEOUT queda detras de todos los
    que terminaron. Metrica principal: posicion promedio.
"""
import csv
import math
import os
import sys

LENGUAJES = [
    ("Python", "resultados_python.txt"),
    ("C++", "resultados_cpp.txt"),
    ("Java", "resultados_java.txt"),
    ("JavaScript", "resultados_js.txt"),
    ("C#", "resultados_cs.txt"),
]
ALGORITMOS = ["Burbuja", "Insercion", "Seleccion", "Quicksort", "Heapsort",
              "Mergesort", "Shellsort", "Bucketsort", "Radixsort"]
CASOS = ["aleatorio", "ordenado", "inverso"]
N_GRANDE = 10_000     # umbral para la comparacion "solo tamanos grandes"
MIN_T = 1e-6          # resolucion de los CSV (6 decimales); evita dividir entre 0
PRUEBAS_ESPERADAS = 135

SALIDA = []


def p(texto=""):
    SALIDA.append(texto)
    print(texto)


# ----------------------------------------------------------------------
#  Lectura de CSV (acepta el formato nuevo con columna "estado" y el viejo de Python)
# ----------------------------------------------------------------------
def leer_csv(ruta):
    meta, datos, cols = {}, {}, None
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        for fila in csv.reader(f):
            if not fila:
                continue
            if fila[0].startswith("#"):
                meta[fila[0][1:].strip()] = fila[1].strip() if len(fila) > 1 else ""
                continue
            if fila[0].strip() == "algoritmo":
                cols = [c.strip() for c in fila]
                continue
            if cols is None:
                continue
            r = dict(zip(cols, fila))
            clave = (r["algoritmo"], int(r["n"]), r["caso"])
            if "estado" in r:
                estado = r["estado"]
            else:  # formato viejo: tiempo_s = "OMITIDO" cuando no se ejecuto
                estado = "OMITIDO" if r.get("tiempo_s", "") == "OMITIDO" else "OK"
            if estado == "OK":
                datos[clave] = ("OK", float(r["tiempo_s"]), int(r["comparaciones"]), int(r["intercambios"]))
            else:
                datos[clave] = (estado, None, None, None)
    return meta, datos


# ----------------------------------------------------------------------
#  Utilidades
# ----------------------------------------------------------------------
def fmt_t(t):
    if t is None:
        return "-"
    if t < 1:
        return f"{t:.4f}"
    if t < 100:
        return f"{t:.3f}"
    return f"{t:.1f}"


def fmt_n(x):
    return f"{x:,}"


def geomedia(valores):
    return math.exp(sum(math.log(v) for v in valores) / len(valores))


def media(valores):
    return sum(valores) / len(valores)


def rangos(valores):
    """valores: dict clave -> valor comparable (menor = mejor). Empates -> posicion promedio."""
    orden = sorted(valores.items(), key=lambda kv: kv[1])
    res, i = {}, 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and orden[j + 1][1] == orden[i][1]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            res[orden[k][0]] = r
        i = j + 1
    return res


def tabla(enc, filas, izq=(0,), sangria="  "):
    cols = list(zip(enc, *filas)) if filas else [(h,) for h in enc]
    anchos = [max(len(str(x)) for x in c) for c in cols]

    def linea(f):
        celdas = []
        for i, x in enumerate(f):
            x = str(x)
            celdas.append(x.ljust(anchos[i]) if i in izq else x.rjust(anchos[i]))
        return sangria + " | ".join(celdas)

    p(linea(enc))
    p(sangria + "-+-".join("-" * a for a in anchos))
    for f in filas:
        p(linea(f))


def titulo(texto, nivel=1):
    p()
    if nivel == 1:
        p("=" * 78)
        p(texto)
        p("=" * 78)
    else:
        p(texto)
        p("-" * len(texto))


# ----------------------------------------------------------------------
#  Comparacion de lenguajes
# ----------------------------------------------------------------------
def estadisticas_lenguajes(celdas, langs, datos):
    est = {l: {"vic": 0, "rank": [], "ratios": [], "total": 0.0} for l in langs}
    for k in celdas:
        ts = {l: max(datos[l][k][1], MIN_T) for l in langs}
        mejor = min(ts.values())
        rk = rangos(ts)
        for l in langs:
            est[l]["rank"].append(rk[l])
            est[l]["ratios"].append(ts[l] / mejor)
            est[l]["total"] += datos[l][k][1]
            if ts[l] == mejor:
                est[l]["vic"] += 1
    return est


def ganador_lenguajes(celdas, langs, datos):
    if not celdas:
        return None, None
    est = estadisticas_lenguajes(celdas, langs, datos)
    geo = {l: geomedia(est[l]["ratios"]) for l in langs}
    return min(geo, key=geo.get), geo


def ranking_lenguajes(titulo_txt, celdas, langs, datos):
    p(titulo_txt)
    if not celdas:
        p("  (no hay pruebas en comun para comparar)")
        return
    est = estadisticas_lenguajes(celdas, langs, datos)
    geo = {l: geomedia(est[l]["ratios"]) for l in langs}
    orden = sorted(langs, key=geo.get)
    filas = []
    for i, l in enumerate(orden, 1):
        filas.append([i, l, f"{est[l]['vic']}/{len(celdas)}", f"{media(est[l]['rank']):.2f}",
                      f"{geo[l]:.2f}x", fmt_t(est[l]["total"])])
    tabla(["#", "Lenguaje", "Victorias", "Posicion prom.", "Veces mas lento", "Tiempo total (s)"],
          filas, izq=(1,))


def tabla_por_grupo(celdas, langs, datos, grupo_fn, nombre_grupo, grupos):
    filas = []
    for g in grupos:
        sub = [k for k in celdas if grupo_fn(k) == g]
        if not sub:
            continue
        est = estadisticas_lenguajes(sub, langs, datos)
        geo = {l: geomedia(est[l]["ratios"]) for l in langs}
        mejor = min(geo, key=geo.get)
        filas.append([g] + [f"{geo[l]:.2f}x" for l in langs] + [mejor, len(sub)])
    if filas:
        tabla([nombre_grupo] + langs + ["Mas rapido", "Pruebas"], filas, izq=(0, len(langs) + 1))
    else:
        p("  (sin datos)")


# ----------------------------------------------------------------------
#  Comparacion de algoritmos
# ----------------------------------------------------------------------
def construir_entradas(langs, datos, ns):
    """Una entrada por (lenguaje, n, caso) donde los 9 algoritmos tienen resultado OK o TIMEOUT."""
    entradas = []
    for l in langs:
        for n in ns:
            for caso in CASOS:
                res = {a: datos[l].get((a, n, caso)) for a in ALGORITMOS}
                if all(v and v[0] in ("OK", "TIMEOUT") for v in res.values()) and \
                        any(v[0] == "OK" for v in res.values()):
                    entradas.append((l, n, caso, res))
    return entradas


def estadisticas_algoritmos(entradas):
    est = {a: {"rank": [], "ratios": [], "primeros": 0, "timeouts": 0} for a in ALGORITMOS}
    for (_, _, _, res) in entradas:
        clave = {a: ((0, v[1]) if v[0] == "OK" else (1, 0.0)) for a, v in res.items()}
        rk = rangos(clave)
        mejor_t = min(max(v[1], MIN_T) for v in res.values() if v[0] == "OK")
        mejor_clave = min(clave.values())
        for a, v in res.items():
            est[a]["rank"].append(rk[a])
            if clave[a] == mejor_clave:
                est[a]["primeros"] += 1
            if v[0] == "OK":
                est[a]["ratios"].append(max(v[1], MIN_T) / mejor_t)
            else:
                est[a]["timeouts"] += 1
    return est


def ganador_algoritmo(entradas):
    if not entradas:
        return None, None
    est = estadisticas_algoritmos(entradas)
    pos = {a: media(est[a]["rank"]) for a in ALGORITMOS}
    return min(pos, key=pos.get), pos


def ranking_algoritmos(titulo_txt, entradas):
    p(titulo_txt)
    if not entradas:
        p("  (no hay pruebas con los 9 algoritmos completos)")
        return
    est = estadisticas_algoritmos(entradas)
    pos = {a: media(est[a]["rank"]) for a in ALGORITMOS}
    filas = []
    for i, a in enumerate(sorted(ALGORITMOS, key=pos.get), 1):
        e = est[a]
        geo = f"{geomedia(e['ratios']):.2f}x" if e["ratios"] else "-"
        filas.append([i, a, f"{pos[a]:.2f}", f"{e['primeros']}/{len(entradas)}", geo, e["timeouts"]])
    tabla(["#", "Algoritmo", "Posicion prom.", "1eros lugares", "Veces mas lento*", "TIMEOUT"],
          filas, izq=(1,))
    p("  * media geometrica contra el mejor algoritmo de cada prueba, solo pruebas terminadas.")


# ----------------------------------------------------------------------
#  Programa principal
# ----------------------------------------------------------------------
def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    detalle = True
    for arg in sys.argv[1:]:
        if arg.startswith("--carpeta="):
            carpeta = arg.split("=", 1)[1]
        elif arg == "--sin-detalle":
            detalle = False
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # ---------- carga ----------
    metas, datos, avisos, faltan = {}, {}, [], []
    for nombre, archivo in LENGUAJES:
        ruta = os.path.join(carpeta, archivo)
        if not os.path.exists(ruta):  # compatibilidad: tambien acepta la version .csv
            alterno = os.path.join(carpeta, archivo[:-4] + ".csv")
            if os.path.exists(alterno):
                ruta = alterno
        if not os.path.exists(ruta) and os.path.exists(archivo):
            ruta = archivo
        if not os.path.exists(ruta):
            faltan.append(nombre)
            continue
        try:
            metas[nombre], datos[nombre] = leer_csv(ruta)
        except Exception as e:  # noqa
            avisos.append(f"No se pudo leer {archivo}: {e}")
            faltan.append(nombre)
    langs = [n for n, _ in LENGUAJES if n in datos]
    if not langs:
        print(f"No se encontro ningun archivo de resultados (.txt) en {carpeta}")
        return 1
    ns = sorted({k[1] for l in langs for k in datos[l]})

    titulo("REPORTE COMPARATIVO - ALGORITMOS DE ORDENAMIENTO")
    p("Algoritmos: " + ", ".join(ALGORITMOS))
    p("Tamanos: " + ", ".join(fmt_n(n) for n in ns) + "   |   Casos: " + ", ".join(CASOS))

    # ---------- resumen (se calcula primero, se imprime arriba) ----------
    celdas_comunes = sorted(set.intersection(*[{k for k, v in datos[l].items() if v[0] == "OK"} for l in langs])) \
        if len(langs) >= 2 else []
    celdas_grandes = [k for k in celdas_comunes if k[1] >= N_GRANDE]
    gan_len, geo_len = ganador_lenguajes(celdas_comunes, langs, datos)
    gan_len_g, geo_len_g = ganador_lenguajes(celdas_grandes, langs, datos)
    entradas = construir_entradas(langs, datos, ns)
    entradas_g = [e for e in entradas if e[1] >= N_GRANDE]
    gan_alg, pos_alg = ganador_algoritmo(entradas)
    gan_alg_g, pos_alg_g = ganador_algoritmo(entradas_g)

    titulo("RESUMEN")
    if gan_len:
        p(f"LENGUAJE MAS RAPIDO : {gan_len}  (promedio {geo_len[gan_len]:.2f}x vs el mejor; "
          f"{len(celdas_comunes)} pruebas en comun)")
        if gan_len_g:
            p(f"   solo n >= {fmt_n(N_GRANDE)}       : {gan_len_g}  (promedio {geo_len_g[gan_len_g]:.2f}x; "
              f"{len(celdas_grandes)} pruebas)")
    else:
        p("LENGUAJE MAS RAPIDO : no se pudo calcular (se necesitan al menos 2 lenguajes con pruebas en comun)")
    if gan_alg:
        p(f"ALGORITMO MAS RAPIDO: {gan_alg}  (posicion promedio {pos_alg[gan_alg]:.2f} de 9; "
          f"{len(entradas)} combinaciones lenguaje/n/caso)")
        if gan_alg_g:
            p(f"   solo n >= {fmt_n(N_GRANDE)}       : {gan_alg_g}  (posicion promedio {pos_alg_g[gan_alg_g]:.2f}; "
              f"{len(entradas_g)} combinaciones)")
    else:
        p("ALGORITMO MAS RAPIDO: no se pudo calcular (faltan pruebas con los 9 algoritmos completos)")

    # ---------- 1. fuentes ----------
    titulo("1. FUENTES DE DATOS Y HARDWARE")
    filas = []
    for l in langs:
        m, d = metas[l], datos[l]
        entorno = f"Python {m.get('python', '?')}" if l == "Python" else \
            (m.get("compilador") or m.get("jvm") or m.get("runtime") or "?")
        cuenta = {e: sum(1 for v in d.values() if v[0] == e) for e in ("OK", "TIMEOUT", "OMITIDO", "ERROR")}
        filas.append([l, entorno[:40], m.get("limite_tiempo_s", "-"), len(d), cuenta["OK"],
                      cuenta["TIMEOUT"], cuenta["OMITIDO"], cuenta["ERROR"]])
        if len(d) != PRUEBAS_ESPERADAS:
            avisos.append(f"{l}: tiene {len(d)} pruebas y se esperaban {PRUEBAS_ESPERADAS}.")
        if cuenta["ERROR"]:
            avisos.append(f"{l}: {cuenta['ERROR']} prueba(s) con ERROR (el algoritmo no ordeno bien).")
    tabla(["Lenguaje", "Entorno", "Limite (s)", "Pruebas", "OK", "TIMEOUT", "OMITIDO", "ERROR"],
          filas, izq=(0, 1))
    for faltante in faltan:
        avisos.append(f"{faltante}: NO se encontro su archivo de resultados; se excluye de la comparacion.")
    limites = {metas[l].get("limite_tiempo_s") for l in langs if metas[l].get("limite_tiempo_s")}
    if len(limites) > 1:
        avisos.append("Los lenguajes usaron LIMITES DE TIEMPO DISTINTOS: " + ", ".join(sorted(limites)) +
                      ". Los TIMEOUT no son comparables entre ellos.")
    p()
    hw = {}
    for l in langs:
        for k in ("procesador", "ram", "grafica"):
            if metas[l].get(k):
                hw.setdefault(k, set()).add(metas[l][k])
    for k, nombre in (("procesador", "Procesador"), ("ram", "RAM"), ("grafica", "Grafica")):
        if k in hw:
            p(f"  {nombre:11}: " + " / ".join(sorted(hw[k])))
            if len(hw[k]) > 1:
                avisos.append(f"El campo '{k}' difiere entre los CSV: no parecen del mismo equipo.")
    if avisos:
        p()
        p("  AVISOS:")
        for a in avisos:
            p("   - " + a)

    # ---------- 2. verificacion de contadores ----------
    titulo("2. VERIFICACION DE CONTADORES (comparaciones e intercambios)")
    claves = {k for l in langs for k in datos[l]}
    distintos, verificadas = [], 0
    for k in sorted(claves, key=lambda k: (k[1], CASOS.index(k[2]) if k[2] in CASOS else 9, k[0])):
        valores = {l: (datos[l][k][2], datos[l][k][3]) for l in langs if k in datos[l] and datos[l][k][0] == "OK"}
        if len(valores) >= 2:
            verificadas += 1
            if len(set(valores.values())) > 1:
                distintos.append((k, valores))
    p(f"  Pruebas con resultado en 2 o mas lenguajes: {verificadas}")
    if not distintos:
        p("  Resultado: los contadores son IDENTICOS en todos los lenguajes (las implementaciones")
        p("  son equivalentes y las diferencias de tiempo vienen del lenguaje, no del algoritmo).")
    else:
        p(f"  ATENCION: {len(distintos)} prueba(s) con contadores distintos entre lenguajes:")
        for k, v in distintos[:15]:
            p(f"   - {k[0]} n={fmt_n(k[1])} {k[2]}: " + "; ".join(f"{l}={c}/{s}" for l, (c, s) in v.items()))

    # ---------- 3. lenguaje mas rapido ----------
    titulo("3. LENGUAJE MAS RAPIDO")
    p(f"  Base: pruebas (algoritmo, n, caso) que los {len(langs)} lenguajes ({', '.join(langs)}) completaron: "
      f"{len(celdas_comunes)}.")
    p("  'Veces mas lento' = media geometrica de (tiempo / tiempo del mejor lenguaje en esa prueba).")
    p("  Con n pequeno (100, 1,000) los tiempos son de microsegundos y tienen mucho ruido.")
    p()
    ranking_lenguajes("3.1 Ranking general", celdas_comunes, langs, datos)
    p()
    ranking_lenguajes(f"3.2 Solo n >= {fmt_n(N_GRANDE)} (tiempos mas confiables)", celdas_grandes, langs, datos)
    p()
    p("3.3 Por tamano de arreglo (media geometrica, 1.00x = mejor)")
    tabla_por_grupo(celdas_comunes, langs, datos, lambda k: k[1], "n", ns)
    p()
    p("3.4 Por algoritmo")
    tabla_por_grupo(celdas_comunes, langs, datos, lambda k: k[0], "Algoritmo", ALGORITMOS)
    p()
    p("3.5 Por caso")
    tabla_por_grupo(celdas_comunes, langs, datos, lambda k: k[2], "Caso", CASOS)
    sin_comun = [k for k in claves if k not in set(celdas_comunes) and
                 any(k in datos[l] and datos[l][k][0] == "OK" for l in langs)]
    p()
    p(f"  Pruebas excluidas (alguno de los lenguajes no la termino: TIMEOUT/OMITIDO/ERROR): {len(sin_comun)}")
    for l in langs:
        m = sum(1 for k in sin_comun if k not in datos[l] or datos[l][k][0] != "OK")
        if m:
            p(f"   - {l}: no termino {m} de ellas")

    # ---------- 4. algoritmo mas rapido ----------
    titulo("4. ALGORITMO MAS RAPIDO")
    p("  Base: cada combinacion (lenguaje, n, caso) donde los 9 algoritmos tienen resultado.")
    p("  Se ordenan por tiempo; los TIMEOUT quedan detras de todos los que terminaron.")
    p(f"  Combinaciones usadas: {len(entradas)} de {len(langs) * len(ns) * len(CASOS)}.")
    p()
    ranking_algoritmos("4.1 Ranking general", entradas)
    p()
    ranking_algoritmos(f"4.2 Solo n >= {fmt_n(N_GRANDE)}", entradas_g)
    p()
    p("4.3 Posicion promedio por tamano de arreglo (1 = mas rapido)")
    filas = []
    for a in ALGORITMOS:
        fila = [a]
        for n in ns:
            r = [rk for (e, rk) in zip(entradas, estadisticas_algoritmos(entradas)[a]["rank"]) if e[1] == n]
            fila.append(f"{media(r):.2f}" if r else "-")
        filas.append(fila)
    tabla(["Algoritmo"] + [fmt_n(n) for n in ns], filas, izq=(0,))
    p()
    p("4.4 Algoritmo ganador por n, caso y lenguaje")
    filas = []
    for n in ns:
        for caso in CASOS:
            fila = [fmt_n(n), caso]
            for l in langs:
                res = {a: datos[l].get((a, n, caso)) for a in ALGORITMOS}
                if all(v and v[0] in ("OK", "TIMEOUT") for v in res.values()) and \
                        any(v[0] == "OK" for v in res.values()):
                    fila.append(min((a for a in ALGORITMOS if res[a][0] == "OK"), key=lambda a: res[a][1]))
                else:
                    fila.append("-")
            filas.append(fila)
    tabla(["n", "Caso"] + langs, filas, izq=(0, 1) + tuple(range(2, 2 + len(langs))))

    p()
    p("4.5 Ranking por comparaciones e intercambios (iguales en todos los lenguajes)")
    rc, rs, usadas = {a: [] for a in ALGORITMOS}, {a: [] for a in ALGORITMOS}, 0
    for n in ns:
        for caso in CASOS:
            cont = {}
            for a in ALGORITMOS:
                for l in langs:
                    v = datos[l].get((a, n, caso))
                    if v and v[0] == "OK":
                        cont[a] = (v[2], v[3])
                        break
            if len(cont) == len(ALGORITMOS):
                usadas += 1
                r1 = rangos({a: cont[a][0] for a in ALGORITMOS})
                r2 = rangos({a: cont[a][1] for a in ALGORITMOS})
                for a in ALGORITMOS:
                    rc[a].append(r1[a])
                    rs[a].append(r2[a])
    if usadas:
        p(f"  Base: {usadas} combinaciones (n, caso) donde los 9 algoritmos terminaron en algun lenguaje.")
        orden = sorted(ALGORITMOS, key=lambda a: media(rc[a]))
        tabla(["Algoritmo", "Pos. prom. comparaciones", "Pos. prom. intercambios"],
              [[a, f"{media(rc[a]):.2f}", f"{media(rs[a]):.2f}"] for a in orden], izq=(0,))
    else:
        p("  (no hay combinaciones con los 9 algoritmos terminados)")

    # ---------- 5. conclusiones ----------
    titulo("5. CONCLUSIONES Y ADVERTENCIAS")
    if gan_len:
        p(f"  * Lenguaje mas rapido: {gan_len}.")
        if gan_len_g and gan_len_g != gan_len:
            p(f"    (con n >= {fmt_n(N_GRANDE)} el mas rapido es {gan_len_g}; los n pequenos tienen mucho ruido)")
    if gan_alg:
        p(f"  * Algoritmo mas rapido: {gan_alg}.")
        if gan_alg_g and gan_alg_g != gan_alg:
            p(f"    (con n >= {fmt_n(N_GRANDE)} el mas rapido es {gan_alg_g})")
    p("  * Bucketsort y Radixsort no son de proposito general: los datos son permutaciones de 1..n,")
    p("    el caso ideal para ambos (Bucketsort queda con 1 elemento por cubeta y 0 comparaciones).")
    p("    Con otro tipo de datos su ventaja podria cambiar.")
    p("  * Un TIMEOUT significa 'mas lento que el limite', no un tiempo exacto.")
    p("  * Java, JavaScript y C# se midieron tras un calentamiento del JIT (no medido); Python y C++ no")
    p("    lo necesitan. Todos corren en el mismo equipo, con una sola corrida por prueba.")

    # ---------- 6. detalle ----------
    if detalle:
        titulo("6. DETALLE: tiempo (s) por lenguaje, comparaciones e intercambios")
        for n in ns:
            for caso in CASOS:
                p()
                p(f"n = {fmt_n(n)} | {caso}")
                filas = []
                for a in ALGORITMOS:
                    fila = [a]
                    cont = None
                    for l in langs:
                        v = datos[l].get((a, n, caso))
                        if v is None:
                            fila.append("-")
                        elif v[0] == "OK":
                            fila.append(fmt_t(v[1]))
                            cont = cont or (v[2], v[3])
                        else:
                            fila.append("OMIT." if v[0] == "OMITIDO" else v[0])
                    fila += [fmt_n(cont[0]), fmt_n(cont[1])] if cont else ["-", "-"]
                    filas.append(fila)
                tabla(["Algoritmo"] + langs + ["Comparaciones", "Intercambios"], filas, izq=(0,))

    ruta_salida = os.path.join(carpeta, "reporte_final.txt")
    try:
        with open(ruta_salida, "w", encoding="utf-8-sig", newline="\n") as f:
            f.write("\n".join(SALIDA) + "\n")
        print(f"\nReporte guardado en {ruta_salida}")
    except OSError as e:
        print(f"\nNo se pudo guardar el reporte: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
