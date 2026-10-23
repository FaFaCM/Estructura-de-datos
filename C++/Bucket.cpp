#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

vector<int> bucket(vector<int>& arr) {
    vector<vector<int>> cubetas(10);
    for (int x : arr) cubetas[x / 10].push_back(x);
    vector<int> resultado;
    for (auto& c : cubetas) {
        sort(c.begin(), c.end());
        resultado.insert(resultado.end(), c.begin(), c.end());
    }
    return resultado;
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    vector<int> resultado = bucket(numeros);
    cout << "Después: "; imprimir(resultado);
    return 0;
}
