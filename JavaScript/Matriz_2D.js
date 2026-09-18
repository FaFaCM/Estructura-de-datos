const matriz2D = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

function recorrido2D(m) {
    let resultado = "";
    for (let fila of m)
        for (let elemento of fila)
            resultado += elemento + " ";
    console.log(resultado);
}

recorrido2D(matriz2D);