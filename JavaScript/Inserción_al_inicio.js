let arreglo = [10, 20, 30, 0, 0, 0, 0, 0, 0, 0];
let n = 3;

function insInicio(valor) {
    for (let i = n; i > 0; i--) {
        arreglo[i] = arreglo[i - 1];
    }
    arreglo[0] = valor;
    n++;
}

insInicio(5);
console.log(arreglo.slice(0, n));