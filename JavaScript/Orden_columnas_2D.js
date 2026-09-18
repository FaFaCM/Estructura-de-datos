const matriz2D = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

function ordenPorColumnas(m) {
    let resultado = "";
    for (let j = 0; j < m[0].length; j++)
        for (let i = 0; i < m.length; i++)
            resultado += m[i][j] + " ";
    console.log(resultado);
}

ordenPorColumnas(matriz2D);