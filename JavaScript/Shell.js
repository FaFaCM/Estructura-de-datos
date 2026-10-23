function shell(arr) {
    const n = arr.length;
    let salto = Math.floor(n / 2);
    while (salto > 0) {
        for (let i = salto; i < n; i++) {
            const temp = arr[i];
            let j = i;
            while (j >= salto && arr[j - salto] > temp) {
                arr[j] = arr[j - salto];
                j -= salto;
            }
            arr[j] = temp;
        }
        salto = Math.floor(salto / 2);
    }
    return arr;
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", shell(numeros));
