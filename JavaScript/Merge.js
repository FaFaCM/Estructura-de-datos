function mezclar(a, b) {
    const resultado = [];
    let i = 0, j = 0;
    while (i < a.length && j < b.length) {
        if (a[i] <= b[j]) resultado.push(a[i++]);
        else resultado.push(b[j++]);
    }
    return resultado.concat(a.slice(i)).concat(b.slice(j));
}

function merge(arr) {
    if (arr.length <= 1) return arr;
    const medio = Math.floor(arr.length / 2);
    const izquierda = merge(arr.slice(0, medio));
    const derecha = merge(arr.slice(medio));
    return mezclar(izquierda, derecha);
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", merge(numeros));
