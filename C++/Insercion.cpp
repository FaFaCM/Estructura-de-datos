#include <iostream>
#include <vector>
using namespace std;

void insercion(vector<int>& arr) {
    for (int i = 1; i < (int)arr.size(); i++) {
        int actual = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > actual) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = actual;
    }
}

void imprimir(vector<int>& arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> numeros = {5, 3, 8, 1, 9, 2};
    cout << "Antes: "; imprimir(numeros);
    insercion(numeros);
    cout << "Después: "; imprimir(numeros);
    return 0;
}
