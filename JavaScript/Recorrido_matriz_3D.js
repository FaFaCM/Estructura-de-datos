const matriz3D = [
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
];

function recorrido3D(m) {
    let resultado = "";
    for (let capa of m)
        for (let fila of capa)
            for (let elemento of fila)
                resultado += elemento + " ";
    console.log(resultado);
}

recorrido3D(matriz3D);