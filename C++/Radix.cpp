#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void radix(vector<int>& arr) {
    int mayor = *max_element(arr.begin(), arr.end());
    for (int exp = 1; mayor / exp > 0; exp *= 10) {
        vector<vector<int>> cubetas(10);
        for (int x : arr) cubetas[(x / exp) % 10].push_back(x);
        int k = 0;
        for (auto& c : cubetas)
            for (int x : c) arr[k++] = x;
    }
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    radix(numeros);
    cout << "Después: "; imprimir(numeros);
    return 0;
}
