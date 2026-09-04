#include <iostream>
using namespace std;

int main()
{
    int arreglo[10] = { 10, 20, 30 };
    int n = 3;
    int valor = 1;

    for (int i = n; i > 0; i--)
    {
        arreglo[i] = arreglo[i - 1];
    }
    arreglo[0] = valor;
    n++;

    for (int i = 0; i < n; i++)
        cout << arreglo[i] << " ";

    return 0;
}