function radix(arr) {
    const mayor = Math.max(...arr);
    for (let exp = 1; Math.floor(mayor / exp) > 0; exp *= 10) {
        const cubetas = Array.from({ length: 10 }, () => []);
        for (const x of arr) {
            cubetas[Math.floor(x / exp) % 10].push(x);
        }
        arr = [].concat(...cubetas);
    }
    return arr;
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", radix(numeros));
