function insercion(arr) {
    for (let i = 1; i < arr.length; i++) {
        let actual = arr[i];
        let j = i - 1;
        while (j >= 0 && arr[j] > actual) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = actual;
    }
    return arr;
}

const numeros = [5, 3, 8, 1, 9, 2];
console.log("Antes:", numeros);
console.log("Después:", insercion(numeros));
