function bucket(arr) {
    const cubetas = Array.from({ length: 10 }, () => []);
    for (const x of arr) {
        cubetas[Math.floor(x / 10)].push(x);
    }
    let resultado = [];
    for (const c of cubetas) {
        c.sort((a, b) => a - b);
        resultado = resultado.concat(c);
    }
    return resultado;
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", bucket(numeros));
