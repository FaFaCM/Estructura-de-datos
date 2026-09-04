#include <iostream>
using namespace std;

int main()
{
    int arreglo[10] = { 10, 20, 30 };
    int n = 3;
    int valor = 40;

    arreglo[n] = valor;
    n++;

    for (int i = 0; i < n; i++)
        cout << arreglo[i] << " ";

    return 0;
}