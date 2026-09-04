let arreglo = [3, 8, 15, 23, 42, 56, 70];

function busBinaria(valor) {
    let izquierda = 0;
    let derecha = arreglo.length - 1;

    while (izquierda <= derecha) {
        let medio = Math.floor((izquierda + derecha) / 2);

        if (arreglo[medio] === valor) {
            return medio;
        } else if (arreglo[medio] < valor) {
            izquierda = medio + 1;
        } else {
            derecha = medio - 1;
        }
    }
    return -1;
}

console.log(busBinaria(23));