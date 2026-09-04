let arreglo = [10, 20, 30, 40];
let n = 4;

function elInicio() {
    for (let i = 0; i < n - 1; i++) {
        arreglo[i] = arreglo[i + 1];
    }
    n--;
}

elInicio();
console.log(arreglo.slice(0, n));