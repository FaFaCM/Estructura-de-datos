let arreglo = [10, 20, 30, 40, 50];
let n = 5;

function elPosicion(pos) {
    for (let i = pos; i < n - 1; i++) {
        arreglo[i] = arreglo[i + 1];
    }
    n--;
}

elPosicion(2);
console.log(arreglo.slice(0, n));