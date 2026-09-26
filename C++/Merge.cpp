#include <iostream>
#include <vector>
using namespace std;

vector<int> mezclar(vector<int>& a, vector<int>& b) {
    vector<int> resultado;
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] <= b[j]) resultado.push_back(a[i++]);
        else resultado.push_back(b[j++]);
    }
    while (i < (int)a.size()) resultado.push_back(a[i++]);
    while (j < (int)b.size()) resultado.push_back(b[j++]);
    return resultado;
}

vector<int> merge(vector<int> arr) {
    if (arr.size() <= 1) return arr;
    int medio = arr.size() / 2;
    vector<int> izquierda(arr.begin(), arr.begin() + medio);
    vector<int> derecha(arr.begin() + medio, arr.end());
    izquierda = merge(izquierda);
    derecha = merge(derecha);
    return mezclar(izquierda, derecha);
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    vector<int> resultado = merge(numeros);
    cout << "Después: "; imprimir(resultado);
    return 0;
}
