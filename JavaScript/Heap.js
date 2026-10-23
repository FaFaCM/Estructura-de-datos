function heapify(arr, n, i) {
    let mayor = i;
    const izq = 2 * i + 1;
    const der = 2 * i + 2;
    if (izq < n && arr[izq] > arr[mayor]) mayor = izq;
    if (der < n && arr[der] > arr[mayor]) mayor = der;
    if (mayor !== i) {
        [arr[i], arr[mayor]] = [arr[mayor], arr[i]];
        heapify(arr, n, mayor);
    }
}

function heap(arr) {
    const n = arr.length;
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) heapify(arr, n, i);
    for (let i = n - 1; i > 0; i--) {
        [arr[0], arr[i]] = [arr[i], arr[0]];
        heapify(arr, i, 0);
    }
    return arr;
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", heap(numeros));
