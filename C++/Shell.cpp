#include <iostream>
#include <vector>
using namespace std;

void shell(vector<int>& arr) {
    int n = arr.size();
    int salto = n / 2;
    while (salto > 0) {
        for (int i = salto; i < n; i++) {
            int temp = arr[i];
            int j = i;
            while (j >= salto && arr[j - salto] > temp) {
                arr[j] = arr[j - salto];
                j -= salto;
            }
            arr[j] = temp;
        }
        salto /= 2;
    }
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    shell(numeros);
    cout << "Después: "; imprimir(numeros);
    return 0;
}
