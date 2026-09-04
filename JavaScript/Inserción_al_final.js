let arreglo = [10, 20, 30, 0, 0, 0, 0, 0, 0, 0];
let n = 3;

function insFinal(valor) {
    arreglo[n] = valor;
    n++;
}

insFinal(40);
console.log(arreglo.slice(0, n));