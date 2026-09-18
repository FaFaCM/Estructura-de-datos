const matriz2D = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

function ordenPorFilas(m) {
    let resultado = "";
    for (let i = 0; i < m.length; i++)
        for (let j = 0; j < m[i].length; j++)
            resultado += m[i][j] + " ";
    console.log(resultado);
}

ordenPorFilas(matriz2D);