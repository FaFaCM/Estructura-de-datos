#include <iostream>
#include <vector>
using namespace std;

void burbuja(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    burbuja(numeros);
    cout << "Después: "; imprimir(numeros);
    return 0;
}
