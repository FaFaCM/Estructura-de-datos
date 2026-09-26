function quick(arr) {
    if (arr.length <= 1) return arr;
    const pivote = arr[Math.floor(arr.length / 2)];
    const menores = arr.filter(x => x < pivote);
    const iguales = arr.filter(x => x === pivote);
    const mayores = arr.filter(x => x > pivote);
    return [...quick(menores), ...iguales, ...quick(mayores)];
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", quick(numeros));
