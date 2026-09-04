let arreglo = [15, 3, 42, 8, 23];

function busSecuencial(valor) {
    for (let i = 0; i < arreglo.length; i++) {
        if (arreglo[i] === valor) {
            return i;
        }
    }
    return -1;
}

console.log(busSecuencial(42));