#include <iostream>
#include <vector>
using namespace std;

void seleccion(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int menor = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[menor]) menor = j;
        }
        swap(arr[i], arr[menor]);
    }
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    seleccion(numeros);
    cout << "Después: "; imprimir(numeros);
    return 0;
}
