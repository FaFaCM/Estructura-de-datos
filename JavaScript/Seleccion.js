function seleccion(arr) {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        let menor = i;
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[menor]) menor = j;
        }
        [arr[i], arr[menor]] = [arr[menor], arr[i]];
    }
    return arr;
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", seleccion(numeros));
