#include <iostream>
#include <vector>
using namespace std;

vector<int> quick(vector<int> arr) {
    if (arr.size() <= 1) return arr;
    int pivote = arr[arr.size() / 2];
    vector<int> menores, iguales, mayores;
    for (int x : arr) {
        if (x < pivote) menores.push_back(x);
        else if (x == pivote) iguales.push_back(x);
        else mayores.push_back(x);
    }
    vector<int> izquierda = quick(menores);
    vector<int> derecha = quick(mayores);
    vector<int> resultado = izquierda;
    resultado.insert(resultado.end(), iguales.begin(), iguales.end());
    resultado.insert(resultado.end(), derecha.begin(), derecha.end());
    return resultado;
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    vector<int> resultado = quick(numeros);
    cout << "Después: "; imprimir(resultado);
    return 0;
}
